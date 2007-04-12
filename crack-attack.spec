Name:		crack-attack
Summary:	Tetris like game
Version:	1.1.14
Release:	%mkrel 9
Url:		http://www.nongnu.org/crack-attack/
Source0:	http://savannah.nongnu.org/download/crack-attack/%{name}-%{version}.tar.bz2
Source11:	%{name}-48.png
Source12:	%{name}-32.png
Source13:	%{name}-16.png
Source4:	crack-attack-scripts.tar.bz2
Source5:	crack-attack-1.1.10-man6-page.bz2
Patch3:		crack-attack-1.1.10-dont-segfault-i865g.patch
Patch4:     crack-attack-1.1.14-ipv6-patch
Group:		Games/Arcade
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	mesagl-devel SDL_mixer-devel SDL-devel autoconf2.5
BuildRequires:	libmesaglut-devel
BuildRequires:	automake1.8 libgtk+2.0-devel
BuildRequires:	desktop-file-utils
Requires:	zenity

%description
'Crack Attack!' is a free OpenGL game
based on the Super Nintendo classic Tetris Attack.

%prep
%setup -q -a 4
%patch3 -p0
# http://lists.gnu.org/archive/html/crack-attack-devel/2005-05/msg00002.html
%patch4 -p0

perl -pi -e "s|^CXXFLAGS.*|CXXFLAGS = $RPM_OPT_FLAGS -DNDEBUG|" src/Makefile*

export FORCE_AUTOCONF_2_5=1
aclocal-1.8
automake-1.8 -a -c --gnu
WANT_AUTOCONF_2_5=1 autoconf
autoheader
bzcat %{SOURCE5} > doc/crack-attack.6

%build
%configure	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--enable-sound
%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

install -D -m 755 crack-attack-{solo,create-server,join-server} $RPM_BUILD_ROOT%{_gamesbindir}/

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%{name}): command="%{_gamesbindir}/%{name}" icon="%{name}.png" \
section="More Applications/Games/Arcade" title="Crack Attack!" \
longtitle="Tetris like game based on Tetris Attack" needs="x11" xdg="true"
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/crack-attack.1
install -m644 doc/crack-attack.6 -D $RPM_BUILD_ROOT%{_mandir}/man6/crack-attack.6

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Games" \
  --add-category="Game" \
  --add-category="ArcadeGame" \
  --add-category="X-MandrivaLinux-MoreApplications-Games-Arcade" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications data/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%doc doc/*.html doc/*.jpg
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-*
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_menudir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/man6/*

