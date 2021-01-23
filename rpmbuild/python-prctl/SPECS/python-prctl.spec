%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define srcname prctl

Name: python-prctl
Version: 1.7
Release: 3%{?dist}
Summary: python-prctl -- Control process attributes through prctl
Group: System Environment/Libraries
License: GPL
URL: https://pythonhosted.org/python-prctl/
Source: https://github.com/seveas/python-prctl/archive/v%{version}.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libcap-devel
BuildRequires: python-devel
BuildRequires: python-setuptools
# doc
BuildRequires: python-sphinx

%description
The linux prctl function allows you to control specific characteristics of a
process' behaviour. Usage of the function is fairly messy though, due to
limitations in C and linux. This module provides a nice non-messy python(ic)
interface.

Besides prctl, this library also wraps libcap for complete capability handling
and allows you to set the process name as seen in ps and top.

See docs/index.rst for the documentation. An HTML version can be found on
http://packages.python.org/python-prctl/

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build
make -C docs html
 
%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/_build/html/*
%{python_sitearch}/%{srcname}*
%{python_sitearch}/_%{srcname}.so
%{python_sitearch}/python_%{srcname}-%{version}-*.egg-info

%changelog
* Sat Jan 23 2021 Jun Futagawa <jfut@integ.jp> - 1.7-3
- Add BuildRequires: python-sphinx

* Wed Apr 17 2019 Jun Futagawa <jfut@integ.jp> - 1.7-2
- Add BuildRequires: libcap-devel

* Mon Mar 18 2019 Jun Futagawa <jfut@integ.jp> - 1.7-1
- Initial package
