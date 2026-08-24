%define free %{?_non_free:0} %{?!_non_free:1}

%global tarball_version %%( echo %{version} | sed -E "s,^([0-9]+)\\.([0-9]+)\\.([0-9]+)$,\\1.\\2-\\3," )

# These libraries and their dependants are in the same package - indigo-drivers-nonfree
%global __requires_exclude ^lib(PlayerOneCamera|PlayerOnePW|qhyccd|)\\.so.*$

Name:       indigo
Version:    3.0.4
Release:    1%{?dist}
Summary:    INDIGO astronomy software platform

License:    LicenseRef-INDIGO-Astronomy-open-source-license
URL:        https://www.indigo-astronomy.org/
Source0:    deblob.sh
%if %{free}
Source1:    %{name}-free-%{tarball_version}.tar.xz
%else
Source1:    https://github.com/indigo-astronomy/indigo/archive/refs/tags/%{tarball_version}/%{name}-%{tarball_version}.tar.gz
%endif
Source2:    indigo-server.service
Source3:    indigo-server.env

Patch1001:     0001-Do-not-call-udevadm-on-make-install.patch
Patch1002:     0002-Do-not-call-sudo-on-make-install.patch
Patch1003:     0003-Install-fxload-into-INSTALL_ROOT.patch
Patch1004:     0004-Fix-runpath.patch
Patch1005:     0005-Use-system-dc1394.patch
Patch1006:     0006-Use-system-libusb-libhidapi-libjpeg-libtiff-and-libr.patch

Patch2001:     0001-Remove-proprietary-libftd2xx.patch

BuildRequires:  systemd-rpm-macros
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  avahi-compat-libdns_sd-devel
BuildRequires:  libudev-devel
BuildRequires:  git
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  zlib-devel
BuildRequires:  libusb-compat-0.1-devel
BuildRequires:  libusb1-devel
BuildRequires:  systemd-devel
BuildRequires:  avahi-compat-libdns_sd-devel
BuildRequires:  libcurl-devel patchelf
BuildRequires:  libdc1394-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtiff-devel
BuildRequires:  LibRaw-devel
BuildRequires:  hidapi-devel


%description
INDIGO is a system of standards and frameworks for multiplatform and
distributed astronomy software development designed to scale with your
needs.


%package server-free
Summary: INDIGO astronomy server without proprietary drivers

Requires: (%{name}-server-drivers-list-free = %{version}-%{release} or %{name}-server-drivers-list-nonfree = %{version}-%{release})
Requires: perl-interpreter
Requires: perl-Getopt-Std
%ifarch aarch64
Requires: perl-Getopt-Long
%endif

%description server-free
INDIGO is a system of standards and frameworks for multiplatform and
distributed astronomy software development designed to scale with your
needs. "Free" version without proprietary drivers.


%if %{free}
%package server-drivers-list-free
Summary: List of supported drivers for INDIGO astronomy software platform

Conflicts: %{name}-server-drivers-list-nonfree


%description server-drivers-list-free
List of supported drivers for INDIGO astronomy software platform.
%else
%package server-drivers-nonfree
Summary: Non-free drivers for INDIGO astronomy software platform

Requires: %{name}-server-free = %{version}-%{release}
Requires: %{name}-server-drivers-list-nonfree = %{version}-%{release}


%description server-drivers-nonfree
Non-free drivers for INDIGO astronomy software platform.


%package server-drivers-list-nonfree
Summary: List of supported drivers for INDIGO astronomy software platform

Conflicts: %{name}-server-drivers-list-free


%description server-drivers-list-nonfree
List of supported drivers for INDIGO astronomy software platform.
%endif


%package client-libs-free
Summary: Client libraries for INDIGO astronomy software platform


%description client-libs-free
Client libraries for INDIGO astronomy software platform.


%package free-devel
Summary: Headers for INDIGO astronomy software platform

Requires: %{name}-free = %{version}-%{release}
Requires: %{name}-client-libs-free = %{version}-%{release}


%description free-devel
Headers for INDIGO astronomy software platform.


%prep
%setup -q -D -T -b1 -n %{name}-%{tarball_version}

