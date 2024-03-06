#!/usr/bin/python3
""" A Fabric script"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if generated successfully, None otherwise.
    """
    try:
        # create 'versions' folder
        local("mkdir -p versions")

        # Create archive name with the current timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Compress the contents of the web_static folder
        # c: Create a new archive.
        # v: Verbosely list the files processed.
        # z: Compress the archive using gzip.
        # f: Use archive file specified.
        local("tar -czvf versions/{} web_static".format(archive_name))

        # Returns archive path if successful
        return os.path.join("versions", archive_name)
    except Exception:
        return None
