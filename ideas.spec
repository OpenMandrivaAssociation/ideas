%define		name		ideas
%define		version		1.0.3.9
%define		sversion	1039
%define		debug_package %{nil}
Name:		%{name}
Version:	%{version}
Release:	3
Summary:	Nintendo DS and GBA Emulator
Group:		Emulators
License:	Freeware
URL:		http://ideasemu.biz/index.php
Source:		%{name}%{sversion}.tar.bz2
Source1:	%{name}.png
Source2:	acekardplugin.zip
Source3:	DsPad1.6.1.zip
Source4:	syncroaud.tar
Source5:	wifiplugin.zip
BuildRequires:	imagemagick
ExclusiveArch:	%{ix86}

%description
iDeaS is an emulator that runs a lot of commercial games on PC with OpenGL.

iDeaS has emulated the ARM7 GameBoy Advance processor at 100%, and the ARM9
dual screen processor at 99%; enabling it to run many commercial ROMs,
including Super Mario 64 DS and Pokémon Diamond & Pearl (with a few graphical
errors). The touch screen is fully emulated with a cursor instead of a hand,
and a keyboard can be used to emulate the Nintendo DS buttons.

iDeaS uses a plugin system that originally came from the UltraHLE Nintendo 64
emulator so that further support can achieved without looking at the source
code of the emulator.

%prep
%setup -q -c -n %{name}%{sversion}

%build
#unpack plugins
unzip %{SOURCE2}
unzip %{SOURCE3}
tar xf %{SOURCE4}
unzip %{SOURCE5}

%install
%__rm -rf %{buildroot}

# install section
%__mkdir_p %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
%{_libdir}/games/%{name}/%{name}
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

%__install -D -m 755 %{name} %{buildroot}%{_libdir}/games/%{name}/%{name}

%__install -D -m 755 Linux/acekard.so %{buildroot}%{_libdir}/games/%{name}/PlugIn/acekard.so
%__install -D -m 755 Linux/wifi.so %{buildroot}%{_libdir}/games/%{name}/PlugIn/wifi.so
%__install -D -m 755 syncro_aud_alsa.so %{buildroot}%{_libdir}/games/%{name}/PlugIn/syncro_aud_alsa.so
%__install -D -m 755 dspad1.6.1/libDsPad.so %{buildroot}%{_libdir}/games/%{name}/PlugIn/libDsPad.so

#Icons
%__mkdir_p %{buildroot}%{_datadir}/pixmaps/
%__install -c -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%__mkdir_p %{buildroot}/%{_miconsdir} \
	 %{buildroot}/%{_liconsdir} \
	 %{buildroot}/%{_iconsdir}

%__install -m 644 %{SOURCE1} %{buildroot}/%{_miconsdir}/%{name}.png
%__install -m 644 %{SOURCE1} %{buildroot}/%{_iconsdir}/%{name}.png
%__install -m 644 %{SOURCE1} %{buildroot}/%{_liconsdir}/%{name}.png
convert %{buildroot}%{_miconsdir}/%{name}.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{buildroot}%{_iconsdir}/%{name}.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png

# install menu entries
%__mkdir_p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=iDeaS
Comment=Nintendo DS and GBA Emulator
Exec=%{name}
Icon=%{name}
Type=Application
Terminal=false
Categories=X-MandrivaLinux-MoreApplications-Emulators;Emulator;
EOF

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr (644,root,root) %doc readme.txt
%{_bindir}/%{name}
%{_libdir}/games/%{name}/%{name}
%{_libdir}/games/%{name}/PlugIn/*.so
# desktop integration
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

