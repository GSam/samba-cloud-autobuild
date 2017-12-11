#!/usr/bin/python
import argparse
import os
import sys
import subprocess
import tempfile
import random
from string import Template

from common import get_credentials, get_package_list, DEFAULT_REGION, OPENRC_TABLE, SambaCloudError

try:
    from pipes import quote
except ImportError:
    from shlex import quote

HERE = os.path.dirname(__file__)

PACKER_TEMPLATE = os.path.join(HERE, 'config.json')
CLOUD_INIT_TEMPLATE = os.path.join(HERE, 'user_data.ps1')


def write_cloud_init(password=None):
    with open(CLOUD_INIT_TEMPLATE) as f:
        s = f.read()

    f = tempfile.NamedTemporaryFile(suffix='.ps1',
                                    prefix='build-windows-image-',
                                    delete=False)
    f.write(Template(s).substitute(password=password))
    f.close()
    return f.name


def run_packer(packer_file, region, dry_run=False):
    cmd = '. {}; packer build {}'.format(OPENRC_TABLE[region], packer_file)
    print(cmd)
    if not dry_run:
        subprocess.check_call(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser()
    password = subprocess.check_output("pwgen -s 20", shell=True)[:20]

    parser.add_argument('--region', default=DEFAULT_REGION,
                        help="'wlg' or 'por' (default '%s')" % DEFAULT_REGION)

    parser.add_argument('-i', '--image',
                        # packer must use snapshot to create windows instance, refer to:
                        # http://docs.catalystcloud.io/tutorials/using-packer-to-build-custom-bootable-images-on-the-catalyst-cloud.html#using-packer-with-windows-on-the-catalyst-cloud
                        default="windows-server-2012r2-x86_64-live-snapshot",
                        help="specify the image to use")

    parser.add_argument('--net-id',
                        default="4d98cbab-9f97-4103-997c-207571127b1f",  # Samba Team Test
                        help=("Use net with this UUID (lauto to search for a good one)"))

    parser.add_argument('--verbose-logs', action='store_true',
                        help=("run packer --verbose"))

    parser.add_argument('--use-default-pass', action='store_true', default=True,
                        help=("use a default (insecure) password for machines and samba"))

    parser.add_argument('-n', '--dry-run', action='store_true',
                        help="do nothing remotely, "
                        "show the command that would be run")
    parser.add_argument('-f', '--flavor', default='c1.c2r4',
                        help=("specify which flavour to use "
                              "(default: 2 CPUs, 4GB)"))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="say a litle more about what is happening")

    parser.add_argument('--ms-downloads',
                        help="directory of dependency files(vstf_testagent.exe)")

    args = parser.parse_args()

    if args.use_default_pass:
        password = "Password01@"
    else:
        password = subprocess.check_output("pwgen -s 20", shell=True)[:20]

    os.environ['PACKER_PASSWORD'] = password
    os.environ['PACKER_USER_DATA_FILE'] = write_cloud_init(password=password)
    os.environ['PACKER_IMAGE'] = args.image
    os.environ['PACKER_FLAVOR'] = args.flavor
    os.environ['PACKER_NET_ID'] = args.net_id
    os.environ['PACKER_MS_DOWNLOADS'] = args.ms_downloads.rstrip('/')

    run_packer(PACKER_TEMPLATE, args.region, args.dry_run)


main()