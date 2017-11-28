#!/usr/bin/env python
import pexpect

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("host", help="Windows host")
parser.add_argument("username", help="Username to ssh to windows")
parser.add_argument("password", help="Password to ssh to windows")

args = parser.parse_args()

cmd = 'ssh {}@{}'.format(args.username, args.host)
child = pexpect.spawn(cmd)
child.expect('password: ')
child.sendline(args.password)
child.expect('> ')
child.sendline('echo hello')
child.expect('> ')
print child.before