%patch -P 1001 -p 1
%patch -P 1002 -p 1
%patch -P 1003 -p 1
%patch -P 1004 -p 1
%patch -P 1005 -p 1
%patch -P 1006 -p 1

%if %{free}
%patch -P 2001 -p 1
%endif


%build
make \
        INSTALL_ROOT="%{buildroot}" \
        INSTALL_BIN="%{buildroot}%{_bindir}" \
        INSTALL_LIB="%{buildroot}%{_libdir}" \
        INSTALL_INCLUDE="%{buildroot}%{_includedir}" \
        INSTALL_ETC="%{buildroot}%{_sysconfdir}" \
        INSTALL_SHARE="%{buildroot}%{_datadir}" \
        INSTALL_RULES="%{buildroot}/lib/udev/rules.d" \
        INSTALL_FIRMWARE="%{buildroot}/lib/firmware" \
        all


%install
make \
        INSTALL_ROOT="%{buildroot}" \
        INSTALL_BIN="%{buildroot}%{_bindir}" \
        INSTALL_LIB="%{buildroot}%{_libdir}" \
        INSTALL_INCLUDE="%{buildroot}%{_includedir}" \
        INSTALL_ETC="%{buildroot}%{_sysconfdir}" \
        INSTALL_SHARE="%{buildroot}%{_datadir}" \
        INSTALL_RULES="%{buildroot}/lib/udev/rules.d" \
        INSTALL_FIRMWARE="%{buildroot}/lib/firmware" \
        install

rm %{buildroot}/sbin/fxload
rmdir %{buildroot}/sbin

%ifarch aarch64
install -d %{buildroot}%{_bindir}
install -m 0755 tools/rpi_ctrl.sh %{buildroot}%{_bindir}
install -m 0755 tools/rpi_ctrl_v2.sh %{buildroot}%{_bindir}
install -m 0755 tools/wifi_channel_selector.pl %{buildroot}%{_bindir}
%endif

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir %{buildroot}%{_sharedstatedir}/%{name}

cp %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-server.service
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-server

# Install more tools
install -m 0755 build/bin/indigo_drivers %{buildroot}%{_bindir}
install -m 0755 build/bin/indigo_driver_metadata %{buildroot}%{_bindir}
install -m 0755 build/bin/indigo_generator %{buildroot}%{_bindir}
install -m 0755 build/bin/indigo_scan_drivers %{buildroot}%{_bindir}


