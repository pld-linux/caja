#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x

Summary:	File manager for MATE
Summary(pl.UTF-8):	Zarządca plików dla środowiska MATE
Name:		mate-file-manager
Version:	1.6.3
Release:	3
License:	GPL v2+ and LGPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	3925e589ef3365a4d59ce8cca6db946e
URL:		http://wiki.mate-desktop.org/mate-file-manager
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.9
BuildRequires:	cairo-gobject-devel
BuildRequires:	desktop-file-utils
BuildRequires:	exempi-devel >= 1.99.5
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gobject-introspection-devel >= 0.6.4
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	intltool >= 0.40.1
BuildRequires:	libexif-devel >= 0.5.12
BuildRequires:	libselinux-devel
%{!?with_gtk3:BuildRequires:	libunique-devel >= 1.0}
%{?with_gtk3:BuildRequires:	libunique3-devel >= 3.0}
BuildRequires:	libxml2-devel >= 2.4.7
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.5.0
%{?with_apidocs:BuildRequires:	mate-doc-utils >= 1.1.0}
BuildRequires:	pango-devel >= 1:1.1.2
BuildRequires:	pangox-compat-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exempi >= 1.99.5
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	gvfs
Requires:	hicolor-icon-theme
Requires:	libexif >= 0.5.12
Requires:	libxml2 >= 2.4.7
Requires:	mate-desktop >= 1.5.0
Requires:	mate-icon-theme
Requires:	pango >= 1:1.1.2
Requires:	shared-mime-info
Suggests:	mate-backgrounds
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Caja (mate-file-manager) is the file manager and graphical shell for
the MATE desktop, that makes it easy to manage your files and the rest
of your system. It allows to browse directories on local and remote
file systems, preview files and launch applications associated with
them. It is also responsible for handling the icons on the MATE
desktop. Caja is a fork of Nautilus from GNOME.

%description -l pl.UTF-8
Caja (mate-file-manager) to zarządca plików i graficzna powłoka dla
środowiska graficznego MATE. Ułatwia zarządzanie plikami i resztą
systemu. Umożliwia przeglądanie katalogów na lokalnych i zdalnych
systemach plików, podgląd plików oraz uruchamianie aplikacji
powiązanych z nimi. Odpowiada także za obsługę ikon w środowisku MATE.
Caja to odgałęzienie Nautilusa z GNOME.

%package libs
Summary:	Library for mate-file-manager extensions
Summary(pl.UTF-8):	Biblioteka dla rozszerzeń mate-file-managera
License:	LGPL v2+
Group:		Development/Libraries
Requires:	glib2 >= 1:2.28.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Obsoletes:	mate-file-manager-extensions

%description libs
This package provides the library used by Caja view extensions.

%description libs -l pl.UTF-8
Ten pakiet dostarcza bibliotekę używaną przez rozszerzenia widoku
zarządcy plików Caja.

%package devel
Summary:	Support for developing mate-file-manager extensions
Summary(pl.UTF-8):	Pliki do tworzenia rozszerzeń mate-file-managera
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28.0
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0.0}

%description devel
This package provides the header files needed for developing Caja
extensions.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki nagłówkowe niezbędne do tworzenia
rozszerzeń zarządcy plików Caja.

%package apidocs
Summary:	libcaja-extension API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libcaja-extension
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libcaja-extension API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libcaja-extension.

%prep
%setup -q

%build
%{__intltoolize}
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-icon-update \
	--disable-schemas-compile \
	--disable-silent-rules \
	--enable-unique \
	--disable-update-mimedb \
	--with-gnu-ld \
	%{?with_gtk3:--with-gtk=3.0} \
	--with-html-dir=%{_gtkdocdir} \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# mate < 1.5 did not exist in PLD, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/caja.convert

# for external extensions
install -d $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

desktop-file-install \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/io
# update naming convention
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@ije,sr@ijekavian}

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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files  -f caja.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/caja
%attr(755,root,root) %{_bindir}/caja-autorun-software
%attr(755,root,root) %{_bindir}/caja-connect-server
%attr(755,root,root) %{_bindir}/caja-file-management-properties
%{_mandir}/man1/caja.1*
%{_mandir}/man1/caja-connect-server.1*
%{_mandir}/man1/caja-file-management-properties.1*
%attr(755,root,root) %{_libexecdir}/caja-convert-metadata
%dir %{_libdir}/caja
%dir %{_libdir}/caja/extensions-2.0
%{_datadir}/caja
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service
%{_datadir}/glib-2.0/schemas/org.mate.caja.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.media-handling.gschema.xml
%{_datadir}/mime/packages/caja.xml
%{_pixmapsdir}/caja
%{_desktopdir}/caja.desktop
%{_desktopdir}/caja-autorun-software.desktop
%{_desktopdir}/caja-browser.desktop
%{_desktopdir}/caja-computer.desktop
%{_desktopdir}/caja-file-management-properties.desktop
%{_desktopdir}/caja-folder-handler.desktop
%{_desktopdir}/caja-home.desktop
%{_desktopdir}/mate-network-scheme.desktop
%{_iconsdir}/hicolor/*x*/apps/caja.png
%{_iconsdir}/hicolor/*x*/emblems/emblem-note.png
%{_iconsdir}/hicolor/scalable/apps/caja.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaja-extension.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcaja-extension.so.1
%{_libdir}/girepository-1.0/Caja-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcaja-extension.so
%{_includedir}/caja
%{_datadir}/gir-1.0/Caja-2.0.gir
%{_pkgconfigdir}/libcaja-extension.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libcaja-extension
%endif
