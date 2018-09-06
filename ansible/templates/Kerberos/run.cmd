:: Copyright (c) Microsoft. All rights reserved.
:: Licensed under the MIT license. See LICENSE file in the project root for full license information.

@echo off

echo ==============================================
echo          Start to run Kerberos all test cases
echo ==============================================

set vspath="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\mstest.exe"

del C:\testresult.trx

%vspath% ^
/testContainer:C:\MicrosoftProtocolTests\Kerberos\Server-Endpoint\3.18.9.0\Bin\Kerberos_ServerTestSuite.dll ^
/runconfig:C:\MicrosoftProtocolTests\Kerberos\Server-Endpoint\3.18.9.0\Bin\ServerLocalTestRun.testrunconfig ^
/usestderr /noisolation /resultsfile:C:\testresult.trx