%files server-free
%{_bindir}/indigo_ao_sx
%{_bindir}/indigo_aux_arteskyflat
%{_bindir}/indigo_aux_asiair
%{_bindir}/indigo_aux_astromechanics
%{_bindir}/indigo_aux_cloudwatcher
%{_bindir}/indigo_aux_dragonfly
%{_bindir}/indigo_aux_fbc
%{_bindir}/indigo_aux_flatmaster
%{_bindir}/indigo_aux_flipflat
%{_bindir}/indigo_aux_geoptikflat
%{_bindir}/indigo_aux_joystick
%{_bindir}/indigo_aux_mgbox
%{_bindir}/indigo_aux_ppb
%{_bindir}/indigo_aux_rpio
%{_bindir}/indigo_aux_rts
%{_bindir}/indigo_aux_skyalert
%{_bindir}/indigo_aux_sqm
%{_bindir}/indigo_aux_svbpowerbox
%{_bindir}/indigo_aux_uch
%{_bindir}/indigo_aux_upb
%{_bindir}/indigo_aux_upb3
%{_bindir}/indigo_aux_usbdp
%{_bindir}/indigo_aux_wbplusv3
%{_bindir}/indigo_aux_wbprov3
%{_bindir}/indigo_aux_wcv4ec
%{_bindir}/indigo_ccd_dsi
%{_bindir}/indigo_ccd_fli
%{_bindir}/indigo_ccd_iidc
%{_bindir}/indigo_ccd_ptp
%{_bindir}/indigo_ccd_simulator
%{_bindir}/indigo_ccd_ssag
%{_bindir}/indigo_ccd_sx
%{_bindir}/indigo_ccd_uvc
%{_bindir}/indigo_dome_baader
%{_bindir}/indigo_dome_beaver
%{_bindir}/indigo_dome_dragonfly
%{_bindir}/indigo_dome_nexdome
%{_bindir}/indigo_dome_nexdome3
%{_bindir}/indigo_dome_simulator
%{_bindir}/indigo_dome_skyroof
%{_bindir}/indigo_dome_talon6ror
%{_bindir}/indigo_focuser_askar
%{_bindir}/indigo_focuser_astromechanics
%{_bindir}/indigo_focuser_dmfc
%{_bindir}/indigo_focuser_dsd
%{_bindir}/indigo_focuser_efa
%{_bindir}/indigo_focuser_fc3
%{_bindir}/indigo_focuser_fli
%{_bindir}/indigo_focuser_focusdreampro
%{_bindir}/indigo_focuser_ioptron
%{_bindir}/indigo_focuser_lacerta
%{_bindir}/indigo_focuser_lakeside
%{_bindir}/indigo_focuser_lunatico
%{_bindir}/indigo_focuser_mjkzz
%{_bindir}/indigo_focuser_moonlite
%{_bindir}/indigo_focuser_mypro2
%{_bindir}/indigo_focuser_nfocus
%{_bindir}/indigo_focuser_nstep
%{_bindir}/indigo_focuser_optec
%{_bindir}/indigo_focuser_optecfl
%{_bindir}/indigo_focuser_primaluce
%{_bindir}/indigo_focuser_prodigy
%{_bindir}/indigo_focuser_qhy
%{_bindir}/indigo_focuser_robofocus
%{_bindir}/indigo_focuser_steeldrive2
%{_bindir}/indigo_focuser_usbv3
%{_bindir}/indigo_focuser_wemacro
%{_bindir}/indigo_gps_gpsd
%{_bindir}/indigo_gps_nmea
%{_bindir}/indigo_gps_simulator
%{_bindir}/indigo_guider_cgusbst4
%{_bindir}/indigo_mount_asi
%{_bindir}/indigo_mount_ioptron
%{_bindir}/indigo_mount_lx200
%{_bindir}/indigo_mount_nexstar
%{_bindir}/indigo_mount_nexstaraux
%{_bindir}/indigo_mount_pmc8
%{_bindir}/indigo_mount_rainbow
%{_bindir}/indigo_mount_simulator
%{_bindir}/indigo_mount_starbook
%{_bindir}/indigo_mount_synscan
%{_bindir}/indigo_mount_temma
%{_bindir}/indigo_rotator_falcon
%{_bindir}/indigo_rotator_lunatico
%{_bindir}/indigo_rotator_optec
%{_bindir}/indigo_rotator_simulator
%{_bindir}/indigo_rotator_wa
%{_bindir}/indigo_server
%{_bindir}/indigo_system_ascol
%{_bindir}/indigo_wheel_fli
%{_bindir}/indigo_wheel_indigo
%{_bindir}/indigo_wheel_manual
%{_bindir}/indigo_wheel_optec
%{_bindir}/indigo_wheel_qhy
%{_bindir}/indigo_wheel_quantum
%{_bindir}/indigo_wheel_sx
%{_bindir}/indigo_wheel_trutek
%{_bindir}/indigo_wheel_xagyl

%{_bindir}/indigo_prop_tool
%{_bindir}/indigo_raw_crop
%{_bindir}/indigo_raw_to_fits
%{_bindir}/indigo_list_usbserial
%{_bindir}/indigo_log_analyzer
%{_bindir}/indigo_drivers
%{_bindir}/indigo_driver_metadata
%{_bindir}/indigo_generator
%{_bindir}/indigo_scan_drivers

