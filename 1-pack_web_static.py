#!/usr/bin/python3
'''
Fabric Script
'''


from fabric.api import local
from datetime import datetime
import os


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
