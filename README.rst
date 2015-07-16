Ganeti RPM Packaging
====================

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

Packaging status
----------------

* RHEL/CentOS/Scientific Linux 7.x: 2.14.0-1, 2.13.1-1, 2.12.5-1, and 2.11.7-1
* `RHEL/CentOS/Scientific Linux 6.x: 2.11.7-1 <https://github.com/jfut/ganeti-rpm/tree/el6>`_
* `RHEL/CentOS/Scientific Linux 5.x: 2.6.2-3 <https://github.com/jfut/ganeti-rpm/tree/el5>`_
* `Fedora 20: 2.12.5-1 <https://github.com/jfut/ganeti-rpm/tree/f20>`_
* `Fedora 19: 2.12.5-1 <https://github.com/jfut/ganeti-rpm/tree/f19>`_

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
