Name:		crack-attack
Summary:	Tetris like game
Version:	1.1.14
Release:	%mkrel 16
Url:		http://www.nongnu.org/crack-attack/
Source0:	http://savannah.nongnu.org/download/crack-attack/%{name}-%{version}.tar.bz2
Source11:	%{name}-48.png
Source12:	%{name}-32.png
Source13:	%{name}-16.png
Source4:	crack-attack-scripts.tar.bz2
Source5:	crack-attack-1.1.10-man6-page.bz2
Patch3:		crack-attack-1.1.14-dont-segfault-i865g.patch
Patch4:     	crack-attack-1.1.14-ipv6-patch
Patch5:         crack-attack-1.1.14-gcc43.patch
Group:		Games/Arcade
License:	GPL
BuildRequires:	mesagl-devel 
BuildRequires:	SDL_mixer-devel 
BuildRequires:	SDL-devel
BuildRequires:	libmesaglut-devel
BuildRequires:	autoconf 
BuildRequires:	gtk+2-devel
Requires:	zenity
Suggests:	crack-attack-music
Suggests:	crack-attack-sounds
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
'Crack Attack!' is a free OpenGL game
based on the Super Nintendo classic Tetris Attack.

%prep
%setup -q -a 4
%patch3 -p0 -b .seg
# http://lists.gnu.org/archive/html/crack-attack-devel/2005-05/msg00002.html
%patch4 -p0
%patch5 -p1 -b .gcc43
bzcat %{SOURCE5} > doc/crack-attack.6

perl -pi -e "s|^CXXFLAGS.*|CXXFLAGS = $RPM_OPT_FLAGS -DNDEBUG|" src/Makefile*

%build
autoreconf -fi
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--enable-sound
%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -D -m 755 crack-attack-{solo,create-server,join-server} %{buildroot}%{_gamesbindir}/

install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

rm -rf %{buildroot}%{_mandir}/man1/crack-attack.1
install -m644 doc/crack-attack.6 -D %{buildroot}%{_mandir}/man6/crack-attack.6

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Crack Attack!
Exec=crack-attack
Icon=crack-attack
Terminal=false
Type=Application
Categories=ArcadeGame;Game;
StartupNotify=false
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

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
