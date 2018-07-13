#!/bin/bash

BASE_URL=https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory

FILES=(
    'rax.py'
    'openstack_inventory.py'
)

for file in ${FILES[@]}
do
    wget ${BASE_URL}/${file} -O ${file}
    chmod a+x ${file}
done
