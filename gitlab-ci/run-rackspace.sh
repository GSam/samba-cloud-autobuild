#!/bin/bash -x

export ANSIBLE_INVENTORY=../inventory/rax.py

ansible-playbook main.yml \
    -e MACHINE_DRIVER=rackspace \
    -e REMOTE_USER=root \
    -vv "$@"
