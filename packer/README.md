# Ansible Project: Packer

1. Create a virtualenv, and install requirements:

    pip install -U -r ../requirements.txt

2. Source your Openstack RC file:

    source ~/sambatest.catalyst.net.nz-openrc.sh

3. Usage:

    ./build-ubuntu-1604.yml
    ./build-ubuntu-1804.yml
    ./build-windows.yml

Default output image will be `packer-{{OS_IMAGE_NAME}}`, to override:

    ./build-ubuntu-1604.yml -e PACKER_OUTPUT_IMAGE_NAME=samba-build-16.04-template
