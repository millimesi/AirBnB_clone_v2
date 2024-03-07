#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['18.210.33.153', '54.236.27.119']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        date_format = "%Y%m%d%H%M%S"
        date_str = datetime.utcnow().strftime(date_format)
        file_name = "versions/web_static_{}.tgz".format(date_str)

        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]
        release_path = '/data/web_static/releases/{}'.format(folder_name)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Move contents to the proper location
        run('mv {}/web_static/* {}/'.format(release_path, release_path))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    archive_path = do_pack()
    if archive_path:
        do_deploy(archive_path)
    else:
        print('Packaging failed.')
