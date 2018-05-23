Set up Marge-Bot service on a Ubuntu server

Go to `cat-prod-secret:

    ssh cat-prod-secret
    pedit -d samba \?

Copy ansible vault password, save it to:

    ~/.vault_pass

Copy ssh private key for samba team, and save it to:

    ~/.ssh/id_rsa_catalyst_samba
    chmod 400 ~/.ssh/id_rsa_catalyst_samba

Then cd to this dir, run:

    ansible-playbook main.yml


Note: this playbook didn't bother to create server and network in cloud since
it's a one off task. If you need to do it again, just prepare the server
manually and put the ip in hosts.ini.
