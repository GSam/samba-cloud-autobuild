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

    s.sendline('del testresult.trx')
    s.prompt()

    s.sendline('start run.cmd')
    s.prompt()

    timelapse = 0
    timeout = 10 * 60
    while timelapse <= timeout:
        s.sendline('dir *.trx')
        s.prompt()
        print(s.before)
        if 'File Not Found' in s.before:
            print('waiting for testresult.trx, timelapse/timeout: {}/{} seconds'.format(timelapse, timeout))
            time.sleep(30)
            timelapse += 30
        elif 'testresult.trx' in s.before:
            print('found testresult.trx, timelapse: {} seconds'.format(timelapse))
            break
    ret = 0 if timelapse <= timeout else 1
    sys.exit(ret)


if __name__ == '__main__':
    main()