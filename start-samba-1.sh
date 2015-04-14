#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc.sh
#c1.c2r4 c093745c-a6c7-4792-9f3d-085e7782eca6
#c1.c4r8 45060aa3-3400-4da0-bd9d-9559e172f678
#c1.c4r4 62473bef-f73b-4265-a136-e3ae87e7f1e2
nova boot --flavor=62473bef-f73b-4265-a136-e3ae87e7f1e2 --image=samba-build-14.04-template --user-data user-config.yaml --config-drive true --key-name=abartlet --poll samba-build-$1
