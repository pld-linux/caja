# TODO
# -extensions not optional:
# mate-file-manager-1.5.2-0.2.i686: required "libcaja-extension.so.1" is provided by the following packages:
#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	File manager for MATE
Name:		mate-file-manager
Version:	1.5.2
Release:	1
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
Source0:	http://pub.caja.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	99ad04fe0460c7267803e88f22966e67
URL:		http://caja.org/
BuildRequires:	cairo-gobject-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	exempi-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	libexif-devel
BuildRequires:	libselinux-devel
BuildRequires:	libunique-devel
BuildRequires:	libxml2-devel
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel
%{?with_apidocs:BuildRequires:	mate-doc-utils >= 1.1.0}
BuildRequires:	pangox-compat-devel
BuildRequires:	startup-notification-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
Requires:	%{name}-extensions = %{version}-%{release}
Requires:	filesystem
Requires:	gamin
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	gvfs
Requires:	hicolor-icon-theme
Requires:	mate-icon-theme
#Requires:	redhat-menus
Requires:	shared-mime-info
Suggests:	mate-backgrounds
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Caja (mate-file-manager) is the file manager and graphical shell for
the MATE desktop, that makes it easy to manage your files and the rest
of your system. It allows to browse directories on local and remote
file systems, preview files and launch applications associated with
them. It is also responsible for handling the icons on the MATE
desktop.

%package extensions
Summary:	Mate-file-manager extensions library
License:	LGPL v2+
Group:		Development/Libraries

%description extensions
This package provides the libraries used by caja extensions.

%package devel
Summary:	Support for developing mate-file-manager extensions
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-extensions = %{version}-%{release}

%description devel
This package provides libraries and header files needed for developing
caja extensions.

%package apidocs
Summary:	libcaja API documentation
Summary(pl.UTF-8):	Dokumentacja API libcaja
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libcaja API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libcaja.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--disable-static \
	--enable-unique \
	--disable-update-mimedb \
	--disable-schemas-compile \
	--with-gnu-ld \
	--with-x \
	--with-gtk=2.0

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' |xargs rm

#%{__rm} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
#%{__rm} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

install -d $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

desktop-file-install \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/io
%find_lang caja

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_mime_database
%update_icon_cache hicolor
%glib_compile_schemas

%post	extensions -p /sbin/ldconfig
%postun	extensions -p /sbin/ldconfig

%files  -f caja.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB NEWS README
%attr(755,root,root) %{_bindir}/caja
%attr(755,root,root) %{_bindir}/caja-autorun-software
%attr(755,root,root) %{_bindir}/caja-connect-server
%attr(755,root,root) %{_bindir}/caja-file-management-properties
%{_datadir}/caja
%dir %{_libdir}/caja
%dir %{_libdir}/caja/extensions-2.0
%{_pixmapsdir}/caja/
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/caja.png
%{_iconsdir}/hicolor/scalable/apps/caja.svg
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_mandir}/man1/caja*.1.*
%{_libexecdir}/caja-convert-metadata
%{_datadir}/mime/packages/caja.xml

%files extensions
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaja-extension.so.*.*.*
%ghost %{_libdir}/libcaja-extension.so.1
%{_libdir}/girepository-1.0/Caja-2.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcaja-extension.so
%{_includedir}/caja
%{_pkgconfigdir}/libcaja-extension.pc
%{_datadir}/gir-1.0/Caja-2.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libcaja-extension
%endif
