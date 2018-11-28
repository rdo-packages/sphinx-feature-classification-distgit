# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library sphinx-feature-classification
%global module sphinx_feature_classification

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack sphinx-feature-classification library
License:    ASL 2.0
URL:        https://docs.openstack.org/sphinx-feature-classification/latest/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python%{pyver}-%{library}
Summary:    OpenStack sphinx-feature-classification library
%{?python_provide:%python_provide python%{pyver}-%{library}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-ddt
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-testrepository

Requires:  python%{pyver}-pbr

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-docutils
%else
Requires:  python%{pyver}-docutils
%endif

%description -n python%{pyver}-%{library}
OpenStack sphinx-feature-classification library.

This is a Sphinx directive that allows creating matrices of drivers a project contains and which features they support.


%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack sphinx-feature-classification library tests
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-ddt
Requires:   python%{pyver}-testtools
Requires:   python%{pyver}-testrepository
Requires:   python%{pyver}-%{library} = %{version}-%{release}

%description -n python%{pyver}-%{library}-tests
OpenStack sphinx-feature-classification library.

This package contains the example library test files.


%package -n python-%{library}-doc
Summary:    OpenStack sphinx-feature-classification library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{library}-doc
OpenStack sphinx-feature-classification library.

This package contains the documentation.

%description
OpenStack sphinx-feature-classification library.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{pyver_install}

%check
export PYTHON=%{pyver_bin}
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%changelog
