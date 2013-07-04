%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define srcname bitarray

Name: python-bitarray
Version: 0.8.0
Release: 1%{?dist}
Summary: efficient arrays of booleans -- C extension
Group: System Environment/Libraries
License: Python Software Foundation License
URL: http://cheeseshop.python.org/pypi/bitarray
Source: http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
This module provides an object type which efficiently represents an array of
booleans. Bitarrays are sequence types and behave very much like usual lists.
Eight bits are represented by one byte in a contiguous block of memory. The
user can select between two representations; little-endian and big-endian. Most
of the functionality is implemented in C. Methods for accessing the machine
representation are provided. This can be useful when bit level access to binary
files is required, such as portable bitmap image files (.pbm). Also, when
dealing with compressed data which uses variable bit length encoding, you may
find this module useful.

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
* Thu Feb  8 2013 Jun Futagawa <jfut@integ.jp> - 0.8.0-1
- Initial package
