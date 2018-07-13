# Setup GitLab CI with Ansible

## How to use

Here we use openstack as the driver.

### Edit and source RC File

In openstack dashboard site, click your email in the up right corner.
Download OpenStack RC File v3, edit it, make sure you have these:

    # this is a var from RC File v2, but docker-machine needs it
    export OS_TENANT_NAME="sambatest.catalyst.net.nz"
    # stop script to ask for password
    export OS_PASSWORD=YOUR-PASSWORD

Make sure you source it, and check:

    env | grep OS_

### Create virtualenv for driver and activate

create a virtualenv for each driver, and install the `requirements.txt` in it:

    virtualenv openstack openstackenv
    pip install -r roles/openstack/requirements.txt
    source openstackenv/bin/activate

### Make sure dynamic inventory is working

If everything is ok, the dynamic inventory should work:

    ../inventory/openstack_inventory.py --list

### Create gitlab-runner for your driver

Now run the bash script for your driver to create and provision gitlab-runner:

    ./run-openstack.sh -e REGISTRATION_TOKEN=your-token -e RUNNER_NAME=gitlab-runner-0

We didn't put the registration token into repo, you have to provide it.
Thus you can register this runner to any gitlab project or group.

Please be aware that a group/team/organization in gitlab have its own
registration token, we can make good use of that to register runner for all
projects in the group.

For `RUNNER_NAME`, if you provide a existing name, ansible will update it,
unregister all existing runners on it, and register again.

If you provide an non-existing name, ansible will create new runner.

The second way is recommended, which means we always have fresh new build,
without breaking the old runners.

### Absent a runner and server

Once the new runner is up and working fine, you need to pause the old
runner(which will stop it to receive new jobs). When all jobs finished, you
can run this command to unregister runner and delete server:

    ./run-openstack.sh -e RUNNER_NAME=gitlab-runner-0 -e state=absent

Usage for other drivers is similar.

## How it works

All actual work are done by 2 type of roles:

- driver role, e.g.: openstack, create/delete instance in cloud
- gitlab-runner: provison the instance as a gitlab-runner server

Each role should be self-contained as much as possible. For those vars have to
be shared, e.g.: `USER_DATA_FILE`, put them in `group_vars/all.yml`.

The `templates/env_file` in each driver role will be rendered and passed to
gitlab-runner docker container and then used by docker-machine in it.
It should only contains env vars needed by docker-machine for that specific
driver. To get full list:

    docker-machine create --driver openstack --help

