#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import os
import re
import sys
from os.path import dirname, abspath, join
import time
import argparse
import tarfile
from datetime import datetime

from io import StringIO

HERE = abspath(dirname(__file__))

# use timestamp, then we don't override old data
# PREFIX = datetime.now().strftime('%Y%m%d%H%M%S')

MODEL = join(HERE, "{{model_file_name}}")

# data dir for this run
STATS_DIR_NAME = "{{stats_dir_name}}"
STATS_DIR = join(HERE, STATS_DIR_NAME)

os.system('mkdir -p {}'.format(STATS_DIR))

S_MAX = 60


CMD = """
script/traffic_replay -U Administrator%{{samba_password}}  \
--realm {{samba_realm}} \
--workgroup {{samba_domain|upper}} \
--fixed-password iegh1haevoofoo3looT9  \
-r {r} \
-S {S} \
--random-seed=1 \
-D 60 \
--debuglevel 0 \
{MODEL}  {{SAMBA_DC.name}}.{{samba_realm}} \
| tee {output}
"""


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_output_path(r, S):
    return join(STATS_DIR, 'r{:02}-S{:02}.txt'.format(r, S))


def replay():
    S = 3
    while S < S_MAX:
        for r in [1, 2, 5]:
            output = get_output_path(r, S)
            if os.path.exists(output):
                if 'Total conversations' in open(output, 'r').read():
                    print('skip {}'.format(output))
                    continue
                else:
                    os.remove(output)
            cmd = CMD.format(r=r, S=S, MODEL=MODEL, output=output)
            time.sleep(1)
            print(cmd)
            ret = os.system(cmd)
            if ret != 0:
                print('exit with cmd out put: {}'.format(ret))
                exit(ret)
        S = max(S * 6 // 5, S + 1)


# regex to extract number form file
EXTRACTORS = {
    # Total conversations:           92
    'total-conversations': 'Total conversations:\s+(\d+)',
    # Successful operations:        537 (9.071 per second)
    'successful-operations': 'Successful operations:\s+(\d+)\s+',
    'successful-operations-per-second': 'Successful operations:\s+\d+\s+\((\d+\.\d+) per second\)',
    # Failed operations:              0 (0.000 per second)
}


def extract_number(filepath, extractor='successful-operations-per-second'):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            text = f.read()
            pattern = EXTRACTORS[extractor]
            m = re.search(pattern, text)
            if m:
                return float(m.group(1))
    return 0.0


def summary():

    buf = StringIO()

    def _print(*args, **kwargs):
        # print to string io
        kwargs['file'] = buf
        print(*args, **kwargs)

    FILES = os.listdir(STATS_DIR)
    s_range = set()
    r_range = set()

    for fn in FILES:
        m = re.search(r'^r(\d+)-S(\d+).txt', fn)
        if m:
            r, S = m.group(1, 2)
            r_range.add(r)
            s_range.add(S)

    S_RANGE = sorted(int(s) for s in s_range)
    R_RANGE = sorted(int(r) for r in r_range)

    HEAD_FORMAT = '{:^5}'
    CELL_FORMAT = '{:>6}'

    _print(HEAD_FORMAT.format('r\S'), end='')

    for S in S_RANGE:
        _print(CELL_FORMAT.format(S), end='')

    _print('\n')

    max_number = 0.0
    errors = 0

    for r in R_RANGE:
        _print(HEAD_FORMAT.format(r), end='')
        for S in S_RANGE:
            output = get_output_path(r, S)
            n = extract_number(output)
            if n == 0.0:
                errors += 1
            if float(n) > max_number:
                max_number = float(n)
            n = '{:.1f}'.format(n)
            _print(CELL_FORMAT.format(n), end='')
        _print('\n')

    _print('\nmax: {}'.format(max_number))
    _print("errors: {}".format(errors))

    text = buf.getvalue()
    buf.close()
    print(text)

    # write summary to file
    txtname = os.path.join(STATS_DIR, 'summary.txt')
    with open(txtname, 'w') as txt:
        txt.write(text)

    # make a tarfile for stats dir
    tarname = '{}.tgz'.format(STATS_DIR)
    with tarfile.open(tarname, 'w:gz') as tar:
        tar.add(STATS_DIR, arcname=STATS_DIR_NAME)


def main():

    parser = argparse.ArgumentParser(
        description='Run traffic replay against DC')

    parser.add_argument(
        '-r', '--replay', action='store_true',
        help='run traffic replay')

    parser.add_argument(
        '-s', '--summary', action='store_true',
        help='get traffic summary')

    parser.add_argument(
        '-a', '--all', action='store_true',
        help='run replay and get summary')

    args = parser.parse_args()

    has_task = False
    if args.all or args.replay:
        replay()
        has_task = True
    if args.all or args.summary:
        summary()
        has_task = True

    if not has_task:
        parser.print_help()


if __name__ == '__main__':
    main()
