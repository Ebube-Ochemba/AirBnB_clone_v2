#!/usr/bin/python3
"""
A Fabric script that deletes out-of-date archives.
"""

from fabric.api import run, env, local

env.hosts = ['52.86.25.3', '35.153.194.184']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Deletes out-of-date archives"""

    try:
        if int(number) == 0:
            number = 1

        # Ensure we keep at least the most recent version
        number = int(number) + 1

        # Delete archives locally
        local("ls -dt versions/* | tail -n +{} | sudo "
              "xargs rm -fr".format(number))

        # Delete archives locally
        remote_path = "/data/web_static/releases/*"
        run("ls -dt {} | tail -n +{} | sudo "
            "xargs rm -fr".format(remmote_path, number))

        return True
    except Exception as e:
        return False
