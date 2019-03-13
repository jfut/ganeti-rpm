%{!?os_ver: %define os_ver %(Z=`rpm -q --whatprovides /etc/redhat-release`;rpm -q --qf '%{V}' $Z | sed 's/\\.[0-9]*//')}

Name:		snf-image
Version:	0.15.1
Release:	1%{?dist}
Summary:	snf-image is a Ganeti OS definition
Vendor:         Synnefo development team

License:	GPLv2
URL:		https://github.com/grnet/snf-image
Source0:	%{name}-%{version}.tar.gz
Source1:        %{name}.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	make

Requires:       kpartx
Requires:       mbr
Requires:       python >= 2.6
Requires:       curl
Requires:       scapy
Requires:       python-prctl
Requires:       xz

%description
snf-image is a Ganeti OS definition. It allows Ganeti to launch instances from 
predefined or untrusted custom Images. The whole process of deploying an Image
 onto the block device, as provided by Ganeti, is done in complete isolation 
from the physical host, enhancing robustness and security.

snf-image supports KVM and Xen based Ganeti clusters.

snf-image also supports Image customization via hooks. Hooks allow for:

* Changing the password of root or arbitrary users
* Injecting files into the file system, e.g., SSH keys
* Setting a custom hostname
* Re-creating SSH host keys to ensure the image uses unique keys

%prep
%setup -q

%build
patch -p1 < %{SOURCE1}
cd snf-image-host
./autogen.sh
%configure \
make

%install
cd snf-image-host
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p %{buildroot}/etc/ganeti/snf-image/
mkdir -p %{buildroot}/var/lib/snf-image/helper
mkdir -p %{buildroot}/etc/default
mkdir -p %{buildroot}/usr/share/doc/snf-image/
cp AUTHORS %{buildroot}/usr/share/doc/snf-image
cp COPYING %{buildroot}/usr/share/doc/snf-image
cp defaults.in %{buildroot}/etc/default/snf-image
cp variants.list %{buildroot}/etc/ganeti/snf-image

%post
snf-image-update-helper -y
ln -s /etc/ganeti/snf-image/variants.list /usr/share/ganeti/os/snf-image/variants.list

%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/ganeti/os/snf-image/*
/usr/share/doc/snf-image/*
/etc/ganeti/snf-image/*
/etc/xen/scripts/vif-snf-image
/var/lib/snf-image/helper/
%config /etc/default/snf-image
