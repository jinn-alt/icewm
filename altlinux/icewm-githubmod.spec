# -*- mode: rpm-spec; coding: utf-8 -*-
%define realname icewm
%def_with menu
%define gitrev .git956b8d7

Name: %realname-githubmod
Version: 1.3.10
Release: alt1

Summary: X11 Window Manager
Group: Graphical desktop/Icewm
License: LGPLv2
Url: https://github.com/bbidulock/icewm
Packager: Dmitriy Khanzhin <jinn@altlinux.ru>

Provides: icewm = %version-%release
Provides: icewm-light = %version-%release
Requires: design-%realname >= 1.0-alt6
Conflicts: icewm-light

Source0: %name.tar
Source1: %realname.menu
Source2: %realname.menu-method
Source3: %realname-16.png
Source4: %realname-32.png
Source5: %realname-48.png
Source6: start%realname
Source7: IceWM.xpm
Source8: %realname.wmsession
#Source9: README.ALT
Source10: %realname.desktop
Source11: restart
Source12: icewm-old-changelog.bz2

Patch0: %name-%version-%release.patch

BuildRequires(pre): rpm-macros-cmake
# Automatically added by buildreq on Sat Apr 11 2015
BuildRequires: OpenSP cmake gcc-c++ libSM-devel libXext-devel libXft-devel
BuildRequires: libXinerama-devel libXrandr-devel libalsa-devel libesd-devel
BuildRequires: libgdk-pixbuf-devel libsndfile-devel linuxdoc-tools perl-parent

%if_without menu
BuildPreReq: desktop-file-utils
%endif

%description
 Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.
 This release is based on alternative source, based on a community fork
maintained on Github.

Recommends: iftop, mutt

%prep
%setup -n %name
%patch0 -p1

%build
%cmake	-DCFGDIR=%_sysconfdir/X11/%realname -DPREFIX=%_prefix \
	-DLIBDIR=%_x11x11dir/%realname -DCONFIG_GUIEVENTS=on  \
	-DICESOUND="ALSA,OSS,ESound"
pushd BUILD
%make_build
popd

%install
pushd BUILD
%makeinstall_std
popd
BUILD/genpref > %buildroot/%_x11x11dir/%realname/preferences

%if_with menu
mkdir -p %buildroot%_menudir
install -m 644 %SOURCE1 %buildroot%_menudir/%realname
%endif
mkdir -p %buildroot%_sysconfdir/menu-methods
install -m 755 %SOURCE2 %buildroot%_sysconfdir/menu-methods/%realname

install -pD -m644 %SOURCE3 %buildroot%_miconsdir/%realname.png
install -pD -m644 %SOURCE4 %buildroot%_niconsdir/%realname.png
install -pD -m644 %SOURCE5 %buildroot%_liconsdir/%realname.png
install -pD -m644 %SOURCE7 %buildroot%_pixmapsdir/IceWM.xpm
install -pD -m644 %SOURCE8 %buildroot%_sysconfdir/X11/wmsession.d/04IceWM
#install -m 644 #SOURCE9 doc/README.ALT
install -m644 %SOURCE12 icewm-old-changelog.bz2

mkdir -p %buildroot%_sysconfdir/X11/%realname

install -m 755 %SOURCE6 %buildroot%_bindir/start%realname
install -m 755 %SOURCE11 %buildroot%_sysconfdir/X11/%realname/restart

%if_without menu
desktop-file-install --vendor alt --dir %buildroot%_desktopdir %SOURCE10
%endif

%find_lang  %realname

# remove unpackaged files
rm -f %buildroot/%_bindir/%realname-set-gnomewm
rm -rf %buildroot/%_x11x11dir/%realname/themes/*

%files -f %realname.lang
%dir %_sysconfdir/X11/%realname
%config(noreplace) %_sysconfdir/X11/%realname/restart
%config(noreplace) %_sysconfdir/menu-methods/*
%_sysconfdir/X11/wmsession.d/*
%_bindir/*
%dir %_x11x11dir/%realname
%_x11x11dir/%realname/icons
%_x11x11dir/%realname/ledclock
%_x11x11dir/%realname/mailbox
%_x11x11dir/%realname/taskbar
%_x11x11dir/%realname/themes
%config(noreplace) %_x11x11dir/%realname/keys
%config(noreplace) %_x11x11dir/%realname/menu
%config(noreplace) %_x11x11dir/%realname/preferences
%config(noreplace) %_x11x11dir/%realname/programs
%config(noreplace) %_x11x11dir/%realname/toolbar
%config(noreplace) %_x11x11dir/%realname/winoptions
%if_with menu
%_menudir/*
%else
%_desktopdir/*
%endif
%_niconsdir/*
%_miconsdir/*
%_liconsdir/*
%_pixmapsdir/*
%_man1dir/*

%doc AUTHORS NEWS README.md BUILD/doc/*.html icewm-old-changelog.bz2

%changelog
* Sun Jul 05 2015 Dmitriy Khanzhin <jinn@altlinux.org> 1.3.10-alt1
- 1.3.10 release
- updated reboot/shutdown commands for use with systemd and sysvinit

* Mon May 04 2015 Dmitriy Khanzhin <jinn@altlinux.org> 1.3.9-alt4.git960629d
- added forgotten requires to design-icewm

* Thu Apr 30 2015 Dmitriy Khanzhin <jinn@altlinux.org> 1.3.9-alt3.git960629d
- git snapshot 960629d
- old changelog cut off to separate file
- added conflict to icewm-light

* Tue Apr 14 2015 Dmitriy Khanzhin <jinn@altlinux.org> 1.3.9-alt2.gite97394f
- added support fd.o-style icons

* Tue Apr 14 2015 Dmitriy Khanzhin <jinn@altlinux.org> 1.3.9-alt1.gite97394f
- initial build for altlinux