%{_libdir}/indigo_agent_alpaca.so
%{_libdir}/indigo_agent_astap.so
%{_libdir}/indigo_agent_astrometry.so
%{_libdir}/indigo_agent_auxiliary.so
%{_libdir}/indigo_agent_config.so
%{_libdir}/indigo_agent_guider.so
%{_libdir}/indigo_agent_imager.so
%{_libdir}/indigo_agent_mount.so
%{_libdir}/indigo_agent_scripting.so
%{_libdir}/indigo_agent_snoop.so
%{_libdir}/indigo_agent_solver.so
%{_libdir}/indigo_ao_sx.so
%{_libdir}/indigo_aux_arteskyflat.so
%{_libdir}/indigo_aux_asiair.so
%{_libdir}/indigo_aux_astromechanics.so
%{_libdir}/indigo_aux_cloudwatcher.so
%{_libdir}/indigo_aux_dragonfly.so
%{_libdir}/indigo_aux_fbc.so
%{_libdir}/indigo_aux_flatmaster.so
%{_libdir}/indigo_aux_flipflat.so
%{_libdir}/indigo_aux_geoptikflat.so
%{_libdir}/indigo_aux_joystick.so
%{_libdir}/indigo_aux_mgbox.so
%{_libdir}/indigo_aux_ppb.so
%{_libdir}/indigo_aux_rpio.so
%{_libdir}/indigo_aux_rts.so
%{_libdir}/indigo_aux_skyalert.so
%{_libdir}/indigo_aux_sqm.so
%{_libdir}/indigo_aux_svbpowerbox.so
%{_libdir}/indigo_aux_uch.so
%{_libdir}/indigo_aux_upb.so
%{_libdir}/indigo_aux_upb3.so
%{_libdir}/indigo_aux_usbdp.so
%{_libdir}/indigo_aux_wbplusv3.so
%{_libdir}/indigo_aux_wbprov3.so
%{_libdir}/indigo_aux_wcv4ec.so
%{_libdir}/indigo_ccd_dsi.so
%{_libdir}/indigo_ccd_fli.so
%{_libdir}/indigo_ccd_iidc.so
%{_libdir}/indigo_ccd_ptp.so
%{_libdir}/indigo_ccd_simulator.so
%{_libdir}/indigo_ccd_ssag.so
%{_libdir}/indigo_ccd_sx.so
%{_libdir}/indigo_ccd_uvc.so
%{_libdir}/indigo_dome_baader.so
%{_libdir}/indigo_dome_beaver.so
%{_libdir}/indigo_dome_dragonfly.so
%{_libdir}/indigo_dome_nexdome.so
%{_libdir}/indigo_dome_nexdome3.so
%{_libdir}/indigo_dome_simulator.so
%{_libdir}/indigo_dome_skyroof.so
%{_libdir}/indigo_dome_talon6ror.so
%{_libdir}/indigo_focuser_askar.so
%{_libdir}/indigo_focuser_astromechanics.so
%{_libdir}/indigo_focuser_dmfc.so
%{_libdir}/indigo_focuser_dsd.so
%{_libdir}/indigo_focuser_efa.so
%{_libdir}/indigo_focuser_fc3.so
%{_libdir}/indigo_focuser_fli.so
%{_libdir}/indigo_focuser_focusdreampro.so
%{_libdir}/indigo_focuser_ioptron.so
%{_libdir}/indigo_focuser_lacerta.so
%{_libdir}/indigo_focuser_lakeside.so
%{_libdir}/indigo_focuser_lunatico.so
%{_libdir}/indigo_focuser_mjkzz.so
%{_libdir}/indigo_focuser_moonlite.so
%{_libdir}/indigo_focuser_mypro2.so
%{_libdir}/indigo_focuser_nfocus.so
%{_libdir}/indigo_focuser_nstep.so
%{_libdir}/indigo_focuser_optec.so
%{_libdir}/indigo_focuser_optecfl.so
%{_libdir}/indigo_focuser_primaluce.so
%{_libdir}/indigo_focuser_prodigy.so
%{_libdir}/indigo_focuser_qhy.so
%{_libdir}/indigo_focuser_robofocus.so
%{_libdir}/indigo_focuser_steeldrive2.so
%{_libdir}/indigo_focuser_usbv3.so
%{_libdir}/indigo_focuser_wemacro.so
%{_libdir}/indigo_gps_gpsd.so
%{_libdir}/indigo_gps_nmea.so
%{_libdir}/indigo_gps_simulator.so
%{_libdir}/indigo_guider_cgusbst4.so
%{_libdir}/indigo_mount_asi.so
%{_libdir}/indigo_mount_ioptron.so
%{_libdir}/indigo_mount_lx200.so
%{_libdir}/indigo_mount_nexstar.so
%{_libdir}/indigo_mount_nexstaraux.so
%{_libdir}/indigo_mount_pmc8.so
%{_libdir}/indigo_mount_rainbow.so
%{_libdir}/indigo_mount_simulator.so
%{_libdir}/indigo_mount_starbook.so
%{_libdir}/indigo_mount_synscan.so
%{_libdir}/indigo_mount_temma.so
%{_libdir}/indigo_rotator_falcon.so
%{_libdir}/indigo_rotator_lunatico.so
%{_libdir}/indigo_rotator_optec.so
%{_libdir}/indigo_rotator_simulator.so
%{_libdir}/indigo_rotator_wa.so
%{_libdir}/indigo_system_ascol.so
%{_libdir}/indigo_wheel_fli.so
%{_libdir}/indigo_wheel_indigo.so
%{_libdir}/indigo_wheel_manual.so
%{_libdir}/indigo_wheel_optec.so
%{_libdir}/indigo_wheel_qhy.so
%{_libdir}/indigo_wheel_quantum.so
%{_libdir}/indigo_wheel_sx.so
%{_libdir}/indigo_wheel_trutek.so
%{_libdir}/indigo_wheel_xagyl.so
%{_libdir}/libindigo.so
%{_libdir}/libindigocat.so

