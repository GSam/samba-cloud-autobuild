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

FIXED = 'Microsoft.Protocol.TestSuites.Kerberos'

for x in print_xml:
    print ET.tostring(entries[x])

testsuites = {}
for test in entries['TestDefinitions']:
    testsuites[test.attrib['id']] = test
    for test_method in test.findall('ns:TestMethod',
                                    namespaces={'ns': ns}):
        testsuites[test.attrib['id']] = (test, test_method.attrib['className'])
        break

print 'testsuite:', FIXED
print parser.parse(entries['Times'].attrib['start']).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')
print 'progress: push'
for result in entries['Results']:
    if result.tag.endswith('UnitTestResult'):
        start_time = result.attrib.get('startTime')
        if start_time:
            print parser.parse(start_time).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')

        test = '%s.%s' % (testsuites[result.attrib['testId']][1], result.attrib['testName'])
        print 'test: ', test

        out = result.find('ns:Output/ns:StdOut', namespaces={'ns': ns})
        if out:
            print ET.tostring(out, method='text').strip() + '\n'

        end_time = result.attrib.get('endTime')
        if end_time:
            print parser.parse(end_time).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')

        error = result.find('ns:Output/ns:ErrorInfo', namespaces={'ns': ns})
        if error is not None:
            print '%s: %s [\n%s\n]\n' % (test_mapping[result.attrib['outcome']],
                                         test, ET.tostring(error, method='text'))
        else:
            print '%s: %s' % (test_mapping[result.attrib['outcome']], test)
    else:
        print ET.tostring(result, method='text').strip() + '\n'

print parser.parse(entries['Times'].attrib['finish']).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')
print 'progress: pop'
print entries
outcome = entries['ResultSummary'].attrib.get('outcome', 'None')
print 'testsuite-%s:' % mapping.get(outcome, ''), FIXED
