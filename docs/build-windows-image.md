# Tips for building windows image with Packer

## Use a snapshot for the source image

Use a windows image directly will fail with vague error. Refer to:

http://docs.catalystcloud.io/tutorials/using-packer-to-build-custom-bootable-images-on-the-catalyst-cloud.html#using-packer-with-windows-on-the-catalyst-cloud

## packer template key name

`source_image` is the id, `source_image_name` is the name.
Don't use name for `source_image`.

`cloud_init_file` in openstack is called `user_data_file` in packer template.

## create a proper security group
winrm will use port 5985 and 5986, make sure Ingress TCP on both ports are allowed for your IP.
If you run packer from Catalyst LAN, the `Remote IP Prefix` will be `202.78.240.7/32`.

## OpenStack RC File

Make sure `~/sambatest.catalyst.net.nz-openrc.sh` exists.

## Windows packages to install
Run `scripts/download-windows-packeges`

## Command to rebuild image

python build-windows-testclient --ms-downloads ~/Desktop/ms-downloads --use-default-pass -v
