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

- RHEL/CentOS/Scientific Linux **7.x and later**

```
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
tar czf /var/lib/ganeti-$(date +%FT%T).tar.gz -C /var/lib ganeti
```

## Update ganeti package

**Mandatory** on all nodes.

```
yum --enablerepo=epel,integ-ganeti update ganeti
```

## Start ganeti node

**Mandatory** on member nodes.

- RHEL/CentOS/Scientific Linux **7.x and later**

```
systemctl start ganeti.target
systemctl start ganeti-kvmd.service
```

## Update configuration files

**Mandatory** on master node.

- RHEL/CentOS/Scientific Linux **7.x and later**

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

### Updated X.509 certificate signing algorithm by [Ganeti 2.16.1 Release](https://github.com/ganeti/ganeti/releases/tag/v2.16.1)

Ganeti now uses the SHA-256 digest algorithm to sign all generated X.509 certificates used to secure the RPC communications between nodes. Previously, Ganeti was using SHA-1 which is seen as weak (but not broken) and has been deprecated by most vendors; most notably, OpenSSL — used by Ganeti on some setups — rejects SHA-1-signed certificates when configured to run on security level 2 and above.

Users are advised to re-generate Ganeti's server and node certificates after installing 2.16.1 on all nodes using the following command:

```
# --new-cluster-certificate option includes --new-node-certificates option.
gnt-cluster renew-crypto --new-cluster-certificate
```

On setups using RAPI and/or SPICE with Ganeti-generated certificates, --new-rapi-certificate and --new-spice-certificate should be appended to the command above.

```
gnt-cluster renew-crypto --new-cluster-certificate --new-rapi-certificate --new-spice-certificate
```

