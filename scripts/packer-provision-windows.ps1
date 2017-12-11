#ps1_sysnative

# this script is used by templates/build-wondows-image.json,
# which is a packer template to build windows image

# echo on
Set-PSDebug -Trace 1

# install chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Yes to all
choco feature enable -n allowGlobalConfirmation

# install openssh and install service
choco install openssh -params "'/SSHServerFeature'" -y
choco install firefox wireshark winpcap wget -y


# download windows protocol test suites files
Invoke-WebRequest -Uri 'https://github.com/Microsoft/WindowsProtocolTestSuites/archive/master.zip' -OutFile 'C:\\WindowsProtocolTestSuites.zip'

Invoke-WebRequest -Uri 'https://github.com/Microsoft/WindowsProtocolTestSuites/releases/download/2.0/ADFamily-TestSuite-ServerEP.msi'  -OutFile 'C:\\ADFamily-TestSuite-ServerEP.msi'

Invoke-WebRequest -Uri 'https://github.com/Microsoft/WindowsProtocolTestSuites/releases/download/2.0/Kerberos-TestSuite-ServerEP.msi'  -OutFile 'C:\\Kerberos-TestSuite-ServerEP.msi'

Invoke-WebRequest -Uri 'https://github.com/Microsoft/WindowsProtocolTestSuites/releases/download/2.0/MS-AZOD-TestSuite-ODEP.msi'  -OutFile 'C:\\MS-AZOD-TestSuite-ODEP.msi'

Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/GSam/WindowsProtocolTestSuites/staging/InstallPrerequisites/InstallPrerequisites.ps1'  -OutFile 'C:\\InstallPrerequisites.ps1'

Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/GSam/WindowsProtocolTestSuites/staging/InstallPrerequisites/PrerequisitesConfig.xml'  -OutFile 'C:\\PrerequisitesConfig.xml'

Invoke-WebRequest -Uri 'https://github.com/Microsoft/WindowsProtocolTestSuites/releases/download/2.0/ProtocolTestManager.msi'  -OutFile 'C:\\ProtocolTestManager.msi'

C:\\ProtocolTestManager.msi /q