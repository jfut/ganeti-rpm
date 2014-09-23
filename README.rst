Ganeti RPM Packaging
====================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

Packaging status
----------------

* RHEL/CentOS/Scientific Linux 6.x: 2.11.6-1
* RHEL/CentOS/Scientific Linux 5.x: 2.6.2-3
* Fedora 20: 2.11.6-1
* Fedora 19: 2.11.6-1

Version 2.11.2 or later: Warning from upstream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  - Improvements to KVM wrt to the kvmd and instance shutdown behavior.
  WARNING: In contrast to our standard policy, this bug fix update
  introduces new parameters to the configuration. This means in
  particular that after an upgrade from 2.11.0 or 2.11.1, 'cfgupgrade'
  needs to be run, either manually or explicitly by running
  'gnt-cluster upgrade --to 2.11.2' (which requires that they 
  had configured the cluster with --enable-full-version).
  This also means, that it is not easily possible to downgrade from 
  2.11.2 to 2.11.1 or 2.11.0. The only way is to go back to 2.10 and
  back.

Build the package
-----------------

* Build all packages::

  ./package.sh -a

* Build the specified package(s) only::

  ./package.sh -p [PACAKGE]

Documentation
--------------

* `Installation and Upgrade guides <https://github.com/jfut/ganeti-rpm/tree/master/doc>`_

Binary RPM files
----------------

RHEL/CentOS/Scientific Linux 6.x, 5.x, and Fedora 19:

- http://jfut.integ.jp/linux/ganeti/

Other Ganeti resources
----------------------

* `The project site <http://code.google.com/p/ganeti/>`_
* `Ganeti's documentation <http://docs.ganeti.org/ganeti/current/html/>`_
