import argparse

import xml.etree.ElementTree as ET
from dateutil import parser


parser = argparse.ArgumentParser()

parser.add_argument(
    "--trx",
    default='/tmp/testresult.trx',
    help="path to trx file"
)

parser.add_argument(
    "--test-suite",
    default='Kerberos',
    help="Test Suite name"
)

args = parser.parse_args()

xml = ET.fromstring(open(args.trx, 'r').read())

ns = "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"
entries = dict((x.tag[len('{%s}' % ns):], x) for x in xml)

print_xml = ['Times', 'ResultSummary']
mapping = {'Failed': 'failure', 'Passed': 'success'}
test_mapping = {'Failed': 'failure', 'Passed': 'successful'}

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
        print parser.parse(result.attrib['startTime']).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')

        test = '%s.%s' % (testsuites[result.attrib['testId']][1], result.attrib['testName'])
        print 'test: ', test

        print ET.tostring(result.find('ns:Output/ns:StdOut', namespaces={'ns': ns}),
                          method='text').strip() + '\n'

        print parser.parse(result.attrib['endTime']).strftime('time: %Y-%m-%d %H:%m:%S.%fZ')

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
print 'testsuite-%s:' % mapping[entries['ResultSummary'].attrib['outcome']], FIXED
