#!/usr/bin/python
import random, re
import os, sys
import tempfile
import shutil
from collections import defaultdict
import time

from flask import Flask, render_template, request, make_response

HERE = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(HERE, 'templates')

QUEUE_DIR = os.environ.get('PERF_TEST_QUEUE_DIR',
                           os.path.join(HERE, 'perf-queue'))

app = Flask(__name__)#, template_folder=TEMPLATE_DIR)

def always(x):
    return True

def true_or_false(x, default=None):
    if isinstance(x, bool):
        return x
    x = x.lower()
    if x in ('true', 'yes', '1'):
        return True
    if x in ('false', 'no', '0'):
        return False
    return default

@app.route('/', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        get = request.form.get
    else:
        get = request.args.get

    validators = {
        'remote': ["http://git.catalyst.net.nz/samba.git",
                   "git://git.catalyst.net.nz/samba.git",
                   "git://git.samba.org/samba.git",
                   "git://git.samba.org/abartlet/samba.git",
                   "git://git.samba.org/garming/samba.git",
                   "https://github.com/douglasbagnall/samba.git",
                   "https://github.com/gsam/samba.git",
                   "/home/samba-test-bot/samba-mirror.git"].__contains__,
        'job-name': re.compile(r'^[{}\w -]+$').match,
        'commits': re.compile(r'^[\w/^~. -]*$').match,
        'testregex': re.compile(r'^[^\n]*$').match,
        'bestof': re.compile(r'^\d+$').match,
        'response-type': ['text', 'html'].__contains__,
        'preserve-tmp-dir': ['yes', 'no'].__contains__,
        'graphs': ['yes', 'no'].__contains__,
    }

    def validate(k, default=None):
        v = get(k)
        if v is not None and validators[k](v):
            return v
        return default

    job_name = validate('job-name',
                        'Performance test at {now} on commits {commits}, '
                        'using tests matching "{tests}"')
    remote = validate('remote')
    commits = validate('commits')
    testregex = validate('testregex', '')
    bestof = validate('bestof', '3')
    response_type = validate('response-type', 'html')
    preserve_tmp_dir = true_or_false(validate('preserve-tmp-dir', False))
    graphs = true_or_false(validate('graphs', False))

    missing = ' and '.join(k for k, v in
                           [('remote', remote),
                            ('commits', commits)]
                           if not v)
    if missing:
        msg = 'You need to provide %s' % missing
        if response_type == 'text':
            return msg
        return render_template('perf-queue-add.html', msg=msg)

    job_name = job_name.format(now=time.strftime('%Y-%m-%d %H:%M:%S'),
                               commits=commits,
                               tests=testregex)


    fh, fn = tempfile.mkstemp(prefix='job-', dir=QUEUE_DIR)
    f = open(fn, 'w')
    os.close(fh)
    print >> f, 'title: ', job_name
    print >> f, '\n# options'
    print >> f, '-r', remote
    print >> f, '-t', testregex
    print >> f, '--best-of', bestof
    if preserve_tmp_dir:
        print >> f, '--preserve-tmp-dir'
    print >> f, '\n# meta-options'
    print >> f, 'graphs:', graphs
    print >> f, '\n# commits'
    print >> f, commits
    f.close()

    msg = 'job submitted (id %s)' % os.path.basename(fn)

    if response_type == 'text':
        return msg

    return render_template('perf-queue-add.html', msg=msg,
                           job_name=job_name,
                           commits=commits, remote=remote,
                           testregex=testregex, bestof=bestof,
                           preserve_tmp_dir=preserve_tmp_dir,
                           graphs=graphs)


@app.route('/list', methods=['GET', 'POST'])
def list_jobs():
    jobs = []
    for fn in os.listdir(QUEUE_DIR):
        ffn = os.path.join(QUEUE_DIR, fn)
        f = open(ffn)
        s = f.read()
        f.close()
        m = re.search(r'title:(.+)', s)
        if m:
            title = m.group(1)
        else:
            title = '[untitled]'

        jobs.append((fn, title, s))

    return render_template('perf-queue-list.html', jobs=jobs)


def main():
    global QUEUE_DIR
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--world-visible', action='store_true',
                        help='Allow connections from beyond localhost')
    parser.add_argument('-p', '--port', default=5000, type=int,
                        help='listen on this port')
    parser.add_argument('-q', '--queue-dir', default=QUEUE_DIR,
                        help='save queued jobs here')
    args = parser.parse_args()

    QUEUE_DIR = args.queue_dir

    try:
        if not args.world_visible:
            app.run(debug=True, port=args.port)
        else:
            app.run(host='0.0.0.0', port=args.port)
    except Exception, e:
        import traceback
        print(traceback.format_exc())
        print >>sys.stderr, e


if __name__ == '__main__':
    main()
