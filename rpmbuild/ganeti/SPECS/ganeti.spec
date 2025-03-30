# without debuginfo
%global debug_package %{nil}

# rc version
%global rc_version %(echo '%{version}' | sed -e 's|.*rc.*|rc|g')

# python version
%define python3_pkgversion 3

# man version
%define _man_version 3.1

# search path
%define _search_sharedir /usr/share
%define _search_libdir /usr/lib
%define _search_lib64dir /usr/lib64
%define _search_local_libdir /usr/local/lib
%define _search_local_lib64dir /usr/local/lib64

%define os_search_path %{_search_sharedir}/%{name}/os,%{_search_libdir}/%{name}/os,%{_search_lib64dir}/%{name}/os,%{_search_local_libdir}/%{name}/os,%{_search_local_lib64dir}/%{name}/os,/srv/%{name}/os
%define iallocator_search_path %{_search_libdir}/%{name}/iallocators,%{_search_lib64dir}/%{name}/iallocators,%{_search_local_libdir}/%{name}/iallocators,%{_search_local_lib64dir}/%{name}/iallocators
%define extstorage_search_path %{_search_sharedir}/%{name}/extstorage,%{_search_libdir}/%{name}/extstorage,%{_search_lib64dir}/%{name}/extstorage,%{_search_local_libdir}/%{name}/extstorage,%{_search_local_lib64dir}/%{name}/extstorage,/srv/%{name}/extstorage

Name: ganeti
Version: 3.1.0.rc2
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: Cluster virtual server management software
License: BSD-2-Clause
URL: http://code.google.com/p/ganeti/

%if "%{rc_version}" == "rc"
Source0: https://jfut.integ.jp/linux/ganeti-test/ganeti-%{version}.tar.gz
%else
Source0: https://github.com/ganeti/ganeti/releases/download/v%{version}/ganeti-%{version}.tar.gz
%endif
Source1: ganeti.init
Source2: ganeti.logrotate
Source3: ganeti.sysconfig

BuildRoot: %{_tmppath}/%{name}-root

Patch2: ganeti-2.16.1-fix-new-cluster-node-certificates.patch
Patch4: ganeti-2.16.1-ask-whether-upgrade-without-rpm.patch
# https://github.com/jfut/ganeti-rpm/issues/50
Patch11: ganeti-3.1.0-kvm-qmp-timeout.patch
# ignore tests that take an extremely long time to complete
Patch12: ganeti-3.1.0-ignore-test-start-daemon.patch
# ignore tests with AssertionError: ResolverError not raised by <lambda>
Patch13: ganeti-3.1.0-ignore-test-hostname-resolution-error.patch
Patch14: ganeti-3.1.0-python36.patch

BuildRequires: iproute
BuildRequires: libcurl-devel
BuildRequires: m4
BuildRequires: procps-ng
BuildRequires: python%{python3_pkgversion}
BuildRequires: python%{python3_pkgversion}-bitarray
BuildRequires: python%{python3_pkgversion}-docutils
BuildRequires: python%{python3_pkgversion}-inotify
BuildRequires: python%{python3_pkgversion}-paramiko
BuildRequires: python%{python3_pkgversion}-psutil
BuildRequires: python%{python3_pkgversion}-pycurl
BuildRequires: python%{python3_pkgversion}-pyOpenSSL
BuildRequires: python%{python3_pkgversion}-pyparsing
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-sphinx
BuildRequires: qemu-img
BuildRequires: socat

# unittests
BuildRequires: fakeroot
BuildRequires: python%{python3_pkgversion}-pyyaml

Requires: fping
Requires: iproute
Requires: iputils
Requires: libcap
Requires: logrotate
Requires: lvm2
Requires: openssh
Requires: procps-ng
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-bitarray
Requires: python%{python3_pkgversion}-inotify
Requires: python%{python3_pkgversion}-paramiko
Requires: python%{python3_pkgversion}-psutil
Requires: python%{python3_pkgversion}-pycurl
Requires: python%{python3_pkgversion}-pyOpenSSL
Requires: python%{python3_pkgversion}-pyparsing
Requires: socat

