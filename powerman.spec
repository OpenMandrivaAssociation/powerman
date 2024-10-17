%define	major 0
%define libname	%mklibname powerman  %{major}
%define devname %mklibname -d powerman

Summary:	Power to the Cluster
Name:		powerman
Version:	2.3.26
Release:	2
Group:		System/Servers
License:	GPLv2+
Url:		https://code.google.com/p/powerman/
Source0:	https://github.com/chaos/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:		powerman-2.3.26-var_run-to-run.patch

BuildRequires:  git
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	genders-devel
BuildRequires:	net-snmp
BuildRequires:	readline-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:  pkgconfig(systemd)
Requires(post,preun,pre,postun): rpm-helper
Requires(post):	systemd

%description
PowerMan is a tool for manipulating remote power control (RPC) devices from a 
central location. Several RPC varieties are supported natively by PowerMan and 
Expect-like configurability simplifies the addition of new devices.

%package -n	%{libname}
Summary:	PowerMan library
Group:          System/Libraries

%description -n	%{libname}
PowerMan is a tool for manipulating remote power control (RPC) devices from a 
central location. Several RPC varieties are supported natively by PowerMan and 
Expect-like configurability simplifies the addition of new devices.

%package -n	%{devname}
Summary:	Development library and header files for the PowerMan library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
This package contains the development genders library and its header files.

%prep
%setup -q

%build
autoreconf -i
%configure \
	--disable-static \
	--with-snmppower \
	--with-httppower \
	--with-genders \
	--with-ncurses \
	--with-user=powerman \
	--with-systemdsystemunitdir=%{_unitdir}

%make_build

%install
%make_install

find %{buildroot} -name "*.la" -delete

# get rid of execute bit on powerman script files to fix rpmlint errror
chmod -x %{buildroot}%{_sysconfdir}/%{name}/*

# don't package this for now
rm -rf %{buildroot}%{_libdir}/stonith

%pre
%_pre_useradd powerman /var/empty /bin/sh

%postun
%_postun_userdel powerman

%post
%_tmpfilescreate %{name}
%_post_service powerman

%preun
%_preun_service powerman

%files
%doc ChangeLog DISCLAIMER COPYING NEWS TODO
%{_initrddir}/%{name}
%{_bindir}/pm
%{_bindir}/powerman
%{_sbindir}/httppower
%{_sbindir}/plmpower
%{_sbindir}/powermand
%{_sbindir}/snmppower
%{_sbindir}/vpcd
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_mandir}/man*/*
%attr(0755,powerman,powerman) %dir /var/run/%{name}

%files -n %{libname}
%{_libdir}/libpowerman.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

