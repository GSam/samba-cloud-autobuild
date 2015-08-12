"""These bits are shared between start-samba and multi-samba"""
import os
import sys
import subprocess
import tempfile
import random
import re

try:
    from pipes import quote
except ImportError:
    from shlex import quote


HERE = os.path.dirname(__file__)
YAML_DIR = os.path.join(HERE, 'yaml')

OPENRC_TABLE = {
    # listing both our short names, and the official names in case we
    # ever use those.
    'por':      '~/sambatest.catalyst.net.nz-openrc.sh',
    'nz-por-1': '~/sambatest.catalyst.net.nz-openrc.sh',
    'wlg':      '~/sambatest.catalyst.net.nz-openrc-wlg.sh',
    'nz_wlg_2': '~/sambatest.catalyst.net.nz-openrc-wlg.sh'
}

SERVER_NAME = "samba-build-%s-%s"

def get_credentials(region, no_secrets=False):
    """Get the credentials for the region ('wlg' or 'por')"""
    credentials_file = OPENRC_TABLE[region]
    env = subprocess.check_output(['bash', '-c', 'source %s && env' %
                                   credentials_file], env={})
    credentials = dict(x.strip().split('=', 1) for x in env.split("\n")
                       if x.startswith('OS_'))

    if no_secrets:
        # There is no point preserving any of the credential
        # variables, even though most are not really secret -- they
        # are only useful in conjunction with the password.
        credentials = {k: '' for k, v in credentials.items()}

    return credentials

def get_package_list(name, form=str):
    fn = os.path.join(HERE, 'package-lists', name)
    f = open(fn)
    if form is str:
        packages = f.read()
    elif form is list:
        packages = [x[3:].strip() for x in f if x[:3] == ' - ']
    f.close()
    return packages


def run_nova_cmd(args, region="por", dry_run=False):
    open_rc = OPENRC_TABLE[region]
    args = ['.', open_rc, ';', 'nova'] + [quote(x) for x in args]
    str_args = ' '.join(args)
    if dry_run:
        return str_args
    return subprocess.check_output(str_args, shell=True)


def add_common_args(parser):
    default_server_suffix = "%s-%04d" % (os.environ.get('USER'),
                                         random.randint(0, 9999))
    parser.add_argument('suffix', nargs='?',
                        default=default_server_suffix,
                        help="name the server with this suffix")

    parser.add_argument('--whole-name', action='store_true',
                        help="use the 'suffix' as the whole name")

    parser.add_argument('--key-name', default=os.environ.get('USER'),
                        help="use this ssh key pair")

    parser.add_argument('-i', '--image', default="samba-build-14.04-template",
                        help="specify the image to use")

    parser.add_argument('-f', '--flavor', default='c1.c2r4',
                        help=("specify which flavour to use "
                              "(default: 2 CPUs, 4GB)"))

    parser.add_argument('--region', default="por",
                        help="'wlg' or 'por' (default 'por')")

    parser.add_argument('-b', '--branch', default='master',
                        help="git branch to use")

    parser.add_argument('-r', '--remote',
                        default='git://git.catalyst.net.nz/samba.git',
                        help="git remote to use")

    parser.add_argument('--image-list', action='store_true',
                        help="list the available images, and exit")

    parser.add_argument('--flavor-list', action='store_true',
                        help="list the available flavours, and exit")

    parser.add_argument('-n', '--dry-run', action='store_true',
                        help="do nothing remotely, "
                        "show the nova command that would be run")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="say a litle more about what is happening")

    parser.add_argument('--onfail', default="delete",
                        help=("One of 'suspend|shelve|continue|"
                              "delayed-delete|delete' (default 'delete')"))

    parser.add_argument('--readahead', default=8192, type=int,
                        help=("block device readahead (default 8192)"))

    parser.add_argument('--maxtime', default=10000, type=int,
                        help=("how long to wait before timing out"))

    parser.add_argument('--tmpfs', action='store_true',
                        help=("run autobuild in a tmpfs (use 8GB RAM)"))

    parser.add_argument('--skip-samba-build', action='store_true',
                        help=("prepare the image for autobuild, then stop"))

    parser.add_argument('--no-secrets', action='store_true',
                        help=("don't upload nova password; instance won't "
                              "delete/suspend/shelve itself"))


def process_common_args(args):
    if args.dry_run:
        print " This is what we WOULD be doing without -n/--dry-run:\n"

    for nova_cmd in ("image_list",
                     "flavor_list"):
        if vars(args)[nova_cmd]:
            print(run_nova_cmd([nova_cmd.replace('_', '-')],
                               region=args.region, dry_run=args.dry_run))
            sys.exit()


def sanitise_hostname(hostname):
    fixed_name = re.sub(r'[^a-z0-9-]+', '-', hostname.lower())
    if fixed_name != hostname:
        print >> sys.stderr, ("WARNING: the host name '%s' contains invalid characters. "
                              " Using '%s' instead." % (hostname, fixed_name))
    return fixed_name
