# Introduction

This repository contains ansible playbooks that can create a multi site, multi DC samba4 environment in the Catalyst Cloud.

It is based on http://git.catalyst.net.nz/gw?p=samba-cloud-autobuild.git;a=blob_plain;f=yaml/single-site.yaml;h=b5d8e7a7f2edd2fba5cacf2cb30c37afd463d78c;hb=HEAD

The playbooks can be used to:
* provision the entire infrastructure required to host samba servers
* create and configure a master node which then builds samba and becomes the first DC
* create and configure all slaves that rsync's compiled samba binaries from master, then install samba and join the domain
* destroy and clean up the entire stack

# Setup

You will need to install ansible (at least version 2.2.x)i. Follow http://docs.catalystcloud.io/first-instance/ansible.html#launching-your-first-instance-using-ansible for instructions on how to set it up.

All included playbooks rely on using ansible dynamic inventory, so consider setting up your machine as described on http://docs.catalystcloud.io/tutorials/ansible-openstack-dynamic-inventory.html
The inventory script and its configuration file are already included in inventory/ directory. If you don't want to put anything in /etc/ansible/ you can still use the included scripts explicitly by using '-i' parameter when running ansible:
```
ansible-playbook -i inventory/openstack.py site.yml -e env_prefix=your_env_prefix
```

# Before first run

Check group_vars/all and tweak environment or build variables to match your requirements.

By default ssh access to instances is allowed from Wellington and Auckland offices and inter-node communication is allowed on all TCP and UDP ports.

If required, additional security rules can be added be editing host_vars/localhost file and rerunning ansible to apply them:
```
ansible-playbook site.yml -e env_prefix=your_env_prefix --tags "security-group-rules"
```

# Usage
## Build and destroy

The entire stack can be built by running:
```
ansible-playbook site.yml -e env_prefix=your_env_prefix
```
and it can be later destroyed by running:
ansible-playbook site.yml -e 'set_state=absent' -e env_prefix=your_env_prefix

Note on 'set_state' variable: It defaults to 'present' when not set and is used in every ansible module that accepts 'state=' parameter, so it's easy to create and destroy resources using the same module. There are some exceptions when creating and destroying resources is order dependant (on create networks go first then routers, but on destroy router first then networks), so this variable is also used in conditionals.

*Note on 'env_prefix' variable and environment separation:* The infrastructure deploy/destroy playbooks honour 'env_prefix' variable value when it is set in vars files and will not touch any cloud resources outside of the environment set.
While samba.yml playbook revies on that variable to only manage the hosts from specific environment, it can't access it if it is set in hostvars (this is the limitation of playbook hosts: field - https://github.com/ansible/ansible/issues/16931 ), so it needs to be specified, unquoted on the command line as an 'extra var'.
There is a pre-run-check.yml playbook responsible for making sure it is set.


## Example usage
To deploy samba on an already provisioned infrastructure run:
```
ansible-playbook site.yml --tags "samba" -e env_prefix=your_env_prefix
```

By default samba will be copiled and installed only once. To recompile and reinstall it again on all nodes, set another external variable: -e recompile=true
NOTE: compilation is done on master node, slaves only rsync binaries from it.

Use tags to only run compilation related tasks rather than go through all node config:
```
ansible-playbook samba.yml -e env_prefix=dev -e recompile=true --tags "configure,compile,install"
```

## Tags

There is at least one tag associated with every resource - to allow creating, destroying or re-running certain parts of the play, for example:

This will create network components and VMs but will not deploy any samba code
```
ansible-playbook site.yml --tags "cloudinf"
```

This will rsync scripts and binaries from the master node but will not run 'make install' on a slave
```
ansible-playbook site.yml --tags "slave-rsync"
```

Feel free to check what tags are associated with which plays and tasks and feel free to add your own.
