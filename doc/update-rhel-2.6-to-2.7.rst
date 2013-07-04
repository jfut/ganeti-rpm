From 2.6 to 2.7
===============

Backup
++++++

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

::

  /etc/init.d/ganeti stop
  tar czf /var/lib/ganeti-$(date +%FT%T).tar.gz -C /var/lib ganeti

Remove ganeti-htools subpackage
+++++++++++++++++++++++++++++++

**Mandatory** on all nodes.

The htools package was integrated in the ganeti package.

  rpm -e ganeti-htools

Update ganeti package
+++++++++++++++++++++

**Mandatory** on all nodes.

::

  yum --enablerepo=epel,integ-ganeti update ganeti

Update the configuration file
+++++++++++++++++++++++++++++

**Mandatory** on master node.

::

  /usr/lib/ganeti/tools/cfgupgrade --verbose --dry-run
  /usr/lib/ganeti/tools/cfgupgrade --verbose
      This script upgrade the configuration files(/var/lib/ganeti).
  /etc/init.d/ganeti start
  gnt-cluster redist-conf
  /etc/init.d/ganeti restart
  gnt-cluster verify

Fix problems.

ex)::

  gnt-cluster copyfile /var/lib/ganeti/config.data
  gnt-cluster copyfile /etc/ganeti/file-storage-paths
  touch /var/lib/ganeti/ssconf_networks

