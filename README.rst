Ganeti RPM Packaging for f20
============================

Ganeti RPM Packaging for Fedora 20.

Packaging status
----------------

* Fedora 20: 2.12.5-1
* `Other distribution version <https://github.com/jfut/ganeti-rpm/>`_

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

* Remove ghc-test-framework-quickcheck2 package::

  yum remove ghc-test-framework-quickcheck2-devel

* Build all packages::

  ./package.sh -a

* Build the specified package(s) only::

  ./package.sh -p [PACAKGE]

* Re-install ghc-test-framework-quickcheck2 package::

  yum --enablerepo=epel,integ-ganeti install ghc-test-framework-quickcheck2-devel

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
