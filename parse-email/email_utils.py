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
from collections import Counter

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


def count_lines(fn_re, line_re, cache, count=None, since=None, filter_re=None,
                included_set=None):
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

    if included_set is not None:
        lines = [x for x in lines if x in included_set]

    print ("found %d lines matching %r in %d files matching %r" %
           (len(lines), line_re, len(files), fn_re))

    c = collections.Counter(lines)
    if count:
        return c.most_common(count)

    return c.most_common()


def group_by_month(files):
    date_search = re.compile(r'(20\d\d-\d\d)-\d\d-').search
    out = {}
    for fn in files:
        m = date_search(fn)
        if m:
            out.setdefault(m.group(1), []).append(fn)
    return out


def get_files_by_month(fn_re, cache, since):
    fn_match = re.compile(fn_re).search
    files = sorted(x for x in os.listdir(cache) if fn_match(x))
    if since:
        files = filter_by_date(files, since)
    months = group_by_month(files)
    return months


def get_errors_by_month(fn_re, line_re, cache, since=None, filter_re=None):
    line_match = re.compile(line_re).search
    months = get_files_by_month(fn_re, cache, since)
    recent_lines = get_files_by_month(fn_re, cache, since)
    recent_lines = set()

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

    return month_lines


def draw_histogram(fn_re, line_re, cache, since=None, filter_re=None):
    month_lines = get_errors_by_month(fn_re,
                                      line_re,
                                      cache,
                                      since=since,
                                      filter_re=filter_re)
    longest = 1
    for month, lines in month_lines:
        if len(lines) > longest:
            longest = len(lines)

    month_lines.sort()
    for month, lines in month_lines:
        x = len(lines)
        if longest > 72:
            x = x * 72 // longest

        print '%s %3d %s' % (month, len(lines), '#' * x)


TIME_MATCH = r'/\d+ at (\d+h)?(\d+m)?(\d+s)\] '


def draw_runtime_histogram(fn_re, cache, since, line_re=TIME_MATCH):
    months = get_files_by_month(fn_re, cache, since)
    line_match = re.compile(line_re).search
    month_times = []
    longest = 0
    for month, filenames in months.iteritems():
        times = []
        for fn in filenames:
            f = open(os.path.join(cache, fn))
            lines = reversed(f.readlines())
            for line in lines:
                m = line_match(line)
                if m:
                    g = m.groups()
                    t = 0
                    for x in g:
                        if x is None:
                            continue
                        d = int(x[:-1])
                        u = x[-1]
                        if u == 'h':
                            t += d * 3600
                        elif u == 'm':
                            t += d * 60
                        else:
                            t += d
                    times.append(t)
                    break
            f.close()

        month_times.append((month, times))

    month_times.sort()
    longest = 1
    for month, times in month_times:
        times.sort()
        longest = max(longest, times[-1])

    def s(t):
        return t * 73 // longest

    r = [' '] * 75
    for i in range(1 + longest // 3600):
        r[s(i * 3600)] = str(i)[-1]

    key = 'hours   ' + ''.join(r)
    print key

    # mark the extrema, quartiles and median
    for month, times in month_times:
        r = [' '] * 75
        r[s(times[0])] = '.'
        r[s(times[-1])] = '.'
        q1 = s(times[len(times) // 4])
        q3 = s(times[len(times) * 3 // 4])
        r[q1] = '|'
        r[q3] = '|'
        r[q1 + 1: q3] = ['-'] * (q3 - q1 - 1)
        r[s(times[len(times) // 2])] = '#'
        print month, ''.join(r)

    print key
    print "key: median #   interquartile range |-----|   extrema ."


def errors_since(fn_re, line_re, cache, since=None, filter_re=None):
    rows = count_lines(fn_re, line_re, cache, since=since, filter_re=None)
    return set(rows)


def recurring_errors(fn_re, line_re, cache, since=None, filter_re=None,
                     limit=2, included_set=None):

    month_lines = get_errors_by_month(fn_re,
                                      line_re,
                                      cache,
                                      since=since,
                                      filter_re=filter_re)
    c = Counter()

    for month, lines in month_lines:
        if included_set is not None:
            lines = [x for x in lines if x in included_set]

        c.update(set(lines))

    for err, count in c.most_common():
        if count < limit:
            break
        print "%-3d %s" % (count, err)
