# Update Ganeti RPM package from 3.0 to 3.1

Ganeti RPM Packaging for RHEL/CentOS/others.

## Update from a version earlier than 2.16

If you are updating from a version earlier than 2.16, see the document for 3.0.

- [Update Ganeti RPM package from 2.16 to 3.0](https://github.com/jfut/ganeti-rpm/blob/master/doc/update-rhel-2.16-to-3.0.rst)

Official documentation:

- [Ganeti 3.1.0 Release](https://github.com/ganeti/ganeti/releases/tag/v3.1.0)

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
Please make sure you have read the upgrade notes for Ganeti 3.1.0
(available in the UPGRADE file and included in other documentation
formats). Continue with upgrading configuration?
y/[n]/?: y
2025-09-24 20:48:42,530: Found configuration version 3010000 (3.1.0)
2025-09-24 20:48:42,531: No changes necessary
2025-09-24 20:48:42,531: Writing configuration file to /var/lib/ganeti/config.data
Configuration successfully upgraded to version 3.1.0.
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

# el8
yum --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el8
# el9
yum --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el9
# el10
yum --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el10

systemctl start ganeti.target
systemctl start ganeti-kvmd.service
# Optional: ganeti-metad is the daemon providing the metadata service.
systemctl start ganeti-metad.service
```
