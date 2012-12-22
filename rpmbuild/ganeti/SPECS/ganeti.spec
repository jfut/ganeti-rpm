%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{!?os_ver: %define os_ver %(Z=`rpm -q --whatprovides /etc/redhat-release`;A=`rpm -q --qf '%{V}' $Z`; echo ${A:0:1})}

%define _libdir /usr/lib
%define _lib64dir /usr/lib64
%define _local_libdir /usr/local/lib
%define _local_lib64dir /usr/local/lib64

%define os_search_path /usr/share/%{name}/os,%{_libdir}/%{name}/os,%{_lib64dir}/%{name}/os,%{_local_libdir}/%{name}/os,%{_local_lib64dir}/%{name}/os,/srv/%{name}/os
%define iallocator_search_path %{_libdir}/%{name}/iallocators,%{_lib64dir}/%{name}/iallocators,%{_local_libdir}/%{name}/iallocators,%{_local_lib64dir}/%{name}/iallocators

Summary: Cluster-based virtualization management software
Name: ganeti
Version: 2.6.2
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://code.google.com/p/ganeti/
Source0: http://ganeti.googlecode.com/files/ganeti-%{version}.tar.gz
Source1: ganeti.init
Source2: ganeti.sysconfig
BuildArchitectures: noarch
BuildRequires: python
BuildRequires: pyOpenSSL
BuildRequires: pyparsing
BuildRequires: python-inotify
BuildRequires: python-simplejson
%if %{os_ver} == 5
BuildRequires: python-ctypes
%endif
BuildRequires: python-pycurl
BuildRequires: python-paramiko
BuildRequires: socat
BuildRoot: %{_tmppath}/%{name}-root
Requires: python
Requires: pyOpenSSL
Requires: pyparsing
Requires: python-inotify
Requires: python-simplejson
%if %{os_ver} == 5
Requires: python-ctypes
%endif
Requires: python-pycurl
Requires: python-paramiko

%description
Ganeti is a virtualization cluster management software. You are expected
to be a system administrator familiar with your Linux distribution and
the Xen or KVM virtualization environments before using it.

The various components of Ganeti all have man pages and interactive
help. This manual though will help you getting familiar with the system
by explaining the most common operations, grouped by related use.

After a terminology glossary and a section on the prerequisites needed
to use this manual, the rest of this document is divided in sections
for the different targets that a command affects: instance, nodes, etc.

%prep
%setup -q

%build
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --libdir=%{_libdir} \
  --with-ssh-initscript=%{_initrddir}/sshd \
  --with-export-dir=%{_localstatedir}/lib/%{name}/export \
  --with-os-search-path=%{os_search_path} \
  --with-iallocator-search-path=%{iallocator_search_path} \
  --with-xen-bootloader=/usr/bin/pygrub \
  --with-file-storage-dir=%{_localstatedir}/lib/%{name}/file-storage \
  --with-shared-file-storage-dir=%{_localstatedir}/lib/%{name}/shared-file-storage \
  --with-kvm-path=/usr/libexec/qemu-kvm
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

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f /etc/rc3.d/S??ganeti ] || [ -f /etc/rc5.d/S??ganeti ]; then
    /sbin/chkconfig --del ganeti
fi
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
# %{_docdir}/%{name}
%{_sbindir}/*
%{_libdir}/%{name}
%{python_sitelib}/%{name}
%{_mandir}/man*/*
%dir /var/lib/%{name}
%dir /var/log/%{name}

%changelog
* Sun Dec 22 2012 Jun Futagawa <jfut@integ.jp>
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

* Wed Aug  5 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.4

* Fri Aug  5 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.3

* Fri May 13 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 2.4.2
- Added BuildRequires and Requires: python-inotify
- Change service startup order

* Tue Mar  9 2011 Jun Futagawa <jfut@integ.jp>
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

* Tue Oct 10 2010 Jun Futagawa <jfut@integ.jp>
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

* Tue Dec 18 2009 Jun Futagawa <jfut@integ.jp>
- Updated to 2.0.5

* Tue Nov  7 2009 Jun Futagawa <jfut@integ.jp>
- Backported the ``use_localtime`` option for the xen-hvm and kvm
  from the development branch

* Tue Nov  5 2009 Jun Futagawa <jfut@integ.jp>
- Changed export-dir to /var/lib/ganeti/export
- Changed file-storage-dir to /var/lib/ganeti/file-storage

* Sat Oct 24 2009 Jun Futagawa <jfut@integ.jp>
- Backported more options to xen-pvm hypervisor (``use_bootloader``,
  ``bootloader_path`` and ``bootloader_args``) from the development
  branch
- Updated to 2.0.4

* Tue Sep 29 2009 Jun Futagawa <jfut@integ.jp>
- First build 
