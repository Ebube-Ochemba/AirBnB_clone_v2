#!/usr/bin/python3
"""
A Fabric script that creates and distributes an archive to your web servers,
using the function 'deploy'.
"""

from datetime import datetime
from fabric.api import local, put, run, env
from os.path import exists, basename

env.hosts = ['52.86.25.3', '35.153.194.184']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

# Global variable to store the archive path
archive_path = None

def do_pack():
    """Creates a .tgz archive"""
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(timestamp)
        print("Packing web_static to {}".format(filename))
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploys an archive with Fabric"""

    if exists(archive_path) is False:
        return False

    try:
        filename = basename(archive_path)
        name = filename.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(filename, path, name))
        run('rm /tmp/{}'.format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, name))
        run('rm -rf {}{}/web_static'.format(path, name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Creates and distributes an archive to your web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
