#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc.sh
nova boot --flavor=c093745c-a6c7-4792-9f3d-085e7782eca6 --image=ubuntu-14.04-x86_64 --user-data user-config.yaml --config-drive true --key-name=abartlet --poll samba-build-$1
