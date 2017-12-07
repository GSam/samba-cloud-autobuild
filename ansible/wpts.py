#!/usr/bin/env python
import sys
import argparse

from pexpect import pxssh


parser = argparse.ArgumentParser()

parser.add_argument("hostname", help="Windows hostname")
parser.add_argument("username", help="Windows Domain User username")
parser.add_argument("password", help="Windows Domain User Password")

args = parser.parse_args()

s = pxssh.pxssh(
    echo=True,
    options={
        "StrictHostKeyChecking": "no",
    }
)
s.PROMPT = '[>]'

s.login(
    args.hostname,
    args.username,
    password=args.password,
    original_prompt='[>]',
    auto_prompt_reset=False,
)

s.sendline('C:\wpts-run-kerberos.bat')
s.expect('Results file:')
# print(s.before)
# s.logout()  # will timeout

sys.exit(0)
