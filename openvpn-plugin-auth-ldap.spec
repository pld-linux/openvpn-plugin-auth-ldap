# TODO
# - compiled with gcc 4.7 (libobjc.so.4) it crashes
#   Jan 23 13:47:12 pontus openvpn[32621]: OpenVPN 2.2.1 x86_64-pld-linux [SSL] [LZO2] [EPOLL] [PKCS11] [eurephia] built on Jul 7 2011
#   Jan 23 13:47:12 pontus kernel: [38178686.496394] openvpn[32621]: segfault at 0 ip 00007ff3b02c4243 sp 00007fffe923bd20 error 4 in libobjc.so.4.0.0[7ff3b02b6000+16000]
#   Jan 23 13:47:12 pontus openvpn[32621]: NOTE: the current --script-security setting may allow this configuration to call user-defined scripts
#   Jan 23 13:47:12 pontus openvpn: /usr/sbin/openvpn startup failed
#   similarily to http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=641811
#   if built with gcc 4.6 (libobjc.so.3) it does not crash!
#
# Conditional build:
%bcond_with	tests		# check-based tests

Summary:	OpenVPN Auth-LDAP Plugin
Summary(pl.UTF-8):	Wtyczka Auth-LDAP dla OpenVPN
Name:		openvpn-plugin-auth-ldap
Version:	2.0.3
Release:	9
License:	BSD
Group:		Applications
Source0:	http://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
# Source0-md5:	03dedc57efc8d4fc2ffe2c014121299d
Patch0:		%{name}-make.patch
Patch1:		%{name}-objc-include.patch
URL:		http://code.google.com/p/openvpn-auth-ldap/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_tests:BuildRequires:	check}
BuildRequires:	gcc-objc < 6:4.7
BuildRequires:	openldap-devel
BuildRequires:	openvpn-devel
BuildRequires:	re2c
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/openvpn/plugins
%define		_sysconfdir	/etc/openvpn

%description
The openvpn-auth-ldap plugin implements username/password
authentication via LDAP.

%description -l pl.UTF-8
Wtyczka openvpn-auth-ldap implementuje uwierzytelnianie nazwą
użytkownika i hasłem poprzez LDAP.

%prep
%setup -q -n auth-ldap-%{version}
%patch0 -p1
%patch1 -p1

> objc.m4

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
cp -f /usr/share/automake/config.sub .
%configure \
	--with-objc-runtime=GNU \
	--with-check=%{!?with_tests:/proc}%{?with_tests:/usr} \
	--with-openldap=/usr \
	--with-openvpn=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cp -a auth-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/auth-ldap.conf
%attr(755,root,root) %{_libdir}/openvpn-auth-ldap.so
