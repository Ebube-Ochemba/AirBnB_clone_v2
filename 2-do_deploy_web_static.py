#!/usr/bin/python3
"""
A Fabric script that deploys an archive to my web servers.
"""

from fabric.api import put, run, env
from os.path import exists, basename
env.hosts = ['52.86.25.3', '35.153.194.184']


def do_deploy(archive_path):
    """Deploys an archive with Fabric"""

    if exists(archive_path) is False:
        return False

    try:
        # Extract the filename from the path
        filename = basename(archive_path)

        # Remove periond from filename
        name = filename.split(".")[0]

        # Store directory for archive in variable
        path = "/data/web_static/releases/"

        # Upload archive to the /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Create a directory for the archive on the web servers
        run('sudo mkdir -p {}{}/'.format(path, name))

        # Extract the archive contents to the directory created
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(filename, path, name))

        # Remove the archive from the /tmp/ directory
        run('sudo rm /tmp/{}'.format(filename))

        # Moves contents of 'web_static' to archive directory
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, name))

        # Removes web_static directory.
        run('sudo rm -rf {}{}/web_static'.format(path, name))

        # Removes existing and create new symbolic link
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
