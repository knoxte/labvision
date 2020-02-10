# labvision
Repository for managing images, videos and cameras

## Installation from github
    pip install git+https://github.com/MikeSmithLabTeam/labvision
    
## Updating if already installed
    pip install --upgrade git+https://github.com/MikeSmithLabTeam/labvision
    
## To add as a dependency to another pip repository
Add the following argument to setup.py setuptools.setup()

    dependency_links=['https://github.com/MikeSmithLabTeam/labvision/tarball/repo/master#egg=package-1.0'],
