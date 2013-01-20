%define instance_debootstrap_dir /etc/ganeti/instance-debootstrap
%define variants_dir %{instance_debootstrap_dir}/variants
%define hooks_dir %{instance_debootstrap_dir}/hooks
%define with_os_dir /usr/share/ganeti/os

Name: ganeti-instance-debootstrap
Version: 0.12
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: debootstrap-based instance OS definition for ganeti
License: GPLv2
URL: http://code.google.com/p/ganeti/

Source0: http://ganeti.googlecode.com/files/ganeti-instance-debootstrap-%{version}.tar.gz

Patch1: ganeti-instance-debootstrap-0.12-add_support_for_rhel.patch

BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-root

Requires: ganeti
Requires: debootstrap
Requires: kpartx

%description
This package provides an guest OS definition for Ganeti.
It will install a minimal version of Debian or Ubuntu via debootstrap
(thus it requires network access).

%prep
%setup -q

%patch1 -p1

%build
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --localstatedir=/var \
  --with-os-dir=%{with_os_dir}

make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/default
install -m 644 defaults ${RPM_BUILD_ROOT}/%{_sysconfdir}/default/%{name}

install -m 644 variants.list ${RPM_BUILD_ROOT}/%{instance_debootstrap_dir}/variants.list

touch ${RPM_BUILD_ROOT}/%{variants_dir}/default.conf

install -m 755 -d ${RPM_BUILD_ROOT}%{hooks_dir}
install -m 755 examples/hooks/grub ${RPM_BUILD_ROOT}%{hooks_dir}/grub

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
exit 0

%preun
exit 0

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{instance_debootstrap_dir}/variants.list
%config(noreplace) %{variants_dir}/default.conf
%attr(755,root,root) %config %{hooks_dir}/grub
%{_docdir}/%{name}/*
%{with_os_dir}/debootstrap/*

%changelog
* Sun Jan 20 2013 Jun Futagawa <jfut@integ.jp> - 0.12-1
- Updated to 0.12

* Sat Aug 06 2011 Jun Futagawa <jfut@integ.jp>
- Updated to 0.9

* Sat Oct 24 2009 Jun Futagawa <jfut@integ.jp>
- Updated grub script

* Tue Sep 29 2009 Jun Futagawa <jfut@integ.jp>
- first build 
