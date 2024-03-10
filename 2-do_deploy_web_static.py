#!/usr/bin/python3
'''
Fabric Script
'''


from fabric.api import env, local, run, put
from datetime import datetime
import os

env.hosts = ['54.157.179.66', '100.25.35.151']
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_pack():
    '''Compress the webstatic doc'''
    try:
        # create the file name
        creation_time = datetime.now().strftime("%Y%m%d%H%M%S")
        Z_fil_name = "web_static_{}.tgz".format(creation_time)

        # create the version folder
        local("mkdir -p versions")

        # compress the file
        local("tar -vczf versions/{} web_static".format(Z_fil_name))
        return os.path.join("versions", Z_fil_name)
    except Exception:
        return None


def do_deploy(archive_path):
    ''' deploy the web static'''
    if not os.path.exists(archive_path):
        print('the path doesnt exist')
        return False
    try:
        arc_name = os.path.basename(archive_path)
        arc_file_name = os.path.splitext(arc_name)[0]
        release_path = '/data/web_static/releases/{}'.format(arc_file_name)
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(arc_name, release_path))
        run('rm /tmp/{}'.format(arc_name))
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        return True
    except Exception as e:
        print(e)
        return False
# def do_delete(archive_path):
#     if not os.path.exists(archive_path):
#         print('the path doesnt exist')
#         return False
#     try:
#         arc_name = os.path.basename(archive_path)
#         arc_file_name = os.path.splitext(arc_name)[0]
#         release_path = '/data/web_static/releases/{}'.format(arc_file_name)
#         run('rm -rf {}'.format(release_path))
#         return True
#     except Exception as e:
#         print(e)
#         return False
