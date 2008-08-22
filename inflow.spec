%include	/usr/lib/rpm/macros.perl
Summary:	inflow - flow stats for INN
Name:		inflow
Version:	2.4.0
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	ftp://ftp.uni-kassel.de/pub/net/news/unix/inflow/%{name}-%{version}.tar.gz
# Source0-md5:	8eeb022187585aeb34f759c4d1203f92
Patch0:		%{name}-config_location.patch
Patch1:		%{name}-conf.patch
Patch2:		%{name}-png.patch
BuildRequires:	rpm-perlprov
BuildRequires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_pkgdir		%{_var}/lib/%{name}

%description
The inflow package is a set of currently four scripts written to find
out where you get your News from, both in number of articles and in
terms of MBytes, how much the articles are delayed, and how long your 
queues are. In addition, some statistics about News hierarchies
are available, with special emphasis given to the alt.* groups.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__sed} -i -e 's@#! /bin/perl@#!/usr/bin/perl@' *
%{__sed} -i -e 's@#! /usr/local/bin/perl@#!/usr/bin/perl@' *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{perl_privlib},%{_pkgdir},/etc/cron.d}

install inflow-collect inflow-plot inflow-stat outflow-stat $RPM_BUILD_ROOT%{_bindir}
install inflow.conf olm-lookup $RPM_BUILD_ROOT%{_sysconfdir}
install inflow.pm $RPM_BUILD_ROOT%{perl_privlib}

cat > $RPM_BUILD_ROOT/etc/cron.d/%{name} << EOF
0 * * * *	news	%{_bindir}/inflow-collect -cs
0 * * * *	news	%{_bindir}/outflow-stat -wF
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc inflow.CHANGES inflow.HELP inflow.README
%attr(750,root,news) %dir %{_sysconfdir}
%attr(640,root,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(640,root,news) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%attr(755,root,root) %{_bindir}/*
%{perl_privlib}/%{name}.pm
%attr(750,root,news) %dir %{_pkgdir}
