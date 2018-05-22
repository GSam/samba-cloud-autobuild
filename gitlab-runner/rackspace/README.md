# Set up gitlab-runner in Rackspace Cloud with Ansible

## Set up rax credentials file

Create credentials file:

    touch ~/.rackspace_cloud_credentials

with following content:

    [rackspace_cloud]
    username = YOUR-RACKSPACE-USERNAME
    api_key = YOUR-RACKSPACE-API-KEY

NOTE: no quotes arround values, otherwise authentication will fail.


## set up environment variables

Add environment variables to your .bashrc or .zshrc:

    export RAX_CREDS_FILE=~/.rackspace_cloud_credentials
    export RAX_REGION=DFW
    export OS_USERNAME=YOUR-RACKSPACE-USERNAME
    export OS_API_KEY=YOUR-RACKSPACE-API-KEY

Source your .bashrc file or restart your terminal.

NOTE: We didn't put credentials to vault, so we can switch to another account easily.


## Set up python virtualenv for rackspace and ansible modules

    sudo apt install python-virtualenv
    mkdir ~/.virtualenvs
    cd ~/.virtualenvs
    virtualenv rax
    source rax/bin/activate

Or you can install `virtualenvwrapper` to make above things easier(optional):

    http://virtualenvwrapper.readthedocs.io

Then cd to here, install python deps:

    pip install -r requirements.txt

## Verify above set up

Run this in current dir, with virtualenv activated:

    ./invertory/rax.py --list

If everything is ok, this should return you json data from rackspace.


## Set up Ansible vault password file

Find the gitlab-runner Ansible vault password here:

    ssh cat-prod-secret
    pview -d samba \?

Save the vault to `~/.vault_pass`.  In `ansible.cfg`, we ask Ansible to read
this file, so make sure name is correct.

## Run Ansible

Now you are ready to go:

    ansible-playbook main.yml

