#!/bin/bash

/usr/local/samba/bin/samba-tool domain backup restore
  --newservername={{primary_dc_name}} \ \
  --backup-file={{samba_backup_file}} \
  --targetdir={{samba_restore_target_dir}} \
  --username={{samba_username}} \
  --password={{samba_password}}