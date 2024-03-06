#!/usr/bin/python3
"""A Fabric script"""

from datetime import datetime
from fabric.api import local, put, run, env
import os


env.hosts = ["100.25.177.26", "54.146.76.247"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


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


def do_deploy(archive_path):
    """
    Fabric scripts that distributes an archive to your web servers

    Return: False if the file at the path archive_path doesn’t exist
    """

    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    for host in env.hosts:
        with Connection(host=host):
            # Remote path for extraction
            remote_tmp_path = "/tmp/"
            put(archive_path, remote_tmp_path)

            # Extract the archive to the /data/web_static/releases/ directory
            archive_filename = os.path.basename(archive_path)
            arc_name_new = os.path.splitext(archive_filename)[0]
            release_path = "/data/web_static/releases/{}".format(arc_name_new)
            path = os.path.join(remote_tmp_path, archive_filename)
            run("mkdir -p {}".format(release_path))
            run("tar -xzf {} -C {}".format(path, release_path))

            # Remove the archive from the /tmp/ directory on the web server
            run("rm {}".format(path))

            # Move the contents to the proper location
            run("mv {}/web_static/* {}".format(release_path, release_path))
            run("rm -rf {}/web_static".format(release_path))

            # Delete the symbolic link from the web server
            run("rm /data/web_static/current")

            # Create a new the symbolic link /data/web_static/current on
            # the web server, linked to the new version of your code
            # (/data/web_static/releases/<archive filename without extension>)
            run("ln -sf {} /data/web_static/current".format(release_path))
    return True
