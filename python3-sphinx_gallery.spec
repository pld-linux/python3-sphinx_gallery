#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Sphinx extension to automatically generate an examples gallery
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do automatycznego generowania galerii przykładów
Name:		python3-sphinx_gallery
Version:	0.19.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-gallery/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx-gallery/sphinx_gallery-%{version}.tar.gz
# Source0-md5:	bef91dd3e20de28ab4358220d449ca1b
URL:		https://github.com/sphinx-gallery/sphinx-gallery
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
BuildRequires:	ffmpeg
BuildRequires:	python3-Sphinx >= 1.8.3
BuildRequires:	python3-joblib
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.7
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
%setup -q -n sphinx_gallery-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# test_embed_code_links_get_data, test_run_sphinx use network
# test_embed_links_and_styles is too dependent on sphinx version?
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest sphinx_gallery/tests -k 'not test_embed_code_links_get_data and not test_embed_links_and_styles and not test_run_sphinx'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_gallery/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/sphinx_gallery_py2jupyter
%{py3_sitescriptdir}/sphinx_gallery
%{py3_sitescriptdir}/sphinx_gallery-%{version}.dist-info
