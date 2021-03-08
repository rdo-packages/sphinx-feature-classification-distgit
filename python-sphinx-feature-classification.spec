%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library sphinx-feature-classification
%global module sphinx_feature_classification
%global with_doc 1

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack sphinx-feature-classification library
License:    ASL 2.0
URL:        https://docs.openstack.org/sphinx-feature-classification/latest/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{library}
Summary:    OpenStack sphinx-feature-classification library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-oslotest
BuildRequires:  python3-ddt
BuildRequires:  python3-testtools
BuildRequires:  python3-testrepository

Requires:  python3-pbr >= 2.0

Requires:  python3-docutils >= 0.11

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


%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    OpenStack sphinx-feature-classification library documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description -n python-%{library}-doc
OpenStack sphinx-feature-classification library.

This package contains the documentation.
%endif

%description
OpenStack sphinx-feature-classification library.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
export PYTHON=%{__python3}
%{__python3} setup.py test

%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
