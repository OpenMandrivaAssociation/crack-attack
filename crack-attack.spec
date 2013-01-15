Name:		crack-attack
Summary:	Tetris like game
Version:	1.1.14
Release:	23
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
BuildRequires:	autoconf
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(xmu)
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
# This patch will be needed after we switch to freeglut:
#%patch6 -p1
bzcat %{SOURCE5} > doc/crack-attack.6

perl -pi -e "s|^CXXFLAGS.*|CXXFLAGS = $RPM_OPT_FLAGS -DNDEBUG|" src/Makefile*

%build
autoreconf -fi
%configure2_5x	--bindir=%{_gamesbindir} \
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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-21mdv2011.0
+ Revision: 663421
- mass rebuild

* Tue Feb 22 2011 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.1.14-20
+ Revision: 639312
- Add patch that will be needed when we change to freeglut
- Change gl BRs to generic versions
- Remove white spaces

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-19mdv2011.0
+ Revision: 603855
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-18mdv2010.1
+ Revision: 522404
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-17mdv2010.0
+ Revision: 413273
- rebuild

  + Christophe Fergeau <cfergeau@mandriva.com>
    - fix compilation with gcc 4.4

* Tue Apr 07 2009 Funda Wang <fwang@mandriva.org> 1.1.14-16mdv2009.1
+ Revision: 364777
- fix str fmt
- rediff segfault patch

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.1.14-15mdv2009.0
+ Revision: 264380
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-14mdv2009.0
+ Revision: 209709
- added a gcc43 patch from fedora

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.14-14mdv2008.1
+ Revision: 180074
- fix the desktop file
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix "error: (...)there should be no extension as described in the Icon Theme Specification if the value is not an absolute path"
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Jul 23 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.14-12mdv2008.0
+ Revision: 54853
- use suggests instead of requires for the music / sounds packages (thanks blino)

* Wed Jul 18 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.14-11mdv2008.0
+ Revision: 53308
- fix GTK+ buildrequires
- update icon cache in %%post
- drop old menu, X-Mandriva category, and old icons
- simply autotools usage to 'autoreconf'
- unversion autotools buildrequires
- requires -music and -sounds (fixes #20984)

* Wed Apr 25 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.14-10mdv2008.0
+ Revision: 18366
- sync files
- fd.o-compliant icons


* Mon Aug 14 2006 Götz Waschk <waschk@mandriva.org> 1.1.14-9mdv2007.0
- fix buildrequires

* Wed Jul 26 2006 Olivier Blin <blino@mandriva.com> 1.1.14-8mdv2007.0
- use zenity instead of crack-attack (from Cris Boylan, #23535)
- XDG menu
- for section in old menu
- fix BuildRequires

* Fri May 12 2006 Stefan van der Eijk <stefan@eijk.nu> 1.1.14-7mdk
- rebuild for sparc

* Wed Mar 29 2006 Guillaume Bedot <littletux@mandriva.org> 1.1.14-6mdk
- Updated URL and Source0

* Wed Mar 29 2006 Guillaume Bedot <littletux@mandriva.org> 1.1.14-5mdk
- Now use the GUI from the menus

* Fri Nov 25 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.1.14-4mdk
- enable sound (fix #17076)

* Thu Aug 04 2005 Michael Scherer <misc@mandriva.org> 1.1.14-3mdk
- ipv6 patch
- mkrel

* Sat May 21 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.1.14-2mdk
- fix automake usage and buildrequires

* Sun May 15 2005 Olivier Blin <oblin@mandriva.com> 1.1.14-1mdk
- 1.1.14 (needs some testing)
- remove Patches 0, 1, 2, 4, 5 and 6 (merged upstream)

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.10-11mdk
- fix version number in header files (P5 from debian)
- set the SO_REUSEADDR flag on server sockets (P6 from debian)
- get rid of invalid man page and replace it with a valid one from debian (S5)

* Fri Aug 20 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.10-10mdk
- fix typo in menu entry

* Mon Aug 16 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.10-9mdk
- Rebuild with new menu

* Fri Jul 02 2004 Michael Scherer <misc@mandrake.org> 1.1.10-8mdk 
- fix compilation on gcc3.4

* Sun May 23 2004 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.10-7mdk
- add patch similar to old voodoo3 one to not segfault on i865g

* Sun Dec 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.10-6mdk
- use %%{_gamesbindir} and %%{_gamesdatadir}
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install

* Wed Dec 10 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.10-5mdk
- sounds+music support based on crack-attack-miguev-v05.diff and Pascal
  Terjan's work

* Mon Nov 17 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.10-4mdk
- don't "fix bad version" or else we're not compatible with other
  distros

* Fri Nov 14 2003 Olivier Blin <oliv.blin@laposte.net> 1.1.10-3mdk
- fix bad version (it is really 1.1.10) (patch2)

* Tue Oct 21 2003 Olivier Blin <oliv.blin@laposte.net> 1.1.10-2mdk
- patch0: warn server if client version mismatch

* Sat Oct 18 2003 Olivier Blin <oliv.blin@laposte.net> 1.1.10-1mdk
- new version
- drop patch2 and patch3 (merged upstream)

* Mon Sep 22 2003 Götz Waschk <waschk@linux-mandrake.com> 1.1.9-5mdk
- update scripts to support X-treme mode

* Sun Sep 21 2003 Götz Waschk <waschk@linux-mandrake.com> 1.1.9-4mdk
- requires Xdialog for crack-attack-join-server
- fix buildrequires

* Fri Sep 19 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.9-3mdk
- only sleep for 1 second in Patch3, should be enough

* Wed Sep 17 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.9-2mdk
- Patch3: avoid "port is busy" when playing two times in a row the server

* Tue Sep 16 2003 Götz Waschk <waschk@linux-mandrake.com> 1.1.9-1mdk
- drop obsolete patch 0  
- new version

* Mon Sep 15 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.8-4mdk
- workaround Voodoo3 segfault (patch 2, disable 1d texturing for
  voodoo3 renderer)

* Fri Sep 12 2003 Olivier Blin <oliv.blin@laposte.net> 1.1.8-3mdk
- improve g++ 3.3 fixes (thanks to gc)
- use OpenGL 1.3 functions for multi-texturing

* Thu Sep 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.8-2mdk
- use our compile flags

* Fri Aug 22 2003 Olivier Blin <oliv.blin@laposte.net> 1.1.8-1mdk
- Initial release for Mandrake
- g++ 3.3 fixes
- Converted xpm icons to png
- Added scripts to launch crack-attack from menus (prompt for server name)

