# Fabfile to:
#    - update the remote system(s)
#    - download and install an application

# Import Fabric's API module
from fabric.api import *
from ProjectConfig import *


# Set the username
env.user   = "ubuntu"


def get_project():
    run("sudo apt-get install -y git")
    run("git clone https://github.com/chowmean/callosum.git")

def runn():
    # make_installs()
    # install_pip()
    #install_dependencies()
    with cd('callosum'):
        run('ls')
        run('python run.py')
