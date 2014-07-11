%define	major 0
%define libname	%mklibname powerman  %{major}
%define devname %mklibname -d powerman

Summary:	Power to the Cluster
Name:		powerman
Version:	2.3.9
Release:	9
Group:		System/Servers
License:	GPLv2+
Url:		http://code.google.com/p/powerman/
Source0:	http://powerman.googlecode.com/files/powerman-%{version}.tar.gz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	genders-devel
BuildRequires:	net-snmp-devel
BuildRequires:	readline-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ncurses)
Requires(post,preun,pre,postun): rpm-helper

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
%serverbuild
%configure2_5x \
	--disable-static \
	--with-snmppower \
	--with-httppower \
	--with-genders \
	--with-ncurses \
	--with-user=powerman

# parallel makes often fail
make -e VERSION=%{version} EXTRA_CFLAGS="$CFLAGS"

%install
install -d %{buildroot}%{_initrddir}

%makeinstall_std mandir=%{_mandir}

# work around a problem in the install make file target
rm %{buildroot}%{_bindir}/pm
pushd %{buildroot}%{_bindir}
    ln -s powerman pm
popd

# get rid of execute bit on powerman script files to fix rpmlint errror
chmod -x %{buildroot}%{_sysconfdir}/%{name}/*

mv %{buildroot}%{_sysconfdir}/init.d/%{name} %{buildroot}%{_initrddir}/

# Don't turn on by default
perl -pi -e 's|chkconfig:.*95 5|chkconfig: - 95 5|g' %{buildroot}%{_initrddir}/%{name}

# don't package this for now
rm -rf %{buildroot}%{_libdir}/stonith

%pre
%_pre_useradd powerman /var/empty /bin/sh

%postun
%_postun_userdel powerman

%post
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

