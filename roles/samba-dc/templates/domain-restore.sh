#!/bin/bash

/usr/local/samba/bin/samba-tool domain backup restore \
  --newservername={{primary_dc_name}}-restore \
  --backup-file={{ansible_env.HOME}}/samba-backup \
  --targetdir={{samba_restore_target_dir}} \
  --username={{samba_username}} \
  --password={{samba_password}}
