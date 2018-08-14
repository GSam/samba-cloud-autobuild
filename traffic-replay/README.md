# Setup traffic-replay ansible environment

- Download your openstack RC file, edit it, and source it

- Fetch catalyst samba common private key from pview:

    ssh -t cat-prod-secret pview -d samba \?

Copy and save the private key to `.ssh/id_rsa_catalyst_samba`.
The name matters, because we use it in `ansible.cfg`.
And all automation script will use this key, please keep it there.

- Create a virtualenv and install Python depenencies:

    sudo apt install python-virtualenv
    virtualenv ansible
    source ansible/bin/activate
    pip install -r requirements.txt


- Check `group_vars/all.yml`, modify the vars to meet your demand.

For example, `repo_url` and `repo_branch`.

- Run script:

    ./main.yml -v
