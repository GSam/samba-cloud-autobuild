:: Copyright (c) Microsoft. All rights reserved.
:: Licensed under the MIT license. See LICENSE file in the project root for full license information.

@echo off

echo ==============================================
echo          Start to run Kerberos all test cases
echo ==============================================

del {{test_result_file}} >nul 2>&1

"{{MSTEST}}" ^
/testContainer:{{test_suite_bin}}\Kerberos_ServerTestSuite.dll ^
/runconfig:{{test_suite_bin}}\ServerLocalTestRun.testrunconfig ^
/resultsfile:{{test_result_file}} ^
/usestderr ^
/noisolation
