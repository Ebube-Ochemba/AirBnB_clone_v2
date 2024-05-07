#!/usr/bin/python3
"""
A Fabric script that deletes out-of-date archives.
"""

from fabric.api import run, env, local, task, runs_once

env.hosts = ['52.86.25.3', '35.153.194.184']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


@runs_once
def remove_local(number):
    """Removes out-of-date local archives"""
    local("ls -dt versions/* | tail -n +{} | sudo xargs rm -fr".format(number))


@task
def do_clean(number=0):
    """Deletes out-of-date archives"""
    if int(number) == 0:
        number = 1

    # Ensure we keep at least the most recent version
    number = int(number) + 1

    # Delete archives locally
    remove_local(number)

    # Delete archives locally
    rem_path = "/data/web_static/releases/*"
    run("ls -dt {} | tail -n +{} | sudo xargs rm -fr".format(rem_path, number))
