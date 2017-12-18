#!/bin/bash
#
#  Copyright 2016 Andreas Schneider <asn@samba.org>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This is basically Config-DC01.ps1

export PATH="/usr/local/samba/bin:$PATH"

REALM="{{ samba_realm }}"
DNS_NAME="{{ samba_realm|lower }}"
DN_DC_NAME="DC=krb,DC=samba,DC=site"

ADMIN_ACCOUNT="Administrator"
ADMIN_PASSWORD="Password01@"

LOCAL_MACHINE_ACCOUNT="$(hostname -s)\$"
LOCAL_MACHINE_PASSWORD="Password01!"

GROUP01_NAME="testGroup"
GROUP01_SCOPE="Global"
GROUP01_TYPE="Security"

GROUP02_NAME="testGroup2"
GROUP02_SCOPE="Global"
GROUP02_TYPE="Security"

RESOURCE_GROUP01_NAME="resouceGroup"
RESOURCE_GROUP01_SCOPE="Domain"
RESOURCE_GROUP01_TYPE="Security"

RESOURCE_GROUP02_NAME="resouceGroup2"
RESOURCE_GROUP02_SCOPE="Domain"
RESOURCE_GROUP02_TYPE="Security"


LOCAL_RESOURCE01_NAME="localResource01"
LOCAL_RESOURCE01_ACCOUNTNAME="$LOCAL_RESOURCE01_NAME\$"
LOCAL_RESOURCE01_FQDN="localresource01.{{ samba_realm|lower }}"
LOCAL_RESOURCE01_PASSWORD="Password01!"

LOCAL_RESOURCE02_NAME="localResource02"
LOCAL_RESOURCE02_ACCOUNTNAME="$RESOURCE_GROUP02_NAME\$"
LOCAL_RESOURCE02_FQDN="localresource02.{{ samba_realm|lower }}"
LOCAL_RESOURCE02_PASSWORD="Password01!"


USER01_SALT="SAMBADC.SITEtest01"
USER01_NAME="test01"
USER01_PASSWORD="Password01^"

USER02_NAME="test02"
USER02_PASSWORD="Password01&"
USER02_TRANSFORMED_CLAIMS="ad://ext/DepartmentHR"

USER03_NAME="UserDelegNotAllowed"
USER03_PASSWORD="Chenjialuo;"

USER04_NAME="UserTrustedForDeleg"
USER04_PASSWORD="Yuanchengzhi;"
USER04_SERVICE_NAME="abc/UserTrustedForDeleg"

USER05_NAME="UserWithoutUPN"
USER05_PASSWORD="Zhangwuji;"

USER06_NAME="UserPreAuthNotReq"
USER06_PASSWORD="Duanyu;"

USER07_NAME="UserDisabled"
USER07_PASSWORD="Chenjinnan;"

USER08_NAME="UserExpired"
USER08_PASSWORD="Guojing;"

USER09_NAME="UserLocked"
USER09_PASSWORD="Qiaofeng;"

USER10_NAME="UserOutofLogonHours"
USER10_PASSWORD="Huyidao;"

USER11_NAME="UserPwdMustChgPast"
USER11_PASSWORD="Weixiaobao;"

USER12_NAME="UserPwdMustChgZero"
USER12_PASSWORD="Yangguo;"

USER13_NAME="UserLocalGroup"
USER13_PASSWORD="Yantengda;"

USER14_NAME="UserDesOnly"
USER14_PASSWORD="Renyingying;"

USER15_NAME="testsilo01"
USER15_PASSWORD="Password01!"

USER16_NAME="testsilo02"
USER16_PASSWORD="Password01!"

USER17_NAME="testsilo03"
USER17_PASSWORD="Password01!"

USER18_NAME="testsilo04"
USER18_PASSWORD="Password01!"

USER19_NAME="testsilo05"
USER19_PASSWORD="Password01!"

USER22_NAME="testpwd"
USER22_PASSWORD="Password01!"

USER_KRBTGT_NAME="krbtgt"
USER_KRBTGT_PASSWORD="Password01\$"

