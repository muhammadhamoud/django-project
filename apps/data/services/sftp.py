# data/services/sftp.py

import posixpath
import stat
import paramiko


def connect_sftp(server):
    transport = paramiko.Transport((server.host, server.port))
    try:
        if server.private_key_path:
            key = paramiko.RSAKey.from_private_key_file(server.private_key_path)
            transport.connect(username=server.username, pkey=key)
        else:
            transport.connect(username=server.username, password=server.password)

        client = paramiko.SFTPClient.from_transport(transport)
        return client, transport
    except Exception:
        transport.close()
        raise


def list_files_non_recursive(client, remote_path):
    """
    Return tuples of:
    (folder_path, entry)
    """
    entries = client.listdir_attr(remote_path)
    for entry in entries:
        if stat.S_ISDIR(entry.st_mode):
            continue
        yield remote_path, entry


def walk_sftp_recursive(client, root_path, max_depth=3, current_depth=0):
    """
    Yield tuples of:
    (folder_path, entry)
    """
    entries = client.listdir_attr(root_path)

    for entry in entries:
        full_path = posixpath.join(root_path, entry.filename)

        if stat.S_ISDIR(entry.st_mode):
            if current_depth < max_depth:
                yield from walk_sftp_recursive(
                    client=client,
                    root_path=full_path,
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                )
        else:
            yield root_path, entry