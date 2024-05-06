#!/usr/bin/python3
"""
A Facric Script that creates a .tgz archive from the
contents of the 'web_static' folder.
"""

from datetime import datetime
from fabric.api import local


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
