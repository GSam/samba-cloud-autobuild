#!/bin/bash -x

export ANSIBLE_INVENTORY=../inventory/openstack_inventory.py

ansible-playbook main.yml \
    -e MACHINE_DRIVER=openstack \
    -e REMOTE_USER=ubuntu \
    -vv "$@"
