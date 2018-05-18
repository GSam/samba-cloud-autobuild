## set up rax credentials file

create credentials file:

    touch ~/.rackspace_cloud_credentials

with following content:

    [rackspace_cloud]
    username = YOUR-RACKSPACE-USERNAME
    api_key = YOUR-RACKSPACE-API-KEY

NOTE: no quotes arround values, otherwise authentication will fail.

add environment variables to your .bashrc or .zshrc:

    export RAX_CREDS_FILE=~/.rackspace_cloud_credentials
    export RAX_REGION=SYD  # SYD,IAD,DFW,ORD,HKG

The rax.py inventory script will read this var.

add to your .bashrc or .zshrc:

    ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt

.vault_pass.txt is the file has your vault pass in it as a single line.