/usr/sbin/fxload

/lib/firmware/meade-deepskyimager.hex

/lib/udev/rules.d/99-indigo_aux_arteskyflat.rules
/lib/udev/rules.d/99-indigo_aux_fbc.rules
/lib/udev/rules.d/99-indigo_aux_flatmaster.rules
/lib/udev/rules.d/99-indigo_aux_ppb.rules
/lib/udev/rules.d/99-indigo_aux_uch.rules
/lib/udev/rules.d/99-indigo_aux_upb.rules
/lib/udev/rules.d/99-indigo_aux_upb3.rules
/lib/udev/rules.d/99-indigo_ccd_dsi.rules
/lib/udev/rules.d/99-indigo_ccd_fli.rules
/lib/udev/rules.d/99-indigo_ccd_ssag.rules
/lib/udev/rules.d/99-indigo_ccd_sx.rules
/lib/udev/rules.d/99-indigo_ccd_uvc.rules
/lib/udev/rules.d/99-indigo_focuser_dmfc.rules
/lib/udev/rules.d/99-indigo_focuser_efa.rules
/lib/udev/rules.d/99-indigo_focuser_fc3.rules
/lib/udev/rules.d/99-indigo_focuser_prodigy.rules
/lib/udev/rules.d/99-indigo_focuser_usbv3.rules
/lib/udev/rules.d/99-indigo_focuser_wemacro.rules
/lib/udev/rules.d/99-indigo_gps_nmea.rules
/lib/udev/rules.d/99-indigo_mount_asi.rules
/lib/udev/rules.d/99-indigo_mount_lx200.rules
/lib/udev/rules.d/99-indigo_rotator_falcon.rules
/lib/udev/rules.d/99-indigo_wheel_sx.rules

%ifarch aarch64
%{_bindir}/rpi_ctrl.sh
%{_bindir}/rpi_ctrl_v2.sh
%{_bindir}/wifi_channel_selector.pl
%endif

%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}-server.service
%attr(0640,root,%{name}) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server


