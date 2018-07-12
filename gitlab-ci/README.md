# Setup GitLab CI with Ansible

## how to use with openstack

In openstack dashboard site, click your email in the up right corner.
Download OpenStack RC File v3, edit it, make sure you have these:

    # this is a var from RC File v2, but docker-machine need it
    export OS_TENANT_NAME="sambatest.catalyst.net.nz"
    # stop script to ask for password
    export OS_PASSWORD=YOUR-PASSWORD

Make sure you source it, and check:

    env | grep OS_

Now run the bash script for your driver to start Ansible:

    ./run-openstack.sh -e REGISTRATION_TOKEN=your-token -e RUNNER_NAME=gitlab-runner-0

We didn't put the registration token into repo, you have to provide it.
Thus you can register this runner to any gitlab project or group.

Please be aware that a group/team/organization in gitlab have its own
registration token, we can make good use of that to register runner for all
projects in the group.

For the `RUNNER_NAME`, if you provide a existing name, then we will update it,
unregister all existing runners on it, and register again.

If you provide an non-existing name, then we will create new runner.

The second way is recommended, then we always have fresh new build, without
breaking the old runners.

Once the new runner is up and working fine, you need to pause the old
runner(which will stop it to receive new jobs), and delete the instance later.

## How it works

All actual work are done by 2 type of roles:

- driver role, e.g.: openstack, create instance in cloud
- gitlab-runner: provison the instance as a gitlab-runner server

Each role should be self-contained as much as possible. For those vars have to
be shared, e.g.: `USER_DATA_FILE`, put them in group_vars/all.yml.

The `templates/env_file` in each driver role will be passed to gitlab-runner
docker container and then used by docker-machine in it. It should only contains
env vars needed by docker-machine for that specific driver. To get full list:

    docker-machine create --driver openstack --help

