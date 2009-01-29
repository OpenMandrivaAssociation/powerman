%define	major 0
%define libname	%mklibname powerman  %{major}
%define develname %mklibname -d powerman

%define snap r1109

Summary:	Power to the Cluster
Name:		powerman
Version:	2.3.3
Release:	%mkrel 0.%{snap}.1
Group:		System/Servers
License:	GPLv2+
URL:		http://sourceforge.net/projects/powerman
#Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Source0:	powerman-2.3.3-r1109.tar.gz
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	genders-devel
BuildRequires:	libcurl-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcp_wrappers-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{develname}
Summary:	Static library and header files for the PowerMan library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{develname}
PowerMan is a tool for manipulating remote power control (RPC) devices from a 
central location. Several RPC varieties are supported natively by PowerMan and 
Expect-like configurability simplifies the addition of new devices.

This package contains the static genders library and its header files.

%prep

%setup -q

%build
sh ./autogen.sh
%serverbuild
%configure2_5x \
    --with-httppower \
    --with-genders \
    --with-ncurses \
    -with-user=powerman
      
# parallel makes often fail
make -e VERSION=%{version} EXTRA_CFLAGS="$CFLAGS"

%install
rm -rf %{buildroot}

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
%{__perl} -pi -e 's|chkconfig:.*95 5|chkconfig: - 95 5|g' %{buildroot}%{_initrddir}/%{name}

%pre
%_pre_useradd powerman /var/empty /bin/sh

%postun
%_postun_userdel powerman

%post
%_post_service powerman

%preun
%_preun_service powerman

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog DISCLAIMER COPYING NEWS TODO
%{_initrddir}/%{name}
%{_bindir}/powerman
%{_bindir}/pm
%{_sbindir}/plmpower
%{_sbindir}/powermand
%{_sbindir}/httppower
%{_sbindir}/vpcd
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_mandir}/man*/*
%attr(0755,powerman,powerman) %dir /var/run/%{name}

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

