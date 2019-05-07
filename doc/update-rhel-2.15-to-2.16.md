# Update Ganeti RPM package from 2.15 to 2.16

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

## Update from a version earlier than 2.14

If you are updating from a version earlier than 2.14, see the document for 2.15.

- [Update Ganeti RPM package from 2.14 to 2.15](https://github.com/jfut/ganeti-rpm/blob/master/doc/update-rhel-2.14-to-2.15.rst)

Official documentation:

- [Ganeti 2.16.1 Release](https://github.com/ganeti/ganeti/releases/tag/v2.16.1)
- [Ganeti's documentation](http://docs.ganeti.org/ganeti/current/html/) > [Upgrade notes](http://docs.ganeti.org/ganeti/current/html/upgrade.html)

## Backup

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

```
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
tar czf /root/ganeti-$(date +%FT%H-%M-%S).tar.gz -C /var/lib ganeti
chmod 600 /root/ganeti-$(date +%FT%H)*.tar.gz
```

## Update ganeti package

**Mandatory** on all nodes.

```
yum --enablerepo=epel,integ-ganeti update ganeti
```

## Start ganeti node

**Mandatory** on member nodes only.

```
systemctl start ganeti.target
systemctl start ganeti-kvmd.service
```

## Update configuration files

**Mandatory** on master node only.

```
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
/usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
/usr/lib64/ganeti/tools/cfgupgrade --verbose
    This script upgrade the configuration files(/var/lib/ganeti).
systemctl start ganeti.target
gnt-cluster redist-conf
systemctl restart ganeti.target
systemctl start ganeti-kvmd.service
gnt-cluster verify
```

**Troubleshooting**

- 'Can't find node' messages

You can ignore the 'Can't find node' messages and continue.

```
# /usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
Please make sure you have read the upgrade notes for Ganeti 2.16.1
(available in the UPGRADE file and included in other documentation
formats). Continue with upgrading configuration?
y/[n]/?: y
2019-05-07 17:55:14,887: Found configuration version 2150000 (2.15.0)
2019-05-07 17:55:14,887: Creating symlink from /var/lib/ganeti/rapi_users to /var/lib/ganeti/rapi/users
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node '69e8385f-cb86-4ca0-845d-1358f51c92a6' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,898: Can't find node 'ac3197a9-4770-4efe-9087-4d41d8e31695' in configuration, assuming that it's already up-to-date
2019-05-07 17:55:14,903: Writing configuration file to /var/lib/ganeti/config.data
Configuration successfully upgraded to version 2.16.1.
```

- Restore an old configuration

You can restore an old configuration from a backup file.

```
# on all nodes
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
mv /var/lib/ganeti /var/lib/ganeti.failed
tar zxf /root/ganeti-BACKUP_DATE.tar.gz -C /var/lib

yum downgrade ganeti-2.x.y-z.el7

systemctl start ganeti.target
systemctl start ganeti-kvmd.service
```

### Updated X.509 certificate signing algorithm by [Ganeti 2.16.1 Release](https://github.com/ganeti/ganeti/releases/tag/v2.16.1)

Ganeti now uses the SHA-256 digest algorithm to sign all generated X.509 certificates used to secure the RPC communications between nodes. Previously, Ganeti was using SHA-1 which is seen as weak (but not broken) and has been deprecated by most vendors; most notably, OpenSSL — used by Ganeti on some setups — rejects SHA-1-signed certificates when configured to run on security level 2 and above.

Users are advised to re-generate Ganeti's server and node certificates after installing 2.16.1 on all nodes using the following command:

```
# --new-cluster-certificate option includes --new-node-certificates option.
gnt-cluster renew-crypto --new-cluster-certificate

# check new certificates
openssl x509 -in /var/lib/ganeti/server.pem -noout -text
openssl x509 -in /var/lib/ganeti/client.pem -noout -text
```

On setups using RAPI and/or SPICE with Ganeti-generated certificates, it should also re-generate them using the following command:

```
gnt-cluster renew-crypto --new-rapi-certificate --new-spice-certificate
```

