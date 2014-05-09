Update Ganeti RPM package from 2.10 to 2.11
==========================================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

Update from a version earlier than 2.9
++++++++++++++++++++++++++++++++++++++

If you are updating from a version earlier than 2.9, see the document for 2.10.

* `Update Ganeti RPM package from 2.9 to 2.10 <https://github.com/jfut/ganeti-rpm/blob/master/doc/update-rhel-2.9-to-2.10.rst>`_

Official full version:

* `Ganeti's documentation <http://docs.ganeti.org/ganeti/current/html/>`_ >> `Upgrade notes <http://docs.ganeti.org/ganeti/current/html/upgrade.html>`_

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
  gnt-cluster renew-crypto --new-node-certificates
  gnt-cluster verify

Fix problems.

ex)::

  gnt-cluster renew-crypto --new-node-certificates

