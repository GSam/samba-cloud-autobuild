#ps1_sysnative
# powershell template for user_data_file/cloud_init_file

wmic UserAccount set PasswordExpires=False
net user Administrator {{samba_password}}
cmd /C netsh advfirewall set allprofiles state off
winrm quickconfig -q
winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="500"}'
winrm set winrm/config '@{MaxTimeoutms="1800000"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/client/auth '@{Basic="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'
net stop winrm
net start winrm

Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine -Force

Install-WindowsFeature RSAT-AD-Tools Net-Framework-Core ADCS-Cert-Authority AD-Domain-Services
Install-AdcsCertificationAuthority -CAType EnterpriseRootCa
