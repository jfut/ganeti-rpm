Update Ganeti RPM package from 2.11 to 2.12
===========================================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

Update from a version earlier than 2.10
+++++++++++++++++++++++++++++++++++++++

If you are updating from a version earlier than 2.10, see the document for 2.11.

* `Update Ganeti RPM package from 2.10 to 2.11 <https://github.com/jfut/ganeti-rpm/blob/main/doc/update-rhel-2.10-to-2.11.rst>`_

Official full version:

* `Ganeti's documentation <http://docs.ganeti.org/ganeti/current/html/>`_ >> `Upgrade notes <http://docs.ganeti.org/ganeti/current/html/upgrade.html>`_

Backup
++++++

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

- RHEL/CentOS/Scientific Linux **7.x and later**

::

  systemctl stop ganeti.target
  tar czf /var/lib/ganeti-$(date +%FT%T).tar.gz -C /var/lib ganeti

- RHEL/CentOS/Scientific Linux **6.x**

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

- RHEL/CentOS/Scientific Linux **7.x and later**

::

  systemctl start ganeti.target

- RHEL/CentOS/Scientific Linux **6.x**

::

  /etc/init.d/ganeti start

Update configuration files
++++++++++++++++++++++++++

**Mandatory** on master node.

- RHEL/CentOS/Scientific Linux **7.x and later**

::

  /usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
  /usr/lib64/ganeti/tools/cfgupgrade --verbose
      This script upgrade the configuration files(/var/lib/ganeti).
  systemctl start ganeti.target
  gnt-cluster redist-conf
  systemctl restart ganeti.target
  gnt-cluster verify

- RHEL/CentOS/Scientific Linux **6.x**

::

  /usr/lib64/ganeti/tools/cfgupgrade --verbose --dry-run
  /usr/lib64/ganeti/tools/cfgupgrade --verbose
      This script upgrade the configuration files(/var/lib/ganeti).
  /etc/init.d/ganeti start
  gnt-cluster redist-conf
  /etc/init.d/ganeti restart
  gnt-cluster verify