%if %{free}
%files server-drivers-list-free
%{_datadir}/indigo/indigo_drivers
%{_datadir}/indigo/indigo_linux_drivers
%else
%files server-drivers-nonfree
%{_bindir}/indigo_aux_dsusb
%{_bindir}/indigo_ccd_altair
%{_bindir}/indigo_ccd_apogee
%{_bindir}/indigo_ccd_asi
%{_bindir}/indigo_ccd_atik
%{_bindir}/indigo_ccd_baccam
%{_bindir}/indigo_ccd_bresser
%{_bindir}/indigo_ccd_mallin
%{_bindir}/indigo_ccd_meade
%{_bindir}/indigo_ccd_mi
%{_bindir}/indigo_ccd_ogma
%{_bindir}/indigo_ccd_omegonpro
%{_bindir}/indigo_ccd_playerone
%{_bindir}/indigo_ccd_qhy
%{_bindir}/indigo_ccd_qhy2
%{_bindir}/indigo_ccd_qsi
%{_bindir}/indigo_ccd_rising
%{_bindir}/indigo_ccd_sbig
%{_bindir}/indigo_ccd_ssg
%{_bindir}/indigo_ccd_svb
%{_bindir}/indigo_ccd_svb2
%{_bindir}/indigo_ccd_touptek
%{_bindir}/indigo_focuser_asi
%{_bindir}/indigo_focuser_astroasis
%{_bindir}/indigo_focuser_fcusb
%{_bindir}/indigo_guider_asi
%{_bindir}/indigo_guider_gpusb
%{_bindir}/indigo_rotator_asi
%{_bindir}/indigo_wheel_asi
%{_bindir}/indigo_wheel_astroasis
%{_bindir}/indigo_wheel_atik
%{_bindir}/indigo_wheel_mi
%{_bindir}/indigo_wheel_playerone

%{_libdir}/indigo_aux_dsusb.so
%{_libdir}/indigo_ccd_altair.so
%{_libdir}/indigo_ccd_apogee.so
%{_libdir}/indigo_ccd_asi.so
%{_libdir}/indigo_ccd_atik.so
%{_libdir}/indigo_ccd_baccam.so
%{_libdir}/indigo_ccd_bresser.so
%{_libdir}/indigo_ccd_mallin.so
%{_libdir}/indigo_ccd_meade.so
%{_libdir}/indigo_ccd_mi.so
%{_libdir}/indigo_ccd_ogma.so
%{_libdir}/indigo_ccd_omegonpro.so
%{_libdir}/indigo_ccd_playerone.so
%{_libdir}/indigo_ccd_qhy.so
%{_libdir}/indigo_ccd_qhy2.so
%{_libdir}/indigo_ccd_qsi.so
%{_libdir}/indigo_ccd_rising.so
%{_libdir}/indigo_ccd_sbig.so
%{_libdir}/indigo_ccd_ssg.so
%{_libdir}/indigo_ccd_svb.so
%{_libdir}/indigo_ccd_svb2.so
%{_libdir}/indigo_ccd_touptek.so
%{_libdir}/indigo_focuser_asi.so
%{_libdir}/indigo_focuser_astroasis.so
%{_libdir}/indigo_focuser_fcusb.so
%{_libdir}/indigo_guider_asi.so
%{_libdir}/indigo_guider_gpusb.so
%{_libdir}/indigo_rotator_asi.so
%{_libdir}/indigo_wheel_asi.so
%{_libdir}/indigo_wheel_astroasis.so
%{_libdir}/indigo_wheel_atik.so
%{_libdir}/indigo_wheel_mi.so
%{_libdir}/indigo_wheel_playerone.so

%{_libdir}/libPlayerOneCamera.so
%{_libdir}/libPlayerOnePW.so
%{_libdir}/libaltaircam.so
%{_libdir}/libatikcameras.so
%{_libdir}/libbaccam.so
%{_libdir}/libbressercam.so
%{_libdir}/libmallincam.so
%{_libdir}/libmeadecam.so
%{_libdir}/libnncam.so
%{_libdir}/libogmacam.so
%{_libdir}/libomegonprocam.so
%{_libdir}/libqhyccd.so
%{_libdir}/libstarshootg.so
%{_libdir}/libsvbonycam.so
%{_libdir}/libtoupcam.so

%{_libdir}/libPlayerOneCamera.so.3
%{_libdir}/libPlayerOnePW.so.1
%{_libdir}/libqhyccd.so.20

