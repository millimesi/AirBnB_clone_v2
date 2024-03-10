#!/usr/bin/python3
''' 
Fabric Script 
'''


from fabric.api import env, local, run, put
import os

env.hosts = ['54.157.179.66', '100.25.35.151']
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"

def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        print('the path doesnt exist')
        return False
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/web_static_20240308100331')
        run('tar -xzf /tmp/web_static_20240308100331 -C /data/web_static/releases/web_static_20240308100331')
        run('rm /tmp/web_static_20240308100331')
        run('mv /data/web_static/releases/web_static_20240308100331/web_static/* /data/web_static/releases/web_static_20240308100331/')
        run('rm -rf /data/web_static/releases/web_static_20240308100331/web_static/')
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/web_static_20240308100331/ /data/web_static/current')
        return True
    except Exception as e:
        print(e)
        return False


