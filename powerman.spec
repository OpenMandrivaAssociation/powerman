%define	major 0
%define libname	%mklibname powerman  %{major}
%define develname %mklibname -d powerman

Summary:	Power to the Cluster
Name:		powerman
Version:	2.3.9
Release:	%mkrel 3
Group:		System/Servers
License:	GPLv2+
URL:		http://code.google.com/p/powerman/
Source0:	http://powerman.googlecode.com/files/powerman-%{version}.tar.gz
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	genders-devel
BuildRequires:	libcurl-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
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
#sh ./autogen.sh
%serverbuild

%configure2_5x \
    --with-snmppower \
    --with-httppower \
    --with-genders \
    --with-ncurses \
    --with-user=powerman

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
%defattr(-,root,root)
%doc COPYING
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.*a
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Jun 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.9-1mdv2011.0
+ Revision: 682908
- 2.3.9

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.5-4
+ Revision: 667811
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.5-3mdv2011.0
+ Revision: 607197
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.5-2mdv2010.1
+ Revision: 519057
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.5-1mdv2010.0
+ Revision: 387850
- 2.3.5

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.4-1mdv2009.1
+ Revision: 353769
- 2.3.4

* Thu Jan 29 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.3-0.r1109.1mdv2009.1
+ Revision: 335063
- import powerman


* Thu Jan 29 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.3-0.r1109.1mdv2009.1
- initial Mandriva package
