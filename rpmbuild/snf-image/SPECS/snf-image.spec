%{!?os_ver: %define os_ver %(Z=`rpm -q --whatprovides /etc/redhat-release`;rpm -q --qf '%{V}' $Z | sed 's/\\.[0-9]*//')}

Name:           snf-image
Version:        0.23.1
Release:        2%{?dist}
Summary:        snf-image is a Ganeti OS definition
Vendor:         Synnefo development team

License:        GPLv2
URL:            https://github.com/grnet/snf-image
Source0:        https://github.com/grnet/snf-image/archive/%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch1:         snf-image-0.23.1-kvm.patch

BuildRequires:  parted
BuildRequires:  make
BuildRequires:  python-prctl
BuildRequires:  python2-scapy

Requires:       curl
Requires:       kpartx
#Requires:       mbr
Requires:       parted
Requires:       python >= 2.6
Requires:       python-prctl
Requires:       python2-scapy
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

%patch1 -p1

%build
cd snf-image-host
./autogen.sh
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir}
    $@
make

%install
cd snf-image-host
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/default/%{name}
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sysconfdir}/ganeti/%{name}
install -d -m 755 ${RPM_BUILD_ROOT}/%{_datadir}/doc/%{name}
install -d -m 755 ${RPM_BUILD_ROOT}/%{_sharedstatedir}/%{name}/helper

pushd ${RPM_BUILD_ROOT}/%{_datadir}/ganeti/os/%{name}
mv variants.list ../../../../..%{_sysconfdir}/ganeti/%{name}/
ln -s ../../../../..%{_sysconfdir}/ganeti/%{name}/variants.list variants.list
popd

%post
#snf-image-update-helper -y

%files
%defattr(-,root,root)
%doc snf-image-host/AUTHORS snf-image-host/COPYING
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/ganeti/%{name}/variants/
%config(noreplace) %{_sysconfdir}/ganeti/%{name}/variants/default.conf
%config(noreplace) %{_sysconfdir}/ganeti/%{name}/variants.list
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/xen/scripts/vif-snf-image
%{_bindir}/*
%{_datadir}/doc/%{name}/*
%{_datadir}/ganeti/os/%{name}/*
%{_sharedstatedir}/%{name}/helper

%changelog
* Wed Apr 17 2019 Jun Futagawa <jfut@integ.jp> - 0.23.1-2
- Added BuildRequires: parted
- Added Requires: parted

* Mon Mar 18 2019 Jun Futagawa <jfut@integ.jp> - 0.23.1-1
- Initial package