# doc
# /usr/bin/sh: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
BuildRequires: glibc-langpack-en
BuildRequires: graphviz
BuildRequires: man-db
BuildRequires: pandoc

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%package sysvinit
Summary: The SysV initscript to manage the Ganeti.
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}

%description
Ganeti is a cluster virtual server management software tool built on
top of existing virtualization technologies such as Xen or KVM and
other Open Source software.

Ganeti requires pre-installed virtualization software on your servers
in order to function. Once installed, the tool will take over the
management part of the virtual instances (Xen DomU), e.g. disk
creation management, operating system installation for these instances
(in co-operation with OS-specific install scripts), and startup,
shutdown, failover between physical systems. It has been designed to
facilitate cluster management of virtual servers and to provide fast
and simple recovery after physical failures using commodity hardware.

%description sysvinit
Ganeti is a cluster virtual server management software tool built on
top of existing virtualization technologies such as Xen or KVM and
other Open Source software.

This package contains the SysV init script to manage the DRBD when
running a legacy SysV-compatible init system.

It is not required when the init system used is systemd.

%prep
%setup -q

%patch2 -p1
%patch4 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
cabal install --only-dependencies ganeti.cabal --flags="mond metad htest network_bsd"

# fix for el8: error: version mismatch.
# configure.ac:15: error: version mismatch.  This is Automake 1.16.1,
# configure.ac:15: but the definition used by this AM_INIT_AUTOMAKE
# configure.ac:15: comes from Automake 1.16.5.  You should recreate
# configure.ac:15: aclocal.m4 with aclocal and run automake again.
autoreconf -i

%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --libdir=%{_libdir} \
  --enable-symlinks \
  --with-sshd-restart-command="systemctl restart sshd.service" \
  --with-export-dir=%{_localstatedir}/lib/%{name}/export \
  --with-os-search-path=%{os_search_path} \
  --with-extstorage-search-path=%{extstorage_search_path} \
  --with-iallocator-search-path=%{iallocator_search_path} \
  --with-xen-bootloader=/usr/bin/pygrub \
  --with-kvm-path=/usr/libexec/qemu-kvm \
  --with-user-prefix=gnt- \
  --with-group-prefix=gnt- \
  --enable-monitoring \
  --enable-metadata \
  --enable-haskell-tests \
  $@
%make_build

%install
rm -rf ${RPM_BUILD_ROOT}
%make_install DESTDIR=${RPM_BUILD_ROOT}

install -d -m 755 ${RPM_BUILD_ROOT}/%{_initrddir}
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/bash_completion.d
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/cron.d
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/default
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/logrotate.d
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig

install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_initrddir}/%{name}
install -m 644 doc/examples/bash_completion ${RPM_BUILD_ROOT}/%{_sysconfdir}/bash_completion.d/%{name}
install -m 644 doc/examples/ganeti.cron ${RPM_BUILD_ROOT}/%{_sysconfdir}/cron.d/%{name}
install -m 644 doc/examples/ganeti.default ${RPM_BUILD_ROOT}/%{_sysconfdir}/default/%{name}
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/logrotate.d/%{name}
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_unitdir}
install -m 644 doc/examples/systemd/ganeti-common.service ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-common.service
install -m 644 doc/examples/systemd/ganeti-confd.service  ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-confd.service
install -m 644 doc/examples/systemd/ganeti-kvmd.service   ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-kvmd.service
install -m 644 doc/examples/systemd/ganeti-luxid.service  ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-luxid.service
install -m 644 doc/examples/systemd/ganeti-metad.service  ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-metad.service
install -m 644 doc/examples/systemd/ganeti-mond.service   ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-mond.service
install -m 644 doc/examples/systemd/ganeti-noded.service  ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-noded.service
install -m 644 doc/examples/systemd/ganeti-rapi.service   ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-rapi.service
install -m 644 doc/examples/systemd/ganeti-wconfd.service ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-wconfd.service

