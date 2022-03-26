#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Sphinx extension to automatically generate an examples gallery
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do automatycznego generowania galerii przykładów
Name:		python3-sphinx_gallery
Version:	0.7.0
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-gallery/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx-gallery/sphinx-gallery-%{version}.tar.gz
# Source0-md5:	bb9944c614810551c424798556ba8230
URL:		https://github.com/sphinx-gallery/sphinx-gallery
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.8.3
BuildRequires:	python3-joblib
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.5
Provides:	python3-sphinx-gallery = %{version}-%{release}
Obsoletes:	python3-sphinx-gallery < 0.4.0-5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Sphinx extension that builds an HTML version of any Python script
and puts it into an examples gallery.
  
It is extracted from the scikit-learn project and aims to be an
independent general purpose extension.

%description -l pl.UTF-8
Rozszerzenie Sphinksa tworzące wersję HTML dowolnego skryptu Pythona i
umieszczające go w galerii przykładów.

Zostało wyciągnięte z projektu scikit-learn z myślą o używaniu jako
niezależne rozszerzenie ogólnego przeznaczenia.

%prep
%setup -q -n sphinx-gallery-%{version}

%build
%py3_build

%if %{with tests}
# test_embed_code_links_get_data uses network
PYTHONPATH=$(pwd)/build-3/lib \
pytest-3 sphinx_gallery/tests -k 'not test_embed_code_links_get_data'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_gallery/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/copy_sphinxgallery.sh
%attr(755,root,root) %{_bindir}/sphx_glr_python_to_jupyter.py
%{py3_sitescriptdir}/sphinx_gallery
%{py3_sitescriptdir}/sphinx_gallery-%{version}-py*.egg-info
