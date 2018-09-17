:: Copyright (c) Microsoft. All rights reserved.
:: Licensed under the MIT license. See LICENSE file in the project root for full license information.

@echo off

echo ==============================================
echo          Start to run Kerberos all test cases
echo ==============================================

if not defined vspath (
    if defined VS110COMNTOOLS (
        set vspath="%VS110COMNTOOLS%"
    ) else if defined VS120COMNTOOLS (
        set vspath="%VS120COMNTOOLS%"
    ) else if defined VS140COMNTOOLS (
        set vspath="%VS140COMNTOOLS%"
    ) else (
        echo Error: Visual Studio or Visual Studio test agent should be installed, version 2012 or higher
        goto :eof
    )
)

del C:\testresult.trx

%vspath%"..\IDE\mstest.exe" ^
/testContainer:{{test_suite_bin}}\Kerberos_ServerTestSuite.dll ^
/runconfig:{{test_suite_bin}}\ServerLocalTestRun.testrunconfig ^
/usestderr /noisolation /resultsfile:C:\testresult.trx

