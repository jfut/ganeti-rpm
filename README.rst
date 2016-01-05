Ganeti RPM Packaging
====================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

Packaging status
----------------

* RHEL/CentOS/Scientific Linux 7.x for 2.13.x: 2.13.3-1
* `Other distribution version <https://github.com/jfut/ganeti-rpm/>`_

Version 2.13.3: Important changes and security notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  CVE-2015-7944
  
  Ganeti provides a RESTful control interface called the RAPI. Its HTTPS
  implementation is vulnerable to DoS attacks via client-initiated SSL
  parameter renegotiation. While the interface is not meant to be exposed
  publicly, due to the fact that it binds to all interfaces, we believe
  some users might be exposing it unintentionally and are vulnerable. A
  DoS attack can consume resources meant for Ganeti daemons and instances
  running on the master node, making both perform badly.
  
  Fixes are not feasible due to the OpenSSL Python library not exposing
  functionality needed to disable client-side renegotiation. Instead, we
  offer instructions on how to control RAPI's exposure, along with info
  on how RAPI can be setup alongside an HTTPS proxy in case users still
  want or need to expose the RAPI interface. The instructions are
  outlined in Ganeti's security document: doc/html/security.html
  
  CVE-2015-7945
  
  Ganeti leaks the DRBD secret through the RAPI interface. Examining job
  results after an instance information job reveals the secret. With the
  DRBD secret, access to the local cluster network, and ARP poisoning,
  an attacker can impersonate a Ganeti node and clone the disks of a
  DRBD-based instance. While an attacker with access to the cluster
  network is already capable of accessing any data written as DRBD
  traffic is unencrypted, having the secret expedites the process and
  allows access to the entire disk.
  
  Fixes contained in this release prevent the secret from being exposed
  via the RAPI. The DRBD secret can be changed by converting an instance
  to plain and back to DRBD, generating a new secret, but redundancy will
  be lost until the process completes.
  Since attackers with node access are capable of accessing some and
  potentially all data even without the secret, we do not recommend that
  the secret be changed for existing instances.

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

- http://jfut.integ.jp/linux/ganeti/

Other Ganeti resources
----------------------

* `The project site <http://code.google.com/p/ganeti/>`_
* `Ganeti's documentation <http://docs.ganeti.org/ganeti/current/html/>`_

Contributing
------------

1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request
