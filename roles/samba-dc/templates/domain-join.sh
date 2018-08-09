#!/bin/bash

/usr/local/samba/bin/samba-tool domain \
  join {{samba_domain}} DC \
  --server={{primary_dc_name}} \
  --realm={{samba_realm}} \
  --adminpass={{samba_password}} \
  --username={{samba_username}} \
  --password={{samba_password}}
