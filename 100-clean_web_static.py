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
        number = int(number)
        if number <= 1:
            number = 1

        # Delete archives locally
        local("ls -t versions | tail -n +{} | "
              "xargs -I {{}} rm versions/{{}}".format(number + 1))

        # Delete archives locally
        releases_path = "/data/web_static/releases"
        run("ls -t {} | tail -n +{} | "
            "xargs -I {{}} rm -rf {}/{{}}".format(releases_path, number + 1,
                                                  releases_path))

        return True
    except Exception as e:
        return False
