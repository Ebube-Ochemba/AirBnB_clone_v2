#!/usr/bin/python3
"""
A Fabric script that deploys an archive to my web servers.
"""

from fabric.api import put, run, env
from os.path import exists, basename

env.hosts = ['52.86.25.3', '35.153.194.184']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys an archive with Fabric"""

    if exists(archive_path) is False:
        return False

    try:
        # Extract filename and name, store directory for archive in variable
        filename = basename(archive_path)
        name = filename.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload archive to the /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Create a directory for the archive on the web servers
        run('mkdir -p {}{}/'.format(path, name))

        # Extract the archive contents to the directory created
        run('tar -xzf /tmp/{} -C {}{}/'.format(filename, path, name))

        # Remove the archive from the /tmp/ directory
        run('rm /tmp/{}'.format(filename))

        # Moves contents of 'web_static' to archive directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, name))

        # Removes web_static directory
        run('rm -rf {}{}/web_static'.format(path, name))

        # Removes existing and create new symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
