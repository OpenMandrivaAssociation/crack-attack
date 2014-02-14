Summary:	Tetris like game
Name:		crack-attack
Version:	1.1.14
Release:	27
Group:		Games/Arcade
License:	GPL
Url:		http://www.nongnu.org/crack-attack/
Source0:	http://savannah.nongnu.org/download/crack-attack/%{name}-%{version}.tar.bz2
Source11:	%{name}-48.png
Source12:	%{name}-32.png
Source13:	%{name}-16.png
Source4:	crack-attack-scripts.tar.bz2
Source5:	crack-attack-1.1.10-man6-page.bz2
Patch0:		crack-attack-1.1.14-fix-str-fmt.patch
Patch1:		crack-attack-1.1.14-automake-1.13.patch
Patch3:		crack-attack-1.1.14-dont-segfault-i865g.patch
Patch4:		crack-attack-1.1.14-ipv6-patch
Patch5:		crack-attack-1.1.14-gcc43.patch
Patch6:		crack-attack-1.1.14-freeglut-init.patch

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(glu)

Requires:	zenity
Suggests:	crack-attack-music
Suggests:	crack-attack-sounds

%description
'Crack Attack!' is a free OpenGL game
based on the Super Nintendo classic Tetris Attack.

%prep
%setup -q -a 4
%patch0 -p0 -b .str
%patch1 -p1 -b .am113~
%patch3 -p0 -b .seg
# http://lists.gnu.org/archive/html/crack-attack-devel/2005-05/msg00002.html
%patch4 -p0
%patch5 -p1 -b .gcc43
%patch6 -p1 -b .glutinit
bzcat %{SOURCE5} > doc/crack-attack.6

sed -i -e "s|^CXXFLAGS.*|CXXFLAGS = $RPM_OPT_FLAGS -DNDEBUG|" src/Makefile*
autoreconf -fi

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--enable-sound
%make

%install
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

%files
%doc doc/*.html doc/*.jpg
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-*
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_mandir}/man6/*

