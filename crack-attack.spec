Name:		crack-attack
Summary:	Tetris like game
Version:	1.1.14
Release:	%mkrel 11
Url:		http://www.nongnu.org/crack-attack/
Source0:	http://savannah.nongnu.org/download/crack-attack/%{name}-%{version}.tar.bz2
Source11:	%{name}-48.png
Source12:	%{name}-32.png
Source13:	%{name}-16.png
Source4:	crack-attack-scripts.tar.bz2
Source5:	crack-attack-1.1.10-man6-page.bz2
Patch3:		crack-attack-1.1.10-dont-segfault-i865g.patch
Patch4:     	crack-attack-1.1.14-ipv6-patch
Group:		Games/Arcade
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	mesagl-devel 
BuildRequires:	SDL_mixer-devel 
BuildRequires:	SDL-devel
BuildRequires:	libmesaglut-devel
BuildRequires:	autoconf 
BuildRequires:	gtk+2-devel
BuildRequires:	desktop-file-utils
Requires:	zenity
Requires:	crack-attack-music
Requires:	crack-attack-sounds

%description
'Crack Attack!' is a free OpenGL game
based on the Super Nintendo classic Tetris Attack.

%prep
%setup -q -a 4
%patch3 -p0
# http://lists.gnu.org/archive/html/crack-attack-devel/2005-05/msg00002.html
%patch4 -p0
bzcat %{SOURCE5} > doc/crack-attack.6

perl -pi -e "s|^CXXFLAGS.*|CXXFLAGS = $RPM_OPT_FLAGS -DNDEBUG|" src/Makefile*

%build
autoreconf
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--enable-sound
%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

install -D -m 755 crack-attack-{solo,create-server,join-server} $RPM_BUILD_ROOT%{_gamesbindir}/

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png

rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/crack-attack.1
install -m644 doc/crack-attack.6 -D $RPM_BUILD_ROOT%{_mandir}/man6/crack-attack.6

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Games" \
  --add-category="Game" \
  --add-category="ArcadeGame" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications data/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%files
%defattr(-,root,root)
%doc doc/*.html doc/*.jpg
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_mandir}/man6/*

