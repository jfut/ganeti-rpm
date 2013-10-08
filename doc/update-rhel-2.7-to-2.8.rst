Update Ganeti RPM package from 2.7 to 2.8
=========================================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux.

Update from a version earlier than 2.6
++++++++++++++++++++++++++++++++++++++

If you are updating from a version earlier than 2.6, see the document for 2.7.

* `Update Ganeti RPM package from 2.6 to 2.7 <https://github.com/jfut/ganeti-rpm/blob/master/doc/update-rhel-2.6-to-2.7.rst>`_

Backup
++++++

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

::

  /etc/init.d/ganeti stop
  tar czf /var/lib/ganeti-$(date +%FT%T).tar.gz -C /var/lib ganeti

Update ganeti package
+++++++++++++++++++++

**Mandatory** on all nodes.

::

  yum --enablerepo=epel,integ-ganeti update ganeti

Start ganeti node
+++++++++++++++++

**Mandatory** on member nodes.

::

  /etc/init.d/ganeti start

Update configuration files
++++++++++++++++++++++++++

**Mandatory** on master node.

::

  /usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
  /usr/lib64/ganeti/tools/cfgupgrade --verbose
      This script upgrade the configuration files(/var/lib/ganeti).
  /etc/init.d/ganeti start
  gnt-cluster redist-conf
  /etc/init.d/ganeti restart
  gnt-cluster verify

Fix problems.

ex)::

  gnt-cluster copyfile /etc/ganeti/file-storage-paths
  touch /var/lib/ganeti/ssconf_networks
  gnt-cluster copyfile /var/lib/ganeti/ssconf_networks

