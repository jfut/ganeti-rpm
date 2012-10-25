%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define instance_debootstrap_dir /etc/ganeti/instance-debootstrap
%define variants_dir %{instance_debootstrap_dir}/variants
%define hooks_dir %{instance_debootstrap_dir}/hooks
%define with_os_dir /usr/share/ganeti/os

Summary: debootstrap-based instance OS definition for ganeti
Name: ganeti-instance-debootstrap
Version: 0.9
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://code.google.com/p/ganeti/
Source0: http://ganeti.googlecode.com/files/ganeti-instance-debootstrap-%{version}.tar.gz
Patch1: ganeti-instance-debootstrap-0.7-grub.patch
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-root
Requires: ganeti
Requires: debootstrap
Requires: kpartx

%description
Ganeti is a virtual server cluster management software tool built on
top of the Xen virtual machine monitor and other Open Source software.
After setting it up it will provide you with an automated environment
to manage highly available virtual machine instances.

This package provides an OS definition for ganeti that will allow
installation of Debian (and possibly Unbuntu) instances via
debootstrap.

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
* Sat Oct 24 2009 Jun Futagawa <jfut@integ.jp>
- Update grub script

* Tue Sep 29 2009 Jun Futagawa <jfut@integ.jp>
- first build 
