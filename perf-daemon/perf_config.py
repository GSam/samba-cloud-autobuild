# This is where we keep constant values shared between the web
# interface and the daemon.

import os

HERE = os.path.dirname(__file__)
QUEUE_DIR = os.environ.get('PERF_TEST_QUEUE_DIR',
                           os.path.join(HERE, 'perf-queue'))
SUCCESS_DIR = os.environ.get('PERF_TEST_SUCCESS_DIR',
                             os.path.join(HERE, 'perf-queue-done'))
FAIL_DIR = os.environ.get('PERF_TEST_FAIL_DIR',
                          os.path.join(HERE, 'perf-queue-fail'))

RESULT_DIR = os.environ.get('PERF_RESULT_DIR',
                            os.path.join(HERE, 'perf-results'))

MULTI_PERF_SCRIPT = os.path.join(HERE, '../scripts/multi-perf-test')
GRAPH_SCRIPT = os.path.join(HERE, '../scripts/graph-perf-json')

WEB_USER_HOME = os.environ.get('HOME')
TEMP_DIR = os.environ.get('PERF_TEMP_DIR',
                          os.path.join(WEB_USER_HOME, 'temp'))

CURRENT_STATE_FILE = os.environ.get('PERF_CURRENT_STATE_FILE',
                                    os.path.join(TEMP_DIR, 'current_state'))


EMAIL_RECIPIENT = 'samba-dev@catalyst.net.nz'
EMAIL_SERVER = 'smtp1.catalyst.net.nz'

TEMPLATE_DIR = os.path.join(HERE, 'templates')

