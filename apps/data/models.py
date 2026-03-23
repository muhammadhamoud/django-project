# data/models.py

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class DataBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class FileDomain(DataBaseModel):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SFTPServer(DataBaseModel):
    name = models.CharField(max_length=150, unique=True)
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=22)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    private_key_path = models.CharField(max_length=500, blank=True, null=True)
    base_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PropertySFTPSource(DataBaseModel):
    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="data_sources",
    )
    server = models.ForeignKey(
        SFTPServer,
        on_delete=models.CASCADE,
        related_name="property_sources",
    )
    source_name = models.CharField(max_length=150)
    remote_path = models.CharField(max_length=500)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["property", "source_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "server", "source_name", "remote_path"],
                name="uniq_property_server_source_remote_path",
            )
        ]

    def __str__(self):
        return f"{self.property} - {self.source_name}"


class FileRule(DataBaseModel):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        AD_HOC = "ad_hoc", "Ad Hoc"

    class MatchType(models.TextChoices):
        CONTAINS = "contains", "Contains"
        STARTSWITH = "startswith", "Starts With"
        EXACT = "exact", "Exact"
        REGEX = "regex", "Regex"

    class DateSource(models.TextChoices):
        NONE = "none", "None"
        FILENAME = "filename", "Filename"
        FOLDER = "folder", "Folder"
        FORCED = "forced", "Forced"

    class HashType(models.TextChoices):
        NONE = "none", "None"
        MD5 = "md5", "MD5"
        SHA1 = "sha1", "SHA1"
        SHA256 = "sha256", "SHA256"

    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="file_rules",
    )
    source = models.ForeignKey(
        PropertySFTPSource,
        on_delete=models.CASCADE,
        related_name="file_rules",
    )
    domain = models.ForeignKey(
        FileDomain,
        on_delete=models.CASCADE,
        related_name="file_rules",
    )

    name = models.CharField(max_length=200)

    match_type = models.CharField(
        max_length=20,
        choices=MatchType.choices,
        default=MatchType.CONTAINS,
    )
    expected_filename_pattern = models.CharField(
        max_length=500,
        help_text="Plain text or regex depending on match_type."
    )
    file_extension = models.CharField(max_length=20, blank=True, null=True)

    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.DAILY,
    )
    expected_by_time = models.TimeField(blank=True, null=True)
    is_required = models.BooleanField(default=True)

    recursive_scan = models.BooleanField(default=False)
    max_scan_depth = models.PositiveIntegerField(default=3)

    folder_date_regex = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=r"Regex for folder date. Example: (?P<date>\d{4}-\d{2}-\d{2})"
    )
    filename_date_regex = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=r"Regex for filename date. Example: (?P<date>\d{8})"
    )
    date_source = models.CharField(
        max_length=20,
        choices=DateSource.choices,
        default=DateSource.NONE,
    )

    delimiter = models.CharField(max_length=10, blank=True, null=True)
    encoding = models.CharField(max_length=50, blank=True, null=True, default="utf-8")

    hash_type = models.CharField(
        max_length=20,
        choices=HashType.choices,
        default=HashType.NONE,
    )
    min_file_size = models.BigIntegerField(blank=True, null=True)
    max_file_size = models.BigIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["property", "domain", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "source", "domain", "name"],
                name="uniq_file_rule_per_property_source_domain_name",
            )
        ]

    def __str__(self):
        return f"{self.property} - {self.name}"


class IncomingFile(DataBaseModel):
    class Status(models.TextChoices):
        DISCOVERED = "discovered", "Discovered"
        DOWNLOADED = "downloaded", "Downloaded"
        VALIDATED = "validated", "Validated"
        LOADED = "loaded", "Loaded"
        FAILED = "failed", "Failed"
        SKIPPED = "skipped", "Skipped"
        MISSING = "missing", "Missing"

    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="incoming_files",
    )
    source = models.ForeignKey(
        PropertySFTPSource,
        on_delete=models.CASCADE,
        related_name="incoming_files",
    )
    domain = models.ForeignKey(
        FileDomain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_files",
    )
    rule = models.ForeignKey(
        FileRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_files",
    )

    file_name = models.CharField(max_length=255, db_index=True)
    file_path = models.CharField(max_length=1000)
    folder_path = models.CharField(max_length=1000, blank=True, null=True)

    file_date = models.DateField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=128, blank=True, null=True)
    checksum_type = models.CharField(max_length=20, blank=True, null=True)
    modified_at_source = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DISCOVERED,
    )
    load_message = models.TextField(blank=True, null=True)
    loaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["source", "file_path"],
                name="uniq_incoming_file_per_source_path",
            )
        ]
        indexes = [
            models.Index(fields=["property", "file_name"]),
            models.Index(fields=["property", "file_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["rule", "file_date"]),
        ]

    def __str__(self):
        return self.file_name


class ExpectedFile(DataBaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        FOUND = "found", "Found"
        MISSING = "missing", "Missing"
        LATE = "late", "Late"
        SKIPPED = "skipped", "Skipped"

    rule = models.ForeignKey(
        FileRule,
        on_delete=models.CASCADE,
        related_name="expected_files",
    )
    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="expected_files",
    )
    source = models.ForeignKey(
        PropertySFTPSource,
        on_delete=models.CASCADE,
        related_name="expected_files",
    )
    expected_date = models.DateField()
    expected_filename = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    is_found = models.BooleanField(default=False)
    found_at = models.DateTimeField(blank=True, null=True)
    incoming_file = models.ForeignKey(
        IncomingFile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="expected_matches",
    )
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-expected_date", "rule__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["rule", "expected_date"],
                name="uniq_expected_file_per_rule_date",
            )
        ]
        indexes = [
            models.Index(fields=["property", "expected_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.rule.name} - {self.expected_date}"


class FileLoadBatch(DataBaseModel):
    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        PARTIAL = "partial", "Partial"
        FAILED = "failed", "Failed"

    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="file_load_batches",
    )
    domain = models.ForeignKey(
        FileDomain,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_load_batches",
    )
    source = models.ForeignKey(
        PropertySFTPSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_load_batches",
    )

    run_date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RUNNING)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)
    total_files = models.PositiveIntegerField(default=0)
    loaded_files = models.PositiveIntegerField(default=0)
    failed_files = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.property} - {self.run_date} - {self.status}"


class FileLoadLog(DataBaseModel):
    class Action(models.TextChoices):
        DISCOVER = "discover", "Discover"
        DOWNLOAD = "download", "Download"
        VALIDATE = "validate", "Validate"
        LOAD = "load", "Load"
        FAIL = "fail", "Fail"
        RETRY = "retry", "Retry"
        MANUAL_UPDATE = "manual_update", "Manual Update"

    incoming_file = models.ForeignKey(
        IncomingFile,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    batch = models.ForeignKey(
        FileLoadBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    message = models.TextField(blank=True, null=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_load_logs",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.incoming_file.file_name} - {self.action}"