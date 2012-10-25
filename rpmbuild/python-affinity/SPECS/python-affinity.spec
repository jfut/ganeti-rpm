%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define srcname affinity

Name: python-affinity
Version: 0.1.0
Release: 1%{?dist}
Summary: affinity - control processor affinity on windows and linux
Group: System Environment/Libraries
License: Python Software Foundation License
URL: http://cheeseshop.python.org/pypi/affinity
Source: http://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
'affinity' provides a simple api for setting the processor affinity by
wrapping the specific underlying function calls of each
platform. works on windows (requires pywin32) and linux (kernel 2.6 or
patched 2.4).

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build
 
%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitearch}/%{srcname}/
%{python_sitearch}/%{srcname}-*.egg-info

%changelog
* Mon Oct 15 2012 Jun Futagawa <jfut@integ.jp> - 0.1.0-1
- Initial package