/lib/firmware/qhy/IC16200A.HEX
/lib/firmware/qhy/IC16803.HEX
/lib/firmware/qhy/IC8300.HEX
/lib/firmware/qhy/IC90A.HEX
/lib/firmware/qhy/IMG0H.HEX
/lib/firmware/qhy/IMG2P.HEX
/lib/firmware/qhy/IMG2S.HEX
/lib/firmware/qhy/IMG50.HEX
/lib/firmware/qhy/POLEMASTER.HEX
/lib/firmware/qhy/QHY0204.img
/lib/firmware/qhy/QHY09000A.HEX
/lib/firmware/qhy/QHY10.HEX
/lib/firmware/qhy/QHY10768.img
/lib/firmware/qhy/QHY11.HEX
/lib/firmware/qhy/QHY12.HEX
/lib/firmware/qhy/QHY1253.img
/lib/firmware/qhy/QHY128.img
/lib/firmware/qhy/QHY128PRO.img
/lib/firmware/qhy/QHY15.HEX
/lib/firmware/qhy/QHY16.HEX
/lib/firmware/qhy/QHY16000.HEX
/lib/firmware/qhy/QHY160002AD.HEX
/lib/firmware/qhy/QHY16200A.HEX
/lib/firmware/qhy/QHY163.img
/lib/firmware/qhy/QHY165.img
/lib/firmware/qhy/QHY168.img
/lib/firmware/qhy/QHY16803A.HEX
/lib/firmware/qhy/QHY174.img
/lib/firmware/qhy/QHY178.img
/lib/firmware/qhy/QHY183.img
/lib/firmware/qhy/QHY183A.img
/lib/firmware/qhy/QHY1920.img
/lib/firmware/qhy/QHY2.HEX
/lib/firmware/qhy/QHY20.HEX
/lib/firmware/qhy/QHY2020.img
/lib/firmware/qhy/QHY21.HEX
/lib/firmware/qhy/QHY22.HEX
/lib/firmware/qhy/QHY224.img
/lib/firmware/qhy/QHY23.HEX
/lib/firmware/qhy/QHY247.img
/lib/firmware/qhy/QHY268.img
/lib/firmware/qhy/QHY27.HEX
/lib/firmware/qhy/QHY28.HEX
/lib/firmware/qhy/QHY29.HEX
/lib/firmware/qhy/QHY290.img
/lib/firmware/qhy/QHY294.img
/lib/firmware/qhy/QHY294PRO.img
/lib/firmware/qhy/QHY2E.HEX
/lib/firmware/qhy/QHY2PRO.HEX
/lib/firmware/qhy/QHY342.img
/lib/firmware/qhy/QHY342PRO.img
/lib/firmware/qhy/QHY367.img
/lib/firmware/qhy/QHY367PRO.img
/lib/firmware/qhy/QHY4040.img
/lib/firmware/qhy/QHY4040PRO.img
/lib/firmware/qhy/QHY410.img
/lib/firmware/qhy/QHY411.img
/lib/firmware/qhy/QHY411ERIS.img
/lib/firmware/qhy/QHY411_1.3.3.img
/lib/firmware/qhy/QHY42.img
/lib/firmware/qhy/QHY42PRO.img
/lib/firmware/qhy/QHY432.img
/lib/firmware/qhy/QHY461.img
/lib/firmware/qhy/QHY487.img
/lib/firmware/qhy/QHY5.HEX
/lib/firmware/qhy/QHY530.img
/lib/firmware/qhy/QHY533.img
/lib/firmware/qhy/QHY550.img
/lib/firmware/qhy/QHY5II.HEX
/lib/firmware/qhy/QHY5III174.img
/lib/firmware/qhy/QHY5III178.img
/lib/firmware/qhy/QHY5III185.img
/lib/firmware/qhy/QHY5III200.img
/lib/firmware/qhy/QHY5III224.img
/lib/firmware/qhy/QHY5III290.img
/lib/firmware/qhy/QHY5III334.img
/lib/firmware/qhy/QHY5III415.img
/lib/firmware/qhy/QHY5III462.img
/lib/firmware/qhy/QHY5III482.img
/lib/firmware/qhy/QHY5III485.img
/lib/firmware/qhy/QHY5III568.img
/lib/firmware/qhy/QHY5III585.img
/lib/firmware/qhy/QHY5III678.img
/lib/firmware/qhy/QHY5III715.img
/lib/firmware/qhy/QHY5LOADER.HEX
/lib/firmware/qhy/QHY6.HEX
/lib/firmware/qhy/QHY600-9267-1203.img
/lib/firmware/qhy/QHY600.img
/lib/firmware/qhy/QHY600ERIS-12-qxx.img
/lib/firmware/qhy/QHY6060.img
/lib/firmware/qhy/QHY6060PRO.img
/lib/firmware/qhy/QHY695A.HEX
/lib/firmware/qhy/QHY7.HEX
/lib/firmware/qhy/QHY8.HEX
/lib/firmware/qhy/QHY811.img
/lib/firmware/qhy/QHY814A.HEX
/lib/firmware/qhy/QHY8L.HEX
/lib/firmware/qhy/QHY8M.HEX
/lib/firmware/qhy/QHY8PRO.HEX
/lib/firmware/qhy/QHY90A.HEX
/lib/firmware/qhy/QHY9701.img
/lib/firmware/qhy/QHY990.img
/lib/firmware/qhy/QHY991.img
/lib/firmware/qhy/QHY992.img
/lib/firmware/qhy/QHY9S.HEX
/lib/firmware/qhy/miniCam5.HEX
/lib/firmware/qhy/miniCam8.img
/lib/firmware/sbigfcam.hex
/lib/firmware/sbiglcam.hex
/lib/firmware/sbigpcam.hex
/lib/firmware/sbigucam.hex
/lib/firmware/stfga.bin

