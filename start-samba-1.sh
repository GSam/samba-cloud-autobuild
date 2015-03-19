#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc.sh
#c1.c2r4 c093745c-a6c7-4792-9f3d-085e7782eca6
#c1.c4r8 45060aa3-3400-4da0-bd9d-9559e172f678
nova boot --flavor=45060aa3-3400-4da0-bd9d-9559e172f678 --image=ubuntu-14.04-x86_64 --user-data user-config.yaml --config-drive true --key-name=abartlet --poll samba-build-$1
