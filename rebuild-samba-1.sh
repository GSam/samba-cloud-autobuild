#!/bin/bash
. ~/sambatest.catalyst.net.nz-openrc.sh
nova rebuild samba-build-$1 ubuntu-14.04-x86_64
