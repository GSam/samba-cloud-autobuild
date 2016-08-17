import os
import sys
import mailbox
import argparse
import re
import requests
import errno
import collections
import time

import config


def filter_by_date(files, date):
    date_search = re.compile(r'(20\d\d-\d\d-\d\d)-').search
    out = []
    threshold = time.mktime(time.strptime(date, '%Y-%m-%d'))
    for fn in files:
        m = date_search(fn)
        if m:
            t = time.mktime(time.strptime(m.group(1), '%Y-%m-%d'))
            if t > threshold:
                out.append(fn)
    return out


def count_lines(fn_re, line_re, cache, count=None, since=None, filter_re=None):
    fn_match = re.compile(fn_re).search
    line_match = re.compile(line_re).search
    files = sorted(x for x in os.listdir(cache) if fn_match(x))
    if since:
        files = filter_by_date(files, since)

    lines = []
    for fn in files:
        f = open(os.path.join(cache, fn))
        for line in f:
            if line_match(line):
                lines.append(line.strip())
        f.close()

    if filter_re is not None:
        filter_match = re.compile(filter_re).search
        lines = [' '.join(filter_match(x).groups()) for x in lines
                 if filter_match(x)]

    print ("found %d lines matching %r in %d files matching %r" %
           (len(lines), line_re, len(files), fn_re))

    c = collections.Counter(lines)
    if count:
        rows = c.most_common(count)
    else:
        rows = c.most_common()
    for k, v in rows:
        print '%4d %s' % (v, k)


def group_by_month(files):
    date_search = re.compile(r'(20\d\d-\d\d)-\d\d-').search
    out = {}
    for fn in files:
        m = date_search(fn)
        if m:
            out.setdefault(m.group(1), []).append(fn)
    return out


def draw_histogram(fn_re, line_re, cache, since=None, filter_re=None):
    fn_match = re.compile(fn_re).search
    line_match = re.compile(line_re).search
    files = sorted(x for x in os.listdir(cache) if fn_match(x))
    if since:
        files = filter_by_date(files, since)

    months = group_by_month(files)
    month_lines = []
    longest = 0
    for month, filenames in months.iteritems():
        lines = []
        for fn in filenames:
            f = open(os.path.join(cache, fn))
            for line in f:
                if line_match(line):
                    lines.append(line.strip())
            f.close()

        if filter_re is not None:
            filter_match = re.compile(filter_re).search
            lines = [' '.join(filter_match(x).groups()) for x in lines
                     if filter_match(x)]

        month_lines.append((month, lines))
        if len(lines) > longest:
            longest = len(lines)

    month_lines.sort()
    for month, lines in month_lines:
        x = len(lines)
        if longest > 72:
            x = x * 72 // longest

        print '%s %3d %s' % (month, len(lines), '#' * x)