###########################################################
# GROUP01
###########################################################
samba-tool group delete $GROUP01_NAME -d0

samba-tool group add $GROUP01_NAME --group-scope=$GROUP01_SCOPE --group-type=$GROUP01_TYPE -d0

###########################################################
# GROUP02
###########################################################
samba-tool group delete $GROUP02_NAME -d0

samba-tool group add $GROUP02_NAME --group-scope=$GROUP02_SCOPE --group-type=$GROUP02_TYPE -d0

###########################################################
# RESOURCE_GROUP01
###########################################################
samba-tool group delete $RESOURCE_GROUP01_NAME -d0

samba-tool group add $RESOURCE_GROUP01_NAME --group-scope=$RESOURCE_GROUP01_SCOPE --group-type=$RESOURCE_GROUP01_TYPE -d0

###########################################################
# RESOURCE_GROUP02
###########################################################
samba-tool group delete $RESOURCE_GROUP02_NAME -d0

samba-tool group add $RESOURCE_GROUP02_NAME --group-scope=$RESOURCE_GROUP02_SCOPE --group-type=$RESOURCE_GROUP02_TYPE -d0

###########################################################
# LOCAL_RESOURCE01
###########################################################
ldbdel -H /usr/local/samba/private/sam.ldb CN=$LOCAL_RESOURCE01_NAME,CN=Computers,$DN_DC_NAME -d0

cat > tmp.ldif << EOF
dn: CN=$LOCAL_RESOURCE01_NAME,CN=Computers,$DN_DC_NAME
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
objectClass: computer
cn: $LOCAL_RESOURCE01_NAME
name: $LOCAL_RESOURCE01_NAME
sAMAccountName: $LOCAL_RESOURCE01_ACCOUNTNAME
userAccountControl: 4096
dNSHostName: $LOCAL_RESOURCE01_NAME.$DNS_NAME
servicePrincipalName: HOST/$LOCAL_RESOURCE01_NAME
servicePrincipalName: HOST/$LOCAL_RESOURCE01_NAME.$DNS_NAME
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

net rpc user password $LOCAL_RESOURCE01_ACCOUNTNAME $LOCAL_RESOURCE01_PASSWORD -U$ADMIN_ACCOUNT%$ADMIN_PASSWORD

samba-tool group addmembers $RESOURCE_GROUP01_NAME $LOCAL_RESOURCE01_ACCOUNTNAME -d0
samba-tool group addmembers $RESOURCE_GROUP02_NAME $LOCAL_RESOURCE01_ACCOUNTNAME -d0

###########################################################
# LOCAL_RESOURCE02
###########################################################
ldbdel -H /usr/local/samba/private/sam.ldb CN=$LOCAL_RESOURCE02_NAME,CN=Computers,$DN_DC_NAME -d0

cat > tmp.ldif << EOF
dn: CN=$LOCAL_RESOURCE02_NAME,CN=Computers,$DN_DC_NAME
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
objectClass: computer
cn: $LOCAL_RESOURCE02_NAME
name: $LOCAL_RESOURCE02_NAME
sAMAccountName: $LOCAL_RESOURCE02_ACCOUNTNAME
userAccountControl: 4096
dNSHostName: $LOCAL_RESOURCE02_NAME.$DNS_NAME
servicePrincipalName: HOST/$LOCAL_RESOURCE02_NAME
servicePrincipalName: HOST/$LOCAL_RESOURCE02_NAME.$DNS_NAME
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

net rpc user password $LOCAL_RESOURCE02_ACCOUNTNAME $LOCAL_RESOURCE02_PASSWORD -U$ADMIN_ACCOUNT%$ADMIN_PASSWORD

samba-tool group addmembers $RESOURCE_GROUP01_NAME $LOCAL_RESOURCE02_ACCOUNTNAME -d0
samba-tool group addmembers $RESOURCE_GROUP02_NAME $LOCAL_RESOURCE02_ACCOUNTNAME -d0

###########################################################
# USER01
###########################################################
samba-tool user delete $USER01_NAME -d0

