# data/services/checksum.py

import hashlib


def get_hasher(hash_type):
    if hash_type == "md5":
        return hashlib.md5()
    if hash_type == "sha1":
        return hashlib.sha1()
    if hash_type == "sha256":
        return hashlib.sha256()
    return None


def calculate_remote_checksum(client, file_path, hash_type="md5", chunk_size=1024 * 1024):
    """
    Calculate checksum by streaming file content from SFTP.
    """
    hasher = get_hasher(hash_type)
    if not hasher:
        return None

    with client.open(file_path, "rb") as remote_file:
        while True:
            chunk = remote_file.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()