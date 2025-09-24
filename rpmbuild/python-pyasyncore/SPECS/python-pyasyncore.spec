%global srcname pyasyncore
%global modname asyncore

Name:           python-%{srcname}
Version:        1.0.4
Release:        %{autorelease}
Summary:        Make %{modname} available for Python 3.12 onwards

License:        Python-2.0.1
URL:            https://github.com/simonrob/%{srcname}
Source:         https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This package contains the asyncore module as found in Python versions
prior to 3.12. It is provided so that existing code relying on import
asyncore is able to continue being used without significant
refactoring.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version} -p1
# these should not be executable
chmod ugo-x README.md LICENSE


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{modname}


%check
# there are no tests upstream
%pyproject_check_import


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