/lib/udev/rules.d/99-indigo_aux_dsusb.rules
/lib/udev/rules.d/99-indigo_ccd_altair.rules
/lib/udev/rules.d/99-indigo_ccd_apogee.rules
/lib/udev/rules.d/99-indigo_ccd_asi.rules
/lib/udev/rules.d/99-indigo_ccd_atik.rules
/lib/udev/rules.d/99-indigo_ccd_baccam.rules
/lib/udev/rules.d/99-indigo_ccd_bresser.rules
/lib/udev/rules.d/99-indigo_ccd_mallin.rules
/lib/udev/rules.d/99-indigo_ccd_meade.rules
/lib/udev/rules.d/99-indigo_ccd_mi.rules
/lib/udev/rules.d/99-indigo_ccd_ogma.rules
/lib/udev/rules.d/99-indigo_ccd_omegonpro.rules
/lib/udev/rules.d/99-indigo_ccd_playerone.rules
/lib/udev/rules.d/99-indigo_ccd_qhy.rules
/lib/udev/rules.d/99-indigo_ccd_qsi.rules
/lib/udev/rules.d/99-indigo_ccd_rising.rules
/lib/udev/rules.d/99-indigo_ccd_sbig.rules
/lib/udev/rules.d/99-indigo_ccd_ssg.rules
/lib/udev/rules.d/99-indigo_ccd_svb.rules
/lib/udev/rules.d/99-indigo_ccd_svb2.rules
/lib/udev/rules.d/99-indigo_ccd_touptek.rules
/lib/udev/rules.d/99-indigo_focuser_asi.rules
/lib/udev/rules.d/99-indigo_focuser_astroasis.rules
/lib/udev/rules.d/99-indigo_focuser_fcusb.rules
/lib/udev/rules.d/99-indigo_guider_asi.rules
/lib/udev/rules.d/99-indigo_guider_gpusb.rules
/lib/udev/rules.d/99-indigo_rotator_asi.rules
/lib/udev/rules.d/99-indigo_wheel_asi.rules
/lib/udev/rules.d/99-indigo_wheel_astroasis.rules
/lib/udev/rules.d/99-indigo_wheel_playerone.rules

%dir %{_sysconfdir}/apogee
%config(noreplace) %{_sysconfdir}/apogee/*.txt


%files server-drivers-list-nonfree
%{_datadir}/indigo/indigo_drivers
%{_datadir}/indigo/indigo_linux_drivers
%endif


%files server-client-libs-free
%{_libdir}/libindigo_client.so


%files free-devel
%{_includedir}/indigo

%{_libdir}/libindigo.a
%{_libdir}/libindigo_client.a
%{_libdir}/libindigocat.a


%pre server-free
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
        useradd -r -s /sbin/nologin -d %{_sharedstatedir}/%{name} -M \
        -G dialout,video \
        -c 'INDIGO astronomy software platform' -g %{name} %{name}
exit 0


%post server-free
%systemd_post %{name}.service


%preun server-free
%systemd_preun '%{name}.service'


%postun server-free
%systemd_postun_with_restart '%{name}.service'


%changelog
