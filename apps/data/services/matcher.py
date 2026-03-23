# data/services/matcher.py

import re
from datetime import datetime


SUPPORTED_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y%m%d",
    "%d-%m-%Y",
    "%d%m%Y",
    "%Y_%m_%d",
)


def normalize_extension(ext):
    if not ext:
        return ""
    ext = ext.strip().lower()
    if ext and not ext.startswith("."):
        ext = f".{ext}"
    return ext


def file_matches_extension(file_name, expected_extension):
    """
    Return True if:
    - no extension rule was provided, or
    - the filename ends with the required extension
    """
    expected_extension = normalize_extension(expected_extension)
    if not expected_extension:
        return True
    return file_name.lower().endswith(expected_extension)


def file_matches_pattern(file_name, pattern, match_type):
    """
    Match the filename against the rule pattern.
    Supported match types:
    - contains
    - startswith
    - exact
    - regex
    """
    if not pattern:
        return False

    if match_type == "contains":
        return pattern.lower() in file_name.lower()

    if match_type == "startswith":
        return file_name.lower().startswith(pattern.lower())

    if match_type == "exact":
        return file_name.lower() == pattern.lower()

    if match_type == "regex":
        return re.search(pattern, file_name) is not None

    return False


def parse_date_string(value):
    """
    Try common date formats and return a Python date.
    """
    if not value:
        return None

    value = value.strip()
    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def extract_date_from_filename(file_name, filename_date_regex):
    """
    Example regex:
        (?P<date>\d{8})
    or
        (?P<date>\d{4}-\d{2}-\d{2})

    The regex must contain a named group: 'date'
    """
    if not filename_date_regex:
        return None

    match = re.search(filename_date_regex, file_name)
    if not match:
        return None

    date_value = match.groupdict().get("date")
    return parse_date_string(date_value)


def extract_date_from_folder(file_path, folder_date_regex):
    """
    Example regex:
        (?P<date>\d{4}-\d{2}-\d{2})
    """
    if not folder_date_regex:
        return None

    match = re.search(folder_date_regex, file_path)
    if not match:
        return None

    date_value = match.groupdict().get("date")
    return parse_date_string(date_value)


def extract_business_date(file_name, file_path, rule, forced_date=None):
    """
    Decide the file business date using:
    1. forced_date if passed from command
    2. rule.date_source == filename
    3. rule.date_source == folder
    4. None
    """
    if forced_date:
        return datetime.strptime(forced_date, "%Y-%m-%d").date()

    if not rule:
        return None

    if rule.date_source == "filename":
        return extract_date_from_filename(file_name, rule.filename_date_regex)

    if rule.date_source == "folder":
        return extract_date_from_folder(file_path, rule.folder_date_regex)

    return None


def file_matches_rule(file_name, file_path, rule):
    """
    True only if:
    - extension matches
    - filename pattern matches
    """
    extension_ok = file_matches_extension(file_name, rule.file_extension)
    if not extension_ok:
        return False

    pattern_ok = file_matches_pattern(
        file_name=file_name,
        pattern=rule.expected_filename_pattern,
        match_type=rule.match_type,
    )
    if not pattern_ok:
        return False

    return True


def match_rule(file_name, file_path, rules):
    """
    Return the first matching rule.
    You can later improve this to prioritize exact > regex > contains, etc.
    """
    for rule in rules:
        if file_matches_rule(file_name, file_path, rule):
            return rule
    return None