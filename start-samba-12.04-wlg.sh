#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc-wlg.sh
#c1.c4r4 2772d378-c1c3-464c-83b9-1a2d00d1b66b
nova boot --flavor=2772d378-c1c3-464c-83b9-1a2d00d1b66b --image=ubuntu-12.04-x86_64 --user-data user-config-12.04.yaml --config-drive true --key-name=abartlet --poll samba-build-$1
