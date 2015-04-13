#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc-wlg.sh
nova boot --flavor=c1.c2r2 --image=ubuntu-14.04-x86_64 --user-data user-config.yaml --config-drive true --key-name=abartlet --poll samba-build-$1
