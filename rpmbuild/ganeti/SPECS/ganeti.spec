%{!?os_ver: %define os_ver %(Z=`rpm -q --whatprovides /etc/redhat-release`;rpm -q --qf '%{V}' $Z | sed 's/\\.[0-9]*//')}

# search path
%define _search_sharedir /usr/share
%define _search_libdir /usr/lib
%define _search_lib64dir /usr/lib64
%define _search_local_libdir /usr/local/lib
%define _search_local_lib64dir /usr/local/lib64

%define os_search_path %{_search_sharedir}/%{name}/os,%{_search_libdir}/%{name}/os,%{_search_lib64dir}/%{name}/os,%{_search_local_libdir}/%{name}/os,%{_search_local_lib64dir}/%{name}/os,/srv/%{name}/os
%define iallocator_search_path %{_search_libdir}/%{name}/iallocators,%{_search_lib64dir}/%{name}/iallocators,%{_search_local_libdir}/%{name}/iallocators,%{_search_local_lib64dir}/%{name}/iallocators
%define extstorage_search_path %{_search_sharedir}/%{name}/extstorage,%{_search_libdir}/%{name}/extstorage,%{_search_lib64dir}/%{name}/extstorage,%{_search_local_libdir}/%{name}/extstorage,%{_search_local_lib64dir}/%{name}/extstorage,/srv/%{name}/extstorage

# man version
%define _man_version 2.11

Name: ganeti
Version: 2.11.1
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: Cluster virtual server management software
License: GPLv2
URL: http://code.google.com/p/ganeti/

Source0: http://ganeti.googlecode.com/files/ganeti-%{version}.tar.gz
Source1: ganeti.init
Source2: ganeti.sysconfig

BuildRoot: %{_tmppath}/%{name}-root

Patch1: ganeti-2.11.0-fedora.patch

BuildRequires: python
BuildRequires: pyOpenSSL
BuildRequires: pyparsing
BuildRequires: python-affinity 
BuildRequires: python-bitarray
BuildRequires: python-inotify
BuildRequires: python-ipaddr
BuildRequires: python-simplejson
%if %{os_ver} == 5
BuildRequires: python-ctypes
%endif
BuildRequires: python-pycurl
BuildRequires: python-paramiko
BuildRequires: qemu-img
BuildRequires: socat
# htools support: el6 or later only
%if %{os_ver} >= 6
BuildRequires: ghc
BuildRequires: ghc-attoparsec-devel
BuildRequires: ghc-base64-bytestring-devel
BuildRequires: ghc-Crypto-devel
BuildRequires: ghc-curl-devel
BuildRequires: ghc-network-devel
BuildRequires: ghc-hinotify-devel
BuildRequires: ghc-hslogger-devel
BuildRequires: ghc-json-devel
BuildRequires: ghc-parallel-devel
BuildRequires: ghc-QuickCheck-devel
BuildRequires: ghc-regex-pcre-devel
BuildRequires: ghc-text-devel
BuildRequires: ghc-utf8-string-devel
BuildRequires: ghc-vector-devel
BuildRequires: ghc-zlib-devel
BuildRequires: libcurl-devel
%endif
%if %{os_ver} >= 19
BuildRequires: ghc-vector-devel
BuildRequires: ghc-snap-server-devel
%endif

Requires: bridge-utils
Requires: iproute
Requires: iputils
Requires: lvm2
Requires: openssh
Requires: python
Requires: pyOpenSSL
Requires: pyparsing
Requires: python-bitarray
Requires: python-inotify
Requires: python-ipaddr
Requires: python-simplejson
%if %{os_ver} == 5
Requires: python-ctypes
%endif
Requires: python-pycurl
Requires: python-paramiko
Requires: socat

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

%prep
%setup -q

%patch1 -p1

%build
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --libdir=%{_libdir} \
  --enable-symlinks \
  --with-ssh-initscript=%{_initrddir}/sshd \
  --with-export-dir=%{_localstatedir}/lib/%{name}/export \
  --with-os-search-path=%{os_search_path} \
  --with-extstorage-search-path=%{extstorage_search_path} \
  --with-iallocator-search-path=%{iallocator_search_path} \
  --with-xen-bootloader=/usr/bin/pygrub \
  --with-kvm-path=/usr/libexec/qemu-kvm \
  $@
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}/%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/default
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig

install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_initrddir}/%{name}
install -m 644 doc/examples/ganeti.default ${RPM_BUILD_ROOT}/%{_sysconfdir}/default/%{name}
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig/%{name}

# compressed man files
TMP_RPM_BUILD_ROOT=${RPM_BUILD_ROOT}
RPM_BUILD_ROOT=${RPM_BUILD_ROOT}/usr/share/ganeti/%{_man_version}/root
/usr/lib/rpm/redhat/brp-compress
RPM_BUILD_ROOT=${TMP_RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/chkconfig --add ganeti

%preun
if [ $1 = 0 ] ; then
    /sbin/chkconfig --del ganeti
    /sbin/service ganeti stop >/dev/null 2>&1
fi
exit 0

%files
%defattr(-,root,root)
%attr(755,root,root) %config %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%doc COPYING INSTALL NEWS README UPGRADE doc/
%{_bindir}/h*
%{_sbindir}/g*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man*/g*
%{_mandir}/man*/h*
%{_mandir}/man*/mon-collector*
%attr(750,root,root) %dir /var/lib/%{name}
%attr(750,root,root) %dir /var/log/%{name}

%changelog
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
