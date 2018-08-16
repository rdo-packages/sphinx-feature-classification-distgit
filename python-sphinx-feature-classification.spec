%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora}
%global with_python3 1
%endif


%global library sphinx-feature-classification
%global module sphinx_feature_classification

Name:       python-%{library}
Version:    0.3.0
Release:    1%{?dist}
Summary:    OpenStack sphinx-feature-classification library
License:    ASL 2.0
URL:        https://docs.openstack.org/sphinx-feature-classification/latest/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    OpenStack sphinx-feature-classification library
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python2-oslotest
BuildRequires:  python2-ddt
BuildRequires:  python2-testtools
BuildRequires:  python2-testrepository

Requires:  python-docutils
Requires:  python-pbr

%description -n python2-%{library}
OpenStack sphinx-feature-classification library.

This is a Sphinx directive that allows creating matrices of drivers a project contains and which features they support.


%package -n python2-%{library}-tests
Summary:    OpenStack sphinx-feature-classification library tests
Requires:   python2-oslotest
Requires:   python2-ddt
Requires:   python2-testtools
Requires:   python2-testrepository
Requires:   python2-%{library} = %{version}-%{release}

%description -n python2-%{library}-tests
OpenStack sphinx-feature-classification library.

This package contains the example library test files.


%package -n python-%{library}-doc
Summary:    OpenStack sphinx-feature-classification library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme

%description -n python-%{library}-doc
OpenStack sphinx-feature-classification library.

This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    OpenStack sphinx-feature-classification library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-oslotest
BuildRequires:  python3-ddt
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository

%description -n python3-%{library}
OpenStack sphinx-feature-classification library.

This is a Sphinx directive that allows creating matrices of drivers a project contains and which features they support.


%package -n python3-%{library}-tests
Summary:    OpenStack sphinx-feature-classification library tests

Requires:   python3-oslotest
Requires:   python3-ddt
Requires:   python3-testtools
Requires:   python3-testrepository
Requires:   python3-%{library} = %{version}-%{release}

%description -n python3-%{library}-tests
OpenStack sphinx-feature-classification library.

This package contains the example library test files.

%endif # with_python3


%description
OpenStack sphinx-feature-classification library.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 0.3.0-1
- Update to 0.3.0

