# cloudstack-vm-snapshotter
A basic script for taking VM snapshots.


## Getting Started

For best results, run this on Ubuntu 18.04. We're assuming you've cloned this repo to the `ubuntu` user's home directory.

1. Use `pipenv` and the `Pipfile` in this repo to install dependencies, else install them manually: `pip install cs schedule`.
2. Create a file called `cloudstack-vm-snapshotter.env` in `/home/ubuntu` and fill in the following values:

```
ACS_API=
ACS_KEY=
ACS_SECRET=

```
3. Next, create the `systemd` configuration for running this at `/etc/systemd/system/cloudstack-vm-snapshotter.service` and add the following to the file:
```
[Unit]
Description=cloudstack-vm-snapshotter
After=network.target

[Service]
Type=simple
User=ubuntu
EnvironmentFile=/home/ubuntu/cloudstack-vm-snapshotter.env
WorkingDirectory=/home/ubuntu/cloudstack-vm-snapshotter
ExecStart=/usr/bin/python3 app.py
Restart=on-failure
# Other restart options: always, on-abort, etc

[Install]
WantedBy=multi-user.target
```

Now you're all set. Run `sudo systemctl start cloudstack-vm-snapshotter` to start the script, and `sudo systemctl enable cloudstack-vm-snapshotter`.

## Configuring VMs for automated snapshots

All you need to do is add a tag to the VMs you'd like to enable automatic snapshots for. The key of the tag should be `snapshot` and the value must be `true`. Note that this _is_ case-sensitive.