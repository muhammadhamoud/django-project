# data/services/scanner.py

import posixpath
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from data.models import (
    PropertySFTPSource,
    FileRule,
    IncomingFile,
    FileLoadLog,
)
from data.services.sftp import (
    connect_sftp,
    list_files_non_recursive,
    walk_sftp_recursive,
)
from data.services.matcher import (
    match_rule,
    extract_business_date,
)
from data.services.checksum import calculate_remote_checksum
from data.services.expected_files import mark_expected_file_found


def get_filtered_sources(server_name=None, property_code=None, source_name=None):
    sources = PropertySFTPSource.objects.filter(
        is_active=True,
        server__is_active=True,
        property__is_active=True,
    ).select_related("server", "property")

    if server_name:
        sources = sources.filter(server__name=server_name)

    if property_code:
        sources = sources.filter(property__resort_code=property_code)

    if source_name:
        sources = sources.filter(source_name=source_name)

    return sources


def group_sources_by_server(sources):
    grouped = {}
    for source in sources:
        grouped.setdefault(source.server_id, []).append(source)
    return grouped


def get_rules_for_source(source):
    return FileRule.objects.filter(
        is_active=True,
        property=source.property,
        source=source,
    ).select_related("domain")


def should_scan_recursively(rules):
    return any(rule.recursive_scan for rule in rules)


def get_max_scan_depth(rules):
    if not rules:
        return 1
    return max(rule.max_scan_depth for rule in rules)


def get_source_iterator(client, remote_path, rules):
    recursive = should_scan_recursively(rules)
    if recursive:
        max_depth = get_max_scan_depth(rules)
        return walk_sftp_recursive(client, remote_path, max_depth=max_depth)
    return list_files_non_recursive(client, remote_path)


def convert_sftp_mtime_to_aware_datetime(st_mtime):
    if not st_mtime:
        return None
    return datetime.fromtimestamp(
        st_mtime,
        tz=timezone.get_current_timezone(),
    )


def process_discovered_file(client, source, folder_path, entry, rules, forced_date=None, dry_run=False):
    property_obj = source.property
    file_name = entry.filename
    file_path = posixpath.join(folder_path, file_name)
    file_size = getattr(entry, "st_size", None)
    modified_at = convert_sftp_mtime_to_aware_datetime(getattr(entry, "st_mtime", None))

    matched_rule = match_rule(file_name=file_name, file_path=file_path, rules=rules)
    matched_domain = matched_rule.domain if matched_rule else None
    parsed_file_date = extract_business_date(
        file_name=file_name,
        file_path=file_path,
        rule=matched_rule,
        forced_date=forced_date,
    )

    checksum = None
    checksum_type = None

    if matched_rule and matched_rule.hash_type != "none" and not dry_run:
        checksum = calculate_remote_checksum(
            client=client,
            file_path=file_path,
            hash_type=matched_rule.hash_type,
        )
        checksum_type = matched_rule.hash_type

    if dry_run:
        return {
            "created": 0,
            "updated": 0,
            "scanned": 1,
            "message": (
                f"[DRY RUN] {file_path} | "
                f"rule={matched_rule.name if matched_rule else '-'} | "
                f"domain={matched_domain.name if matched_domain else '-'} | "
                f"file_date={parsed_file_date}"
            ),
        }

    with transaction.atomic():
        obj, created = IncomingFile.objects.update_or_create(
            source=source,
            file_path=file_path,
            defaults={
                "property": property_obj,
                "domain": matched_domain,
                "rule": matched_rule,
                "file_name": file_name,
                "folder_path": folder_path,
                "file_date": parsed_file_date,
                "file_size": file_size,
                "checksum": checksum,
                "checksum_type": checksum_type,
                "modified_at_source": modified_at,
                "status": IncomingFile.Status.DISCOVERED,
            },
        )

        FileLoadLog.objects.create(
            incoming_file=obj,
            action=FileLoadLog.Action.DISCOVER,
            message=f"File discovered on SFTP scan: {file_name}",
        )

        mark_expected_file_found(
            rule=matched_rule,
            file_date=parsed_file_date,
            incoming_file=obj,
        )

    return {
        "created": 1 if created else 0,
        "updated": 0 if created else 1,
        "scanned": 1,
        "message": None,
    }


def scan_single_source(client, source, file_date=None, dry_run=False, logger=None):
    rules = list(get_rules_for_source(source))
    iterator = get_source_iterator(client, source.remote_path, rules)

    scanned = 0
    created_count = 0
    updated_count = 0

    for folder_path, entry in iterator:
        result = process_discovered_file(
            client=client,
            source=source,
            folder_path=folder_path,
            entry=entry,
            rules=rules,
            forced_date=file_date,
            dry_run=dry_run,
        )

        scanned += result["scanned"]
        created_count += result["created"]
        updated_count += result["updated"]

        if logger and result["message"]:
            logger(result["message"])

    return {
        "scanned": scanned,
        "created": created_count,
        "updated": updated_count,
    }


def scan_sources(server_name=None, property_code=None, source_name=None, file_date=None, dry_run=False, logger=None):
    sources = get_filtered_sources(
        server_name=server_name,
        property_code=property_code,
        source_name=source_name,
    )

    if not sources.exists():
        raise ValueError("No matching active SFTP sources found.")

    grouped = group_sources_by_server(sources)

    total_scanned = 0
    total_created = 0
    total_updated = 0

    for _, server_sources in grouped.items():
        server = server_sources[0].server

        if logger:
            logger(f"Connecting to SFTP server: {server.name} ({server.host})")

        client, transport = connect_sftp(server)

        try:
            for source in server_sources:
                if logger:
                    logger(f"Scanning {source.property} / {source.source_name} -> {source.remote_path}")

                result = scan_single_source(
                    client=client,
                    source=source,
                    file_date=file_date,
                    dry_run=dry_run,
                    logger=logger,
                )

                total_scanned += result["scanned"]
                total_created += result["created"]
                total_updated += result["updated"]
        finally:
            client.close()
            transport.close()

    return {
        "scanned": total_scanned,
        "created": total_created,
        "updated": total_updated,
        "dry_run": dry_run,
    }