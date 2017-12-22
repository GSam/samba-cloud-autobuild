#!/usr/bin/env python
import argparse

import xml.etree.ElementTree as ET
from dateutil import parser


p = argparse.ArgumentParser()

p.add_argument(
    "--trx",
    default='/tmp/testresult.trx',
    help="path to trx file"
)

p.add_argument(
    "--test-suite",
    default='Kerberos',
    help="Test Suite name"
)

args = p.parse_args()

xml = ET.fromstring(open(args.trx, 'r').read())

ns = "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"
entries = dict((x.tag[len('{%s}' % ns):], x) for x in xml)

print_xml = ['Times', 'ResultSummary']
mapping = {'Failed': 'failure', 'Passed': 'success'}
test_mapping = {
    'Failed': 'failure',
    'Passed': 'successful',
    'Inconclusive': 'Inconclusive',
    'NotExecuted': 'NotExecuted',
}

FIXED = 'Microsoft.Protocol.TestSuites.{}'.format(args.test_suite)

for x in print_xml:
    print ET.tostring(entries[x])

unit_tests = {}
for test in entries['TestDefinitions']:
    test_guid = test.attrib['id']
    unit_tests[test_guid] = test
    for test_method in test.findall('ns:TestMethod', namespaces={'ns': ns}):
        class_name = test_method.attrib['className'].split(',')[0]
        unit_tests[test_guid] = (test, class_name)
        break

print 'testsuite:', FIXED
print parser.parse(entries['Times'].attrib['start']).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')
print 'progress: push'
for result in entries['Results']:
    if result.tag.endswith('UnitTestResult'):
        start_time = result.attrib.get('startTime')
        if start_time:
            print parser.parse(start_time).strftime('startTime: %Y-%m-%d %H:%m:%S.%fZ')

        test = '%s.%s' % (unit_tests[result.attrib['testId']][1], result.attrib['testName'])
        print 'test: ', test

        out = result.find('ns:Output/ns:StdOut', namespaces={'ns': ns})
        if out is not None:
            print ET.tostring(out, method='text').strip() + '\n'
            pass

        end_time = result.attrib.get('endTime')
        if end_time:
            print parser.parse(end_time).strftime('endTime: %Y-%m-%d %H:%m:%S.%fZ')

        error = result.find('ns:Output/ns:ErrorInfo', namespaces={'ns': ns})
        if error is not None:
            print '%s: %s \n[\n%s\n]\n' % (test_mapping[result.attrib['outcome']],
                                         test, ET.tostring(error, method='text'))
        else:
            print '%s: %s' % (test_mapping[result.attrib['outcome']], test)
    else:
        print ET.tostring(result, method='text').strip() + '\n'

print parser.parse(entries['Times'].attrib['finish']).strftime('finish time: %Y-%m-%d %H:%m:%S.%fZ')
print 'progress: pop'
outcome = entries['ResultSummary'].attrib.get('outcome', 'None')
print 'testsuite-{}: {}'.format(mapping.get(outcome, outcome), FIXED)

counters = entries['ResultSummary'].find('ns:Counters', namespaces={'ns': ns})
for k, v in counters.attrib.items():
    print('{}: {}'.format(k, v))
