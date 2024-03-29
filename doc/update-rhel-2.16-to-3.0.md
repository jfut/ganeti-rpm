# Update Ganeti RPM package from 2.16 to 3.0

Ganeti RPM Packaging for RHEL/CentOS/others.

## Update from a version earlier than 2.15

If you are updating from a version earlier than 2.15, see the document for 2.16.

- [Update Ganeti RPM package from 2.15 to 2.16](https://github.com/jfut/ganeti-rpm/blob/master/doc/update-rhel-2.15-to-2.16.rst)

Official documentation:

- [Ganeti 3.0.0 Release](https://github.com/ganeti/ganeti/releases/tag/v3.0.0)

## Backup

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

```bash
systemctl stop ganeti-metad.service
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
tar czf /root/ganeti-$(date +%FT%H-%M-%S).tar.gz -C /var/lib ganeti
chmod 600 /root/ganeti-$(date +%FT%H)*.tar.gz
```

## Update ganeti package

**Mandatory** on all nodes.

```bash
yum --enablerepo=integ-ganeti update integ-ganeti-release
yum --enablerepo=epel,integ-ganeti update ganeti
```

## Important changes

### Change running user and group (#20)

Now, ganeti daemons work with the privileges of gnt-* users and gnt-* groups.

Directories and files in `/var/lib/ganeti` and `/var/log/ganeti` are automatically modified to the appropriate permissions by the `/usr/lib64/ganeti/ensure-dirs` script at startup.

However, to modify the permissions of files in `/var/lib/ganeti/queue/archive/`, you need to manually execute the following command only once after updating to the new package.

```bash
# -f, --full-run  Make a full run and set permissions on archived jobs (time consuming)
/usr/lib64/ganeti/ensure-dirs -f
```

Once you run it, you can just start it normally.

### Migrate qemu-kvm to qmue-kvm-ev

The oldest version of qemu supported by the upstream is `qemu-2.11` (Ubuntu 18.04 LTS Bionic). Therefore, it is recommended to migrate `qemu-kvm`(version `1.5.x`) on `el7` to `qemu-kvm-ev`(version `2.12.x`). At the moment, Ganeti of the Ganeti RPM Package still works with `qemu-kvm`, but it will not working in the future.

```bash
# Migrate qemu-kvm to qemu-kvm-ev
yum install centos-release-qemu-ev
yum update qemu-*
```

## Upgrade configuration files on master node

**Mandatory** on **master** node only.

Upgrade the configuration files(/var/lib/ganeti).

```bash
# dry run
/usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run

# upgrade
/usr/lib64/ganeti/tools/cfgupgrade --verbose
```

## Start ganeti services

**Mandatory** on **member** nodes.

```bash
systemctl start ganeti.target
systemctl start ganeti-kvmd.service

# Optional: ganeti-metad is the daemon providing the metadata service.
systemctl start ganeti-metad.service
```

**Mandatory** on **master** node only.

```bash
systemctl start ganeti.target
gnt-cluster redist-conf

systemctl restart ganeti.target
systemctl start ganeti-kvmd.service

# Optional: ganeti-metad is the daemon providing the metadata service.
systemctl start ganeti-metad.service

gnt-cluster verify
```

**Troubleshooting**

- 'Can't find node' messages

You can ignore the 'Can't find node' messages and continue.

```bash
$ /usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
Please make sure you have read the upgrade notes for Ganeti 3.0.0
(available in the UPGRADE file and included in other documentation
formats). Continue with upgrading configuration?
y/[n]/?: y
2021-01-26 10:11:01,250: Found configuration version 2160000 (2.16.0)
2021-01-26 10:11:01,254: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2021-01-26 10:11:01,254: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2021-01-26 10:11:01,254: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2021-01-26 10:11:01,254: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2021-01-26 10:11:01,256: Writing configuration file to /var/lib/ganeti/config.data
Configuration successfully upgraded to version 3.0.0.
```

- Restore an old configuration and downgrade Ganeti

You can restore an old configuration from a backup file and downgrade Ganeti.

```bash
# on all nodes
systemctl stop ganeti-metad.service
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
mv /var/lib/ganeti /var/lib/ganeti.failed
tar zxf /root/ganeti-BACKUP_DATE.tar.gz -C /var/lib

# el7
yum --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el7
# el8
yum --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el8

systemctl start ganeti.target
systemctl start ganeti-kvmd.service
# Optional: ganeti-metad is the daemon providing the metadata service.
systemctl start ganeti-metad.service
```

## Considerations when migrating from EL7 to EL8/EL9

From EL8 onwards, SSH DSA keys are not supported. Therefore, if your Ganeti cluster is using DSA keys, you must first migrate to RSA keys on an EL7 cluster before you can add new EL8 or later Ganeti nodes to the cluster.

```bash
# Before
[root@node01.example.org ~] $ gnt-cluster info | grep -E "rsa|dss|ssh"
  modify ssh setup: True
  ssh_key_type: dsa
  ssh_key_bits: 1024
  ssh_port: 22

# Renew SSH keys
[root@node01.example.org ~] $ gnt-cluster renew-crypto --new-ssh-keys --ssh-key-type=rsa --ssh-key-bits=4096
The authenticity of host 'node02.example.org (192.168.3.112)' can't be established.
ED25519 key fingerprint is SHA256:AIQZfo/id99meiNTjR35coqOxNiy68prbM+OAz2reX4.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Updating certificates now. Running "gnt-cluster verify"  is recommended after this operation.
This requires all daemons on all nodes to be restarted and may take
some time. Continue?
y/[n]/?: y
Fri Mar  1 09:36:27 2024 Renewing SSH keys
All requested certificates and keys have been replaced. Running "gnt-cluster verify" now is recommended.

# After
[root@node01.example.org ~] $ gnt-cluster info | grep -E "rsa|dss|ssh"
  modify ssh setup: True
  ssh_key_type: rsa
  ssh_key_bits: 4096
  ssh_port: 22
```
