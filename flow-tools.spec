%define	major 0
%define libname %mklibname ft %{major}
%define develname %mklibname ft -d

Summary:	Tool set for working with NetFlow data
Name:		flow-tools
Version:	0.68.5.1
Release:	6
License:	BSD
Group:		Monitoring
URL:		http://code.google.com/p/flow-tools/
Source0:	http://flow-tools.googlecode.com/files/flow-tools-%{version}.tar.bz2
Source1:	flow-capture.service
Source2:	flow-capture.conf
Patch4:		flow-tools-0.68-format_not_a_string_literal_and_no_format_arguments.diff
Requires:	tcp_wrappers
BuildRequires:	docbook-utils
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	zlib-devel
BuildRequires:	tcp_wrappers-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel

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

%package rrdtool
Summary:    Scripts for flow-tools to build rrd graphs
Group:		Monitoring
Requires:   %{name} = %{version}-%{release}
Requires:   python-rrdtool

%description rrdtool
Flow-tools is library and a collection of programs used to collect,
send, process, and generate reports from NetFlow data. The tools can be
used together on a single server or distributed to multiple servers for
large deployments. The flow-toools library provides an API for development
of custom applications for NetFlow export versions 1,5,6 and the 14 currently
defined version 8 subversions. A Perl and Python interface have been
contributed and are included in the distribution. 

This package contains scripts that use python-rrdtool to create rrds and graphs
from flow data. 

%package docs
Summary:    HTML and other redundant docs for flow-tools
Group:      Monitoring

%description docs
Flow-tools is library and a collection of programs used to collect,
send, process, and generate reports from NetFlow data. The tools can be
used together on a single server or distributed to multiple servers for
large deployments. The flow-toools library provides an API for development
of custom applications for NetFlow export versions 1,5,6 and the 14 currently
defined version 8 subversions. A Perl and Python interface have been
contributed and are included in the distribution.

This package contains additional documentation, such as man pages in html
format.

%prep
%setup -q 
%patch4 -p0

cp %{SOURCE2} flow-capture.conf

%build
%configure2_5x \
    --localstatedir=%{_localstatedir}/%{name} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --bindir=%{_sbindir} \
    --with-mysql \
    --with-postgresql \
    --with-openssl

%install
%makeinstall_std

install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/ft
install -d %{buildroot}/var/lib/flow-capture

install -m0755 %{SOURCE1} %{buildroot}%{_unitdir}/flow-capture.service
install -m0644 flow-capture.conf %{buildroot}%{_sysconfdir}/flow-capture.conf

# python path fix
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-log2rrd
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-rpt2rrd
perl -pi -e "s|/usr/local/bin/python|%{_bindir}/python|g" %{buildroot}%{_sbindir}/flow-rptfmt

%post -n flow-capture
%systemd_post flow-capture.service

%preun -n flow-capture
%systemd_preun flow-capture.service

%postun -n flow-capture
%systemd_postun

%files
%doc ChangeLog README SECURITY TODO
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/cfg
%dir %{_sysconfdir}/%{name}/sym
%config(noreplace) %{_sysconfdir}/%{name}/cfg/*
%config(noreplace) %{_sysconfdir}/%{name}/sym/*
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
%{_mandir}/man1/flow-rptfmt.1*
%{_datadir}/%{name}

%files -n flow-capture
%{_unitdir}/flow-capture*
%config(noreplace) %{_sysconfdir}/flow-capture.conf
%{_sbindir}/flow-capture
%{_mandir}/man1/flow-capture.1*
%dir /var/lib/flow-capture

%files rrdtool
%{_sbindir}/flow-log2rrd
%{_sbindir}/flow-rpt2rrd
%{_mandir}/man1/flow-log2rrd.1*
%{_mandir}/man1/flow-rpt2rrd.1*

%files docs
%doc docs/*.html ChangeLog.old TODO INSTALL SECURITY 

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%doc docs/*.html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


