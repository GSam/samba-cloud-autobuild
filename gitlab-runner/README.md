# Ansible scripts for gitlab-runner

This dir contains all ansible scripts to set up and provision gitlab-runner.

# Prerequisites

1. Create ansible-venv for openstack:

    cd samba-cloud-autobuild
    scripts/install-ansible.sh
    source ansible-venv/bin/activate

This will create the ansible-venv dir in repo root, and activate it.

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
