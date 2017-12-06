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

del C:\ff.trx

%vspath%"..\IDE\mstest.exe" "/testContainer:C:\MicrosoftProtocolTests\Kerberos\Server-Endpoint\2.0.66.0\Batch\..\Bin\Kerberos_ServerTestSuite.dll" /runconfig:C:\MicrosoftProtocolTests\Kerberos\Server-Endpoint\2.0.66.0\Batch\..\Bin\ServerLocalTestRun.testrunconfig /usestderr /test:Microsoft.Protocol.TestSuites.Kerberos.TestSuite.KILE.KileInteractiveLogonTest.UDPtoTCP /noisolation /resultsfile:C:\ff.trx