samba-tool user create "$USER01_NAME" "$USER01_PASSWORD" --profile-path="c:\\profiles\\" --script-path="c:\\scripts\\" --home-drive="c:" --home-directory="c:\\home\\" -d0
samba-tool user setexpiry --noexpiry $USER01_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER01_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: DisplayName
DisplayName: $USER01_NAME
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

samba-tool group addmembers "$GROUP02_NAME" "$USER01_NAME" -d0

###########################################################
# USER02
###########################################################
samba-tool user delete $USER02_NAME -d0

samba-tool user create "$USER02_NAME" "$USER02_PASSWORD" --department=HR -d0
samba-tool user setexpiry --noexpiry $USER02_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER02_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER03
###########################################################
samba-tool user delete $USER03_NAME -d0

samba-tool user create "$USER03_NAME" "$USER03_PASSWORD" -d0
cat > tmp.ldif << EOF
dn: CN=$USER03_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 1049152
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER04
###########################################################
samba-tool user delete $USER04_NAME -d0

samba-tool user create "$USER04_NAME" "$USER04_PASSWORD" -d0
# UF_PASSWD_CANT_CHANGE UF_TRUSTED_FOR_DELEGATION
cat > tmp.ldif << EOF
dn: CN=$USER04_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 524864
-
replace: servicePrincipalName
servicePrincipalName: abc/$USER04_NAME
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER05
###########################################################
samba-tool user delete $USER05_NAME -d0

samba-tool user create "$USER05_NAME" "$USER05_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER05_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER05_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
delete: userPrincipalName
-
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER06
###########################################################
samba-tool user delete $USER06_NAME -d0

samba-tool user create "$USER06_NAME" "$USER06_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER06_NAME -d0
# UF_PASSWD_CANT_CHANGE UF_DONT_REQUIRE_PREAUTH
cat > tmp.ldif << EOF
dn: CN=$USER06_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 4194880
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif


###########################################################
# USER07
###########################################################
samba-tool user delete $USER07_NAME -d0

samba-tool user create "$USER07_NAME" "$USER07_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER07_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER07_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

samba-tool user disable $USER07_NAME -d0

###########################################################
# USER08
###########################################################
samba-tool user delete $USER08_NAME -d0

samba-tool user create "$USER08_NAME" "$USER08_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER08_NAME -d0
# UF_PASSWD_CANT_CHANGE
# Expire 2011-01-01
cat > tmp.ldif << EOF
dn: CN=$USER08_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: accountExpires
accountExpires: 1
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif


###########################################################
# USER09
###########################################################
echo "### CHANGE PASSWORD SETTINGS"
samba-tool domain passwordsettings set --complexity=off --history-length=default --min-pwd-length=6 --min-pwd-age=default --max-pwd-age=30 --account-lockout-threshold=1 --account-lockout-duration=99999 -d0

samba-tool user delete $USER09_NAME -d0

samba-tool user create "$USER09_NAME" "$USER09_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER09_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER09_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

# Lock user
echo "### LOCK USER"
smbclient //127.0.0.1/IPC$ -U$USER09_NAME%1234567
smbclient //127.0.0.1/IPC$ -U$USER09_NAME%1234567
smbclient //127.0.0.1/IPC$ -U$USER09_NAME%1234567
smbclient //127.0.0.1/IPC$ -U$USER09_NAME%1234567

# reset password policies
echo "### RESET PASSWORD SETTINGS"
samba-tool domain passwordsettings set --complexity=default --history-length=default --min-pwd-length=default --min-pwd-age=default --max-pwd-age=default --account-lockout-threshold=default --account-lockout-duration=default -d0

###########################################################
# USER10
###########################################################
samba-tool user delete $USER10_NAME -d0

samba-tool user create "$USER10_NAME" "$USER10_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER10_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER10_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: logonHours
logonHours:: AAAAAAAAAAAAAAAAAAAAAAAAAAAA
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER11
###########################################################
samba-tool user delete $USER11_NAME -d0