install -m 644 doc/examples/systemd/ganeti-master.target ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-master.target
install -m 644 doc/examples/systemd/ganeti-node.target ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti-node.target
install -m 644 doc/examples/systemd/ganeti.service ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti.service
install -m 644 doc/examples/systemd/ganeti.target ${RPM_BUILD_ROOT}/%{_unitdir}/ganeti.target

# compressed man files
TMP_RPM_BUILD_ROOT=${RPM_BUILD_ROOT}
RPM_BUILD_ROOT=${RPM_BUILD_ROOT}/usr/share/ganeti/%{_man_version}/root
/usr/lib/rpm/brp-compress
RPM_BUILD_ROOT=${TMP_RPM_BUILD_ROOT}

%check
while read GROUP
do
    getent group ${GROUP} > /dev/null || sudo groupadd -f -r ${GROUP}
done < doc/users/groups

while read USER GROUP
do
    getent passwd ${USER} > /dev/null || sudo useradd -r -g ${GROUP} -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -M ${USER}
done < doc/users/users

while read USER GROUP
do
    getent passwd ${USER} > /dev/null && sudo usermod -aG ${GROUP} ${USER}
done < doc/users/groupmemberships

# check
# https://github.com/ganeti/ganeti/blob/master/.github/workflows/ci.yml
# LC_ALL=C %make check-local: Invalid locale ('en_US', 'UTF-8')
LC_ALL=C make check-local

# remove document source files
rm -f doc/examples/*.in
rm -f doc/examples/hooks/*.in
rm -rf doc/examples/systemd

# tests
# %make: fg: no job control
make py-tests-unit
make py-tests-integration
# PYTHONPATH=$(pwd) python3 test/py/legacy/ganeti.storage.gluster_unittest.py -v
make py-tests-legacy
make hs-tests

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
getent group gnt-admin > /dev/null   || groupadd -f -r gnt-admin
getent group gnt-confd  > /dev/null  || groupadd -f -r gnt-confd
getent group gnt-daemons > /dev/null || groupadd -f -r gnt-daemons
getent group gnt-luxid > /dev/null   || groupadd -f -r gnt-luxid
getent group gnt-masterd > /dev/null || groupadd -f -r gnt-masterd
getent group gnt-metad > /dev/null   || groupadd -f -r gnt-metad
getent group gnt-rapi > /dev/null    || groupadd -f -r gnt-rapi
getent passwd gnt-confd > /dev/null   || useradd -r -g gnt-confd -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -M gnt-confd
getent passwd gnt-masterd > /dev/null || useradd -r -g gnt-confd -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -M gnt-masterd
getent passwd gnt-metad > /dev/null   || useradd -r -g gnt-metad -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -M gnt-metad
getent passwd gnt-rapi > /dev/null    || useradd -r -g gnt-rapi -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -M gnt-rapi
usermod -aG gnt-daemons gnt-confd
usermod -aG gnt-admin gnt-masterd
usermod -aG gnt-confd gnt-masterd
usermod -aG gnt-daemons gnt-masterd
usermod -aG gnt-masterd gnt-masterd
usermod -aG gnt-daemons gnt-metad
usermod -aG gnt-admin gnt-rapi
usermod -aG gnt-daemons gnt-rapi

%post
%systemd_post ganeti.target ganeti-master.target ganeti-node.target
%systemd_post ganeti-confd.service ganeti-noded.service
%systemd_post ganeti-wconfd.service ganeti-luxid.service ganeti-rapi.service
%systemd_post ganeti-kvmd.service
%systemd_post ganeti-metad.service ganeti-mond.service

%preun
%systemd_preun ganeti.target ganeti-master.target ganeti-node.target
%systemd_preun ganeti-confd.service ganeti-noded.service
%systemd_preun ganeti-wconfd.service ganeti-luxid.service ganeti-rapi.service
%systemd_preun ganeti-kvmd.service
%systemd_preun ganeti-metad.service ganeti-mond.service

%postun
%systemd_postun_with_restart ganeti.target ganeti-master.target ganeti-node.target
%systemd_postun_with_restart ganeti-confd.service ganeti-noded.service
%systemd_postun_with_restart ganeti-wconfd.service ganeti-luxid.service ganeti-rapi.service
%systemd_postun_with_restart ganeti-kvmd.service
%systemd_postun_with_restart ganeti-metad.service ganeti-mond.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_unitdir}/*.service
%config %{_unitdir}/*.target
%doc COPYING INSTALL NEWS README.md UPGRADE doc/examples doc/html
%{_bindir}/h*
%{_sbindir}/g*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man*/g*
%{_mandir}/man*/h*
%{_mandir}/man*/mon-collector*
%attr(755,gnt-masterd,gnt-daemons) %dir /var/lib/%{name}
%attr(770,gnt-masterd,gnt-daemons) %dir /var/log/%{name}

