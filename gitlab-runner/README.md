# Ansible scripts for gitlab-runner

This dir contains all ansible scripts to set up and provision gitlab-runner.

# Prerequisites

1. Download this script to create ansible-venv for openstack:

    wget https://github.com/catalyst/catalystcloud-ansible/blob/master/install-ansible.sh
    ./install-ansible.sh

2. Source your openstack rc file

If you don't have it yet, download it from openstack dashboard site. Then:

    source ~/sambatest.catalyst.net.nz-openrc.sh

# Run playbook
To create network, server and provision gitlab-runner:

    cd gitlab-runner
    ansible-playbook main.yml

It's important to cd into gitlab-runner dir. Thus ansible will read the ansible.cfg file
in there, and load dynamic inventory in inventory/openstack.py.

To create networking only:

    ansible-playbook networking.yml

To provision gitlab-runner only:

    ansible-playbook provisioning.yml

# Build docker image

    ansible-playbook build-docker-image.yml

This script just render a Dockerfile in /tmp/ and build the image locally.
To push it to registry, follow the instructions at the end of playbook.
