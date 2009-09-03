%define	major 0
%define libname %mklibname ft %{major}
%define develname %mklibname ft -d

Summary:	Tool set for working with NetFlow data
Name:		flow-tools
Version:	0.68
Release:	%mkrel 6
License:	BSD
Group:		Monitoring
URL:		http://www.splintered.net/sw/flow-tools/
Source0:	ftp://ftp.eng.oar.net/pub/flow-tools/%{name}-%{version}.tar.bz2
Source1:	flow-capture.init
Source2:	flow-capture.conf
Patch0:		flow-tools-0.67-shared.diff
Patch1:		flow-tools-0.68-debug.diff
Patch2:		flow-tools-0.68-gcc4.diff
Patch3:		flow-tools-libtool_fixes.diff
Requires:	tcp_wrappers
BuildRequires:	docbook-utils
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	zlib-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
#BuildRequires:	mysql-devel
#BuildRequires:	postgresql-libs-devel
#BuildRequires:	postgresql-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Flow-tools is library and a collection of programs used to
collect, send, process, and generate reports from NetFlow data.
The tools can be used together on a single server or distributed
to multiple servers for large deployments. The flow-toools library
provides an API for development of custom applications for NetFlow
export versions 1,5,6 and the 14 currently defined version 8
subversions.

%package -n	%{libname}
Summary:	Flow-tools shared libraries
Group:          System/Libraries

%description -n	%{libname}
Flow-tools is library and a collection of programs used to
collect, send, process, and generate reports from NetFlow data.
The tools can be used together on a single server or distributed
to multiple servers for large deployments. The flow-toools library
provides an API for development of custom applications for NetFlow
export versions 1,5,6 and the 14 currently defined version 8
subversions.

%package -n	%{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel libft-devel
Obsoletes:	%{name}-devel
Obsoletes:	%{mklibname ft 0 -d}

%description -n	%{develname}
Flow-tools is library and a collection of programs used to
collect, send, process, and generate reports from NetFlow data.
The tools can be used together on a single server or distributed
to multiple servers for large deployments. The flow-toools library
provides an API for development of custom applications for NetFlow
export versions 1,5,6 and the 14 currently defined version 8
subversions.

%package -n	flow-capture
Summary:	Manage storage of flow file archives by expiring old data
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	flow-tools = %{version}-%{release}

%description -n	flow-capture
The flow-capture utility will receive and store NetFlow exports to
disk.

%prep

%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

cp %{SOURCE1} flow-capture.init
cp %{SOURCE2} flow-capture.conf

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing

%configure2_5x \
    --bindir=%{_sbindir} \
    --localstatedir=%{_sysconfdir}/ft \
    --enable-lfs

#    --with-mysql=%{_prefix} \
#    --with-pgsql=%{_prefix}

%make CFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%makeinstall \
    localstatedir=%{buildroot}%{_sysconfdir}/ft \
    bindir=%{buildroot}%{_sbindir}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/ft
install -d %{buildroot}/var/lib/flow-capture

install -m0755 flow-capture.init %{buildroot}%{_initrddir}/flow-capture
install -m0644 flow-capture.conf %{buildroot}%{_sysconfdir}/flow-capture.conf

# python path fix
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-log2rrd
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-rpt2rrd
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-rptfmt

%post -n flow-capture
%_post_service flow-capture

%preun -n flow-capture
%_preun_service flow-capture

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README SECURITY TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ft/cfg/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ft/sym/*
%dir %{_sysconfdir}/ft
%{_sbindir}/flow-cat
%{_sbindir}/flow-dscan
%{_sbindir}/flow-expire
%{_sbindir}/flow-export
%{_sbindir}/flow-fanout
%{_sbindir}/flow-filter
%{_sbindir}/flow-gen
%{_sbindir}/flow-header
%{_sbindir}/flow-import
%{_sbindir}/flow-mask
%{_sbindir}/flow-merge
%{_sbindir}/flow-nfilter
%{_sbindir}/flow-print
%{_sbindir}/flow-receive
%{_sbindir}/flow-report
%{_sbindir}/flow-send
%{_sbindir}/flow-split
%{_sbindir}/flow-stat
%{_sbindir}/flow-tag
%{_sbindir}/flow-xlate
%{_sbindir}/flow-log2rrd
%{_sbindir}/flow-rpt2rrd
%{_sbindir}/flow-rptfmt
%{_mandir}/man1/flow-cat.1*
%{_mandir}/man1/flow-dscan.1*
%{_mandir}/man1/flow-expire.1*
%{_mandir}/man1/flow-export.1*
%{_mandir}/man1/flow-fanout.1*
%{_mandir}/man1/flow-filter.1*
%{_mandir}/man1/flow-gen.1*
%{_mandir}/man1/flow-header.1*
%{_mandir}/man1/flow-import.1*
%{_mandir}/man1/flow-mask.1*
%{_mandir}/man1/flow-merge.1*
%{_mandir}/man1/flow-nfilter.1*
%{_mandir}/man1/flow-print.1*
%{_mandir}/man1/flow-receive.1*
%{_mandir}/man1/flow-report.1*
%{_mandir}/man1/flow-send.1*
%{_mandir}/man1/flow-split.1*
%{_mandir}/man1/flow-stat.1*
%{_mandir}/man1/flow-tag.1*
%{_mandir}/man1/flow-tools.1*
%{_mandir}/man1/flow-tools-examples.1*
%{_mandir}/man1/flow-xlate.1*
%{_mandir}/man1/flow-log2rrd.1*
%{_mandir}/man1/flow-rpt2rrd.1*
%{_mandir}/man1/flow-rptfmt.1*

%files -n flow-capture
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/flow-capture
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/flow-capture.conf
%{_sbindir}/flow-capture
%{_mandir}/man1/flow-capture.1*
%dir /var/lib/flow-capture

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc docs/*.html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
