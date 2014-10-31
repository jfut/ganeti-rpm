Summary: Ganeti RPM Package Repository release file
Name: integ-ganeti-release
Version: 6
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://jfut.integ.jp/linux/ganeti/

Source0: integ-ganeti.repo
Source1: RPM-GPG-KEY-integ-ganeti

BuildArch: noarch

%description
This package contains yum configuration for the Ganeti RPM Package
Repository, as well as the public GPG keys used to sign packages.

%prep
%setup -c -T
%{__cp} -a %{SOURCE1} .

# %build

%install
%{__rm} -rf %{buildroot}
%{__install} -Dpm 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/integ-ganeti.repo
%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-integ-ganeti

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%pubkey RPM-GPG-KEY-integ-ganeti
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/integ-ganeti.repo
%dir %{_sysconfdir}/pki/rpm-gpg/
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-integ-ganeti

%changelog
* Fri Oct 31 2014 Jun Futagawa <jfut@integ.jp> - 6-1
- Initial integ-ganeti-release package for el6.
