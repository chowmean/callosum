# Fabfile to:
#    - update the remote system(s)
#    - download and install an application

# Import Fabric's API module
from fabric.api import *
from ProjectConfig import *


env.hosts = [
    AWS_HOST,
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
]
# Set the username
env.user   = "ubuntu"

def list_file():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    run("ls -l")

def get_project():
    run("git clone git@github.com:chowmean/callosum.git")

def install_pip():
    run("wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9")
    run("tar -xvzf pip-9.0.1.tar.gz")
    run("cd pip-9.0.1")
    run("python setup.py install")

def make_installs():
    run("aptitude    update")
    run("aptitude -y upgrade")
    install_pip()
    get_project()

def run():
    run('cd callosum_automated')
    run('python run.py')
