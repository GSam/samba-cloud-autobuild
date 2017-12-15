#!/usr/bin/env python
import sys
import argparse
import time

from pexpect import pxssh
from pexpect.exceptions import TIMEOUT


def main():
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

    s.sendline('cd C:\\')
    s.prompt()

    s.sendline(r'start run.cmd')
    retry = 20
    while retry > 0:
        s.sendline('dir *.trx')
        s.prompt()
        print(s.before)
        if 'testresult.trx' not in s.before:
            print('retry: {}'.format(retry))
            time.sleep(30)
            retry -= 1
        else:
            break
    if retry < 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