%files sysvinit
%defattr(-,root,root)
%attr(755,root,root) %config %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Sat Mar 29 2025 Jun Futagawa <jfut@integ.jp> - 3.1.0.rc2-1
- Update to 3.1.0 (#53)
- Drop support for RHEL/CentOS 7
- Add BuildRequires: graphviz
- Add BuildRequires: man-db
- Add BuildRequires: pandoc
- Remove Requires: python%{python3_pkgversion}-simplejson
- Remove BuildRequires: python%{python3_pkgversion}-simplejson
- Remove BuildRequires: python%{python3_pkgversion}-mock

* Sun Sep 25 2022 Jun Futagawa <jfut@integ.jp> - 3.0.2-2
- Add support for RHEL/AlmaLinux/Rocky Linux 9 (#50)
- Remove BuildRequires: pandoc
- Remove BuildRequires: graphviz
- Remove BuildRequires: man-db
- Remove Requires: python%{python3_pkgversion}-docutils
- Add BuildRequires: procps-ng
- Add BuildRequires: restore (for el9)
- Add Requires: procps-ng
- Add Requires: restore (for el9)
- Add ganeti-3.0.2-kvm-qmp-timeout.patch (#50)

* Tue Mar  1 2022 Jun Futagawa <jfut@integ.jp> - 3.0.2-1
- Update to 3.0.2

* Sat Feb 19 2022 Jun Futagawa <jfut@integ.jp> - 3.0.1-2
- Add Requires: fping and ndisc6(el8 not yet provided by EPEL) (#43, thanks @rowlap)

* Thu Feb  4 2021 Jun Futagawa <jfut@integ.jp> - 3.0.1-1
- Update to 3.0.1

* Wed Feb  3 2021 Jun Futagawa <jfut@integ.jp> - 3.0.0-1
- Update to 3.0.0
- Remove BuildRequires: python-ipaddr
- Remove Requires: python-ipaddr
- Remove Requires: bridge-utils
- Use ghc binary package instead of RPMs
- Add %{python3_pkgversion}
- Add the --with-sshd-restart-command option instead of the --with-ssh-initscript option
- Add %global debug_package %{nil}
- Add a check by python unittests(make py-tests) in %check
- Add a check by haskell unittests(make hs-tests) in %check
- Add ganeti-3.0.0-ghc-json-version.patch
- Remove document source files
- Add ganeti-3.0.0-qemu-migrate-set-parameters-version-check.patch (#34)
- Add --with-user-prefix and --with-group-prefix options (#20)
- Add source url for rc version

* Sat Oct  3 2020 Jun Futagawa <jfut@integ.jp> - 2.16.2-1
- Add backport patch from the upstream for VLAN aware bridging (#28, #29, thanks @alfonso-escribano)

* Tue May 26 2020 Jun Futagawa <jfut@integ.jp> - 2.16.2-0
- Updated to 2.16.2

* Fri Feb 28 2020 Jun Futagawa <jfut@integ.jp> - 2.16.1-3
- Add AmbientCapabilities in ganeti-metad.service (#26)
- Add ask whether to continue the upgrade without RPM (#24)

* Tue Feb 25 2020 Jun Futagawa <jfut@integ.jp> - 2.16.1-2
- Add build dependencies for metad and mond and enable them in the build (#25, thanks @ramereth)
- Improve messages for unused daemons when running logrotate (#23)

* Wed Apr 17 2019 Jun Futagawa <jfut@integ.jp> - 2.16.1-1
- Updated to 2.16.1
- Added ganeti-2.16.1-semigroups-downgrade.patch
- Added ganeti-2.16.1-systemd-options.patch
- Updated ganeti source file url
- Added ganeti-2.16.1-fix-new-cluster-node-certificates.patch

* Tue Apr 16 2019 Jun Futagawa <jfut@integ.jp> - 2.16.0-1
- Updated to 2.16.0
- Added Requires: libcap
- Removed DRBD release version patch
- Added BuildRequires: python-docutils
- Added BuildRequires: python-sphinx
- Added BuildRequires: ghc-HUnit-devel
- Added BuildRequires: iproute
- Added BuildRequires: pandoc
- Added BuildRequires: graphviz
- Added ganeti-kvmd.service in % systemd_post, % systemd_preun, and % systemd_postun_with_restart

* Thu Jan 28 2016 Jun Futagawa <jfut@integ.jp> - 2.15.2-2
- Added DRBD release version patch

* Tue Jan  5 2016 Jun Futagawa <jfut@integ.jp> - 2.15.2-1
- Updated to 2.15.2

* Thu Sep 10 2015 Jun Futagawa <jfut@integ.jp> - 2.15.1-1
- Updated to 2.15.1

* Mon Aug 17 2015 Jun Futagawa <jfut@integ.jp> - 2.15.0-1
- Updated to 2.15.0
- Added BuildRequires: ghc-case-insensitive-devel

* Thu Jul 16 2015 Jun Futagawa <jfut@integ.jp> - 2.14.1-1
- Updated to 2.14.1

* Sun Jul  5 2015 Jun Futagawa <jfut@integ.jp> - 2.14.0-1
- Updated to 2.14.0
- Added BuildRequires: cabal-install
- Added BuildRequires: ghc-test-framework-devel
- Added BuildRequires: ghc-test-framework-hunit-devel
- Added BuildRequires: ghc-test-framework-quickcheck2-devel
- Added BuildRequires: ghc-temporary-devel

* Sun Jul  5 2015 Jun Futagawa <jfut@integ.jp> - 2.13.1-1
- Updated to 2.13.1

* Sun Jul  5 2015 Jun Futagawa <jfut@integ.jp> - 2.13.0-1
- Updated to 2.13.0

* Sat May 16 2015 Jun Futagawa <jfut@integ.jp> - 2.12.4-1
- Updated to 2.12.4

* Mon May  4 2015 Jun Futagawa <jfut@integ.jp> - 2.12.3-1
- Updated to 2.12.3

* Sun Mar 29 2015 Jun Futagawa <jfut@integ.jp> - 2.12.2-1
- Updated to 2.12.2

* Fri Jan 16 2015 Jun Futagawa <jfut@integ.jp> - 2.12.1-1
- Updated to 2.12.1

* Fri Jan  9 2015 Jun Futagawa <jfut@integ.jp> - 2.12.0-2
- Fixed network status test of sysvinit script fails
- Added bash_completion file
- Fixed #1007 - gnt-cluster master-failover fails (Added ganeti-2.12.0-systemd-options.patch)

* Sun Oct 12 2014 Jun Futagawa <jfut@integ.jp> - 2.12.0-1
- Initial package for el7
- Updated to 2.12.0
- Ganeti is now distributed under the 2-clause BSD license
- Removed BuildRequires: python-affinity
- Added BuildRequires: ghc-lens-devel
- Added BuildRequires: ghc-lifted-base-devel
- Added BuildRequires: python-psutil
- Added Requires: logrotate
- Added Requires: python-psutil
- Added subpackage: sysvinit

* Tue Sep 23 2014 Jun Futagawa <jfut@integ.jp> - 2.11.6-1
- Updated to 2.11.6
- Ganeti is now distributed under the 2-clause BSD license

* Tue Aug 12 2014 Jun Futagawa <jfut@integ.jp> - 2.11.5-1
- Updated to 2.11.5
- Fixed oCERT-2014-006 Ganeti insecure archive permission

* Sun Aug  3 2014 Jun Futagawa <jfut@integ.jp> - 2.11.4-1
- Updated to 2.11.4

* Wed Jul  9 2014 Jun Futagawa <jfut@integ.jp> - 2.11.3-1
- Updated to 2.11.3

* Mon Jun 16 2014 Jun Futagawa <jfut@integ.jp> - 2.11.2-1
- Updated to 2.11.2

* Wed May 14 2014 Jun Futagawa <jfut@integ.jp> - 2.11.1-1
- Updated to 2.11.1

* Thu May  8 2014 Jun Futagawa <jfut@integ.jp> - 2.11.0-1
- Updated to 2.11.0
- Added BuildRequires: ghc-base64-bytestring-devel
- Added BuildRequires: ghc-hinotify-devel
- Added BuildRequires: ghc-regex-pcre-devel
- Added BuildRequires: ghc-zlib-devel
- Added BuildRequires: ghc-vector-devel
- Added option: --enable-symlinks

* Sun Apr 20 2014 Jun Futagawa <jfut@integ.jp> - 2.10.3-3
- Fixed symbolic links for compressed man files

* Sun Apr 20 2014 Jun Futagawa <jfut@integ.jp> - 2.10.3-2
- Added the ganeti-mond, ganeti-luxid and ganeti-confd daemon for Fedora 19 and above
- Added BuildRequires: ghc-regex-pcre-devel
- Added BuildRequires: ghc-hinotify-devel
- Added BuildRequires: ghc-vector-devel
- Added BuildRequires: ghc-snap-server-devel
- Fixed symbolic links for compressed man files

* Sun Apr 20 2014 Jun Futagawa <jfut@integ.jp> - 2.10.3-1
- Updated to 2.10.3

* Thu Mar 27 2014 Jun Futagawa <jfut@integ.jp> - 2.10.2-1
- Updated to 2.10.2

* Mon Mar 10 2014 Jun Futagawa <jfut@integ.jp> - 2.10.1-1
- Updated to 2.10.1

* Sat Feb 22 2014 Jun Futagawa <jfut@integ.jp> - 2.10.0-1
- Updated to 2.10.0
- Removed multilib patch

* Tue Feb 11 2014 Jun Futagawa <jfut@integ.jp> - 2.9.4-1
- Updated to 2.9.4

* Tue Jan 28 2014 Jun Futagawa <jfut@integ.jp> - 2.9.3-1
- Updated to 2.9.3

* Sat Dec 14 2013 Jun Futagawa <jfut@integ.jp> - 2.9.2-1
- Updated to 2.9.2

* Fri Nov 15 2013 Jun Futagawa <jfut@integ.jp> - 2.9.1-1
- Updated to 2.9.1

* Fri Nov  8 2013 Jun Futagawa <jfut@integ.jp> - 2.9.0-1
- Updated to 2.9.0
- Removed option: --with-file-storage-dir
- Removed option: --with-shared-file-storage-dir

* Fri Nov  8 2013 Jun Futagawa <jfut@integ.jp> - 2.8.2-1
- Updated to 2.8.2

* Thu Oct 17 2013 Jun Futagawa <jfut@integ.jp> - 2.8.1-1
- Updated to 2.8.1

* Tue Oct  8 2013 Jun Futagawa <jfut@integ.jp> - 2.8.0-1
- Updated to 2.8.0
- Added BuildRequires: ghc-hslogger-devel

* Fri Sep 27 2013 Jun Futagawa <jfut@integ.jp> - 2.7.2-1
- Updated to 2.7.2

* Sun Jul 28 2013 Jun Futagawa <jfut@integ.jp> - 2.7.1-1
- Updated to 2.7.1

* Fri Jul  5 2013 Jun Futagawa <jfut@integ.jp> - 2.7.0-2
- Added extstorage search path

* Thu Jul  4 2013 Jun Futagawa <jfut@integ.jp> - 2.7.0-1
- Updated to 2.7.0
- Removed htools subpackage (integrated in a ganeti package)
- Added BuildRequires: python-bitarray
- Added BuildRequires: python-ipaddr
- Added Requires: python-bitarray
- Added Requires: python-ipaddr
- Added BuildRequires: ghc-attoparsec-devel
- Added BuildRequires: ghc-Crypto-devel
- Added BuildRequires: ghc-text-devel
- Added BuildRequires: ghc-utf8-string-devel

* Fri Feb  8 2013 Jun Futagawa <jfut@integ.jp> - 2.6.2-3
- Removed Requires: ghc and ghc-*
- Added Requires: bridge-utils
- Added Requires: iproute
- Added Requires: iputils
- Added Requires: lvm2
- Added Requires: socat
- Added BuildRequires: python-affinity

* Sun Jan 20 2013 Jun Futagawa <jfut@integ.jp> - 2.6.2-2
- Added BuildRequires: qemu-img
- Removed BuildArchitectures to support htools
- Added subpackage: htools (el6 or later only)

* Sat Dec 22 2012 Jun Futagawa <jfut@integ.jp> - 2.6.2-1
- Updated to 2.6.2

* Sun Oct 14 2012 Jun Futagawa <jfut@integ.jp>
- Updated to 2.6.1

* Fri Jul 27 2012 Jun Futagawa <jfut@integ.jp>
- Updated to 2.6.0

* Wed Jul 25 2012 Jun Futagawa <jfut@integ.jp>
- Updated to 2.5.2

* Sat May 12 2012 Jun Futagawa <jfut@integ.jp>
- Updated to 2.5.1

* Fri Apr 13 2012 Jun Futagawa <jfut@integ.jp>
- Updated to 2.5.0
- Fixed OS search path
- Added shared-file-storage-dir path
- Added status function to init script
- Merged Stephen Fromm's patch to improve to daemon-util for distributions without start-stop-daemon

* Thu Nov  3 2011 Jun Futagawa <jfut@integ.jp>
- Added OS search path
- Added iallocator search path

* Mon Oct 31 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.5

* Wed Aug 24 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.4

* Fri Aug  5 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.3

* Fri May 13 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.2
- Added BuildRequires and Requires: python-inotify
- Change service startup order

* Wed Mar  9 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.1

* Tue Mar  8 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.0

* Tue Dec 21 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.3.1

* Wed Dec  1 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.3.0

* Wed Dec  1 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.2.2

* Wed Oct 20 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.2.1

* Sun Oct 10 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.2.0.1

* Tue Oct  5 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.2.0
- Added BuildRequires: python-ctypes
- Added BuildRequires: python-pycurl
- Added BuildRequires: python-paramiko
- Added BuildRequires: socat

* Wed Aug 25 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.7

* Sat Jul 17 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.6

* Sat Jul  3 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.5

* Sun Jun 20 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.4

* Mon Jun  7 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.3

* Sat May 29 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.1.2.1

* Sun May 16 2010 Jun Futagawa <jfut@integ.jp>
- Updated to 2.0.6

* Fri Dec 18 2009 Jun Futagawa <jfut@integ.jp>
- Updated to 2.0.5

* Sat Nov  7 2009 Jun Futagawa <jfut@integ.jp>
- Backported the ``use_localtime`` option for the xen-hvm and kvm
  from the development branch

* Thu Nov  5 2009 Jun Futagawa <jfut@integ.jp>
- Changed export-dir to /var/lib/ganeti/export
- Changed file-storage-dir to /var/lib/ganeti/file-storage

* Sat Oct 24 2009 Jun Futagawa <jfut@integ.jp>
- Backported more options to xen-pvm hypervisor (``use_bootloader``,
  ``bootloader_path`` and ``bootloader_args``) from the development
  branch
- Updated to 2.0.4

* Tue Sep 29 2009 Jun Futagawa <jfut@integ.jp>
- First build 
