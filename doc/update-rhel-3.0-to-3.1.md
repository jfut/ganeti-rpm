# Update the Ganeti RPM package from 3.0 to 3.1

Ganeti RPM packaging for RHEL/AlmaLinux/Rocky Linux/others.

## Update from a version earlier than 2.16

If you are updating from a version earlier than 2.16, see the 3.0 document instead.

- [Update Ganeti RPM package from 2.16 to 3.0](https://github.com/jfut/ganeti-rpm/blob/main/doc/update-rhel-2.16-to-3.0.md)

Official documentation:

- [Ganeti 3.1.0 Release](https://github.com/ganeti/ganeti/releases/tag/v3.1.0)

## Backup

**Required** on all nodes.

Stop the Ganeti services and backup the configuration directory.

```bash
systemctl stop ganeti-metad.service
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
tar czf /root/ganeti-$(date +%FT%H-%M-%S).tar.gz -C /var/lib ganeti
chmod 600 /root/ganeti-$(date +%FT%H)*.tar.gz
```

## Update the Ganeti package

**Required** on all nodes.

```bash
dnf --enablerepo=integ-ganeti update integ-ganeti-release
dnf --enablerepo=epel,integ-ganeti update ganeti
```

## Upgrade configuration files on the master node

**Required** on the **master** node only.

Upgrade the configuration files in `/var/lib/ganeti`.

```bash
# dry run
/usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run

# upgrade
/usr/lib64/ganeti/tools/cfgupgrade --verbose
```

## Start Ganeti services

**Required** on **member** nodes.

```bash
systemctl start ganeti.target
systemctl start ganeti-kvmd.service

# Optional: ganeti-metad provides the metadata service.
systemctl start ganeti-metad.service
```

**Required** on the **master** node only.

```bash
systemctl start ganeti.target
gnt-cluster redist-conf

systemctl restart ganeti.target
systemctl start ganeti-kvmd.service

# Optional: ganeti-metad provides the metadata service.
systemctl start ganeti-metad.service

gnt-cluster verify
```

**Troubleshooting**

- Restore an old configuration and downgrade Ganeti

You can restore an old configuration from a backup file and then downgrade Ganeti.

```bash
# on all nodes
systemctl stop ganeti-metad.service
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
mv /var/lib/ganeti /var/lib/ganeti.failed
tar zxf /root/ganeti-BACKUP_DATE.tar.gz -C /var/lib

# el8
dnf --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el8
# el9
dnf --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el9
# el10
dnf --enablerepo=epel,integ-ganeti downgrade ganeti-x.y.z-n.el10

systemctl start ganeti.target
systemctl start ganeti-kvmd.service
# Optional: ganeti-metad provides the metadata service.
systemctl start ganeti-metad.service
```
