#!/usr/bin/python
import re
import os, sys
import tempfile
from collections import Counter
import time
import json

from flask import Flask, render_template, request, make_response
from perf_config import HERE, QUEUE_DIR, TEMPLATE_DIR, CURRENT_STATE_FILE

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


def get_get(r):
    if r.method == 'POST':
        return request.form.get
    return r.args.get


@app.route('/', methods=['GET', 'POST'])
def add_job():
    get = get_get(request)

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
    print >> f, '--test-regex', testregex
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


def read_current_state():
    try:
        f = open(CURRENT_STATE_FILE)
    except IOError as e:
        print >> sys.stderr, "could not read curent_state; guessing no jobs."
        return None, None, None, None, None
    state = f.read().strip().split('\n')
    f.close()
    return state


class Namespace(object):
    pass


def get_progress_report(job_id, output_dir, workdir):
    progress = Namespace()
    progress.percent = 0
    progress.rounds = 0
    progress.target_rounds = 0
    progress.comment = ''
    result_file = os.path.join(output_dir, 'results.json')
    job_file = os.path.join(QUEUE_DIR, job_id)
    try:
        f = open(result_file)
        results = json.load(f)
        f.close()
    except (ValueError, OSError) as e:
        print >> sys.stderr, e
        results = None

    try:
        f = open(job_file)
        for line in f:
            m = re.match(r'^--best-of\s+(\d+)', line)
            if m is not None:
                progress.target_rounds = int(m.group(1))
        f.close()
    except OSError as e:
        print >> sys.stderr, e

    if results:
        all_commits = [x[0] for x in results]
        c = Counter(all_commits).most_common()
        if not c:
            progress.comment = 'no results!'
            return progress
        progress.rounds = c[0][1]
        if c[-1][1] != progress.rounds:
            progress.comment = 'flakey results (%s run %d times)' % c[-1]

        if progress.target_rounds:
            progress.percent = progress.rounds * 100 // progress.target_rounds

    return progress


@app.route('/list', methods=['GET', 'POST'])
def list_jobs():
    mode, job_id, output_dir, workdir, pid = read_current_state()

    jobs = []
    filenames = os.listdir(QUEUE_DIR)

    for fn in filenames:
        ffn = os.path.join(QUEUE_DIR, fn)
        f = open(ffn)
        s = f.read()
        f.close()
        m = re.search(r'title:(.+)', s)
        if m:
            title = m.group(1)
        else:
            title = '[untitled]'

        if mode == 'queue' and job_id == fn:
            progress = get_progress_report(job_id, output_dir, workdir)
            dest_dir = output_dir
        else:
            dest_dir = None
            progress = None

        jobs.append((fn, title, s, dest_dir, progress))

    if job_id not in filenames:
        jobs.append((job_id, "a background test", "", output_dir, None))

    return render_template('perf-queue-list.html', jobs=jobs)



@app.route('/results.json', methods=['GET', 'POST'])
def results_json():
    mode, current_job, output_dir, workdir, pid = read_current_state()
    f = open(os.path.join(output_dir, 'results.json'))
    s = f.read()
    f.close()
    response = make_response(s)
    response.mimetype = 'application/json'
    return response


@app.route('/details', methods=['GET', 'POST'])
def details_of_active_job():
    #get = get_get(request)
    #job = get('job')
    #mode, current_job, output_dir, workdir, pid = read_current_state()
    #if current_job != job:
    #    return "no"

    return render_template('perf-job-details.html',
                           url='/results.json')



@app.route('/cancel', methods=['GET', 'POST'])
def cancel_queued_job():
    get = get_get(request)
    job = get('job')
    mode, current_job, output_dir, workdir, pid = read_current_state()
    messages = []
    if job in os.listdir(QUEUE_DIR):
        try:
            os.unlink(os.path.join(QUEUE_DIR, job))
            messages.append("removed from the queue!")
        except OSError as e:
            messages.append("no such job: %s" % e)

    if job == current_job:
        for k in (15, 15, 9):
            try:
                os.kill(int(pid), k)
                time.sleep(1)
            except OSError as e:
                if e.errno == 3:
                    messages.append("killed the controlling process")
                    break
                raise

    return "\n".join(messages)


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
