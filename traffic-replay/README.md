# Setup traffic-replay ansible environment

1. Fetch catalyst samba common private key from pview:

    ssh -t cat-prod-secret pview -d samba \?

Copy and save the private key to `.ssh/id_rsa_catalyst_samba`.
The name matters, because we use it in `ansible.cfg`.
And all automation script will use this key, please keep it there.

2. Create a virtualenv and install Python depenencies:

    pip install -r requirements.txt

3. Download your openstack RC file and source it

4. Check `group_vars/all.yml`, modify the vars to meet your demand.

For example, `repo_url` and `repo_branch`.

5. Run script:

    ./main.yml -v
