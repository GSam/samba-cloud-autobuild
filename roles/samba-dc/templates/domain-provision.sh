#!/bin/bash

/usr/local/samba/bin/samba-tool domain provision \
  --use-rfc2307 \
  --realm={{samba_realm}} \
  --domain={{samba_domain}} \
  --server-role=dc \
  --adminpass='{{samba_password}}' \
  --krbtgtpass='{{samba_password}}' \
  --machinepass='{{samba_password}}' \
  --dnspass='{{samba_password}}' \
  --option='dns forwarder={{samba_dns_forwarder}}' \
  --option='kccsrv:samba_kcc={{use_samba_kcc}}' \
  --option='ldapserverrequirestrongauth=no'