samba-tool user create "$USER11_NAME" "$USER11_PASSWORD" --must-change-at-next-login -d0
# UF_PASSWD_CANT_CHANGE UF_DONT_REQUIRE_PREAUTH
cat > tmp.ldif << EOF
dn: CN=$USER11_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 4194880
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER12
###########################################################
samba-tool user delete $USER12_NAME -d0

samba-tool user create "$USER12_NAME" "$USER12_PASSWORD" --must-change-at-next-login -d0
# UF_DONT_REQUIRE_PREAUTH
cat > tmp.ldif << EOF
dn: CN=$USER12_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 4194816
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER13
###########################################################
samba-tool user delete $USER13_NAME -d0

samba-tool user create "$USER13_NAME" "$USER13_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER13_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER13_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

samba-tool group addmembers "$GROUP02_NAME" "$USER13_NAME" -d0
samba-tool group addmembers "$RESOURCE_GROUP01_NAME" "$USER13_NAME" -d0
samba-tool group addmembers "$RESOURCE_GROUP02_NAME" "$USER13_NAME" -d0

###########################################################
# USER14
###########################################################
samba-tool user delete $USER14_NAME -d0

samba-tool user create "$USER14_NAME" "$USER14_PASSWORD" -d0
# UF_PASSWD_CANT_CHANGE UF_USE_DES_KEY_ONLY
cat > tmp.ldif << EOF
dn: CN=$USER14_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 2097728
-
replace: msDS-SupportedEncryptionTypes
msDS-SupportedEncryptionTypes: 3
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER15 - DES
###########################################################
samba-tool user delete $USER15_NAME -d0

samba-tool user create "$USER15_NAME" "$USER15_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER15_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER15_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: msDS-SupportedEncryptionTypes
msDS-SupportedEncryptionTypes: 3
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER16 - AES
###########################################################
samba-tool user delete $USER16_NAME -d0

samba-tool user create "$USER16_NAME" "$USER16_PASSWORD" --department=HR -d0
samba-tool user setexpiry --noexpiry $USER16_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER16_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: msDS-SupportedEncryptionTypes
msDS-SupportedEncryptionTypes: 24
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER17 - RC4
###########################################################
samba-tool user delete $USER17_NAME -d0

samba-tool user create "$USER17_NAME" "$USER17_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER17_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER17_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
-
replace: msDS-SupportedEncryptionTypes
msDS-SupportedEncryptionTypes: 4
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER18
###########################################################
samba-tool user delete $USER18_NAME -d0

samba-tool user create "$USER18_NAME" "$USER18_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER18_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER18_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER19 - RC4
###########################################################
samba-tool user delete $USER19_NAME -d0

samba-tool user create "$USER19_NAME" "$USER19_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER19_NAME -d0
# UF_PASSWD_CANT_CHANGE
cat > tmp.ldif << EOF
dn: CN=$USER19_NAME,CN=Users,$DN_DC_NAME
changetype: modify
replace: userAccountControl
userAccountControl: 576
EOF
ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
rm tmp.ldif

###########################################################
# USER22
###########################################################
samba-tool user delete $USER22_NAME -d0

samba-tool user create "$USER22_NAME" "$USER22_PASSWORD" -d0
samba-tool user setexpiry --noexpiry $USER22_NAME -d0

###########################################################
# USER_KRBTGT
###########################################################
echo "### Change password for $USER_KRBTGT_NAME"
net rpc user password $USER_KRBTGT_NAME $USER_KRBTGT_PASSWORD -U$ADMIN_ACCOUNT%$ADMIN_PASSWORD

###########################################################
# LOCAL_MACHINE_ACCOUNT
###########################################################

# UF_PASSWD_CANT_CHANGE
#cat > tmp.ldif << EOF
#dn: CN=$LOCAL_MACHINE_ACCOUNT,CN=Users,$DN_DC_NAME
#changetype: modify
#replace: userAccountControl
#userAccountControl: 576
#EOF
#ldbmodify -H /usr/local/samba/private/sam.ldb --verbose -d0 < tmp.ldif
#rm tmp.ldif

exit 0
