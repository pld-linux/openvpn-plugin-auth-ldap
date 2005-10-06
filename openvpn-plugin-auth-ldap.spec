# TODO
# [13:32:47] <@pluto_> glen: what for you use a strlcpy? use libsafe.spec and `gcc -Dstrlcpy=strcpy ...` :)
Summary:	OpenVPN Auth-LDAP Plugin
Summary(pl):	Wtyczka Auth-LDAP dla OpenVPN
Name:		openvpn-plugin-auth-ldap
Version:	1.0.1
Release:	0.3
License:	BSD
Group:		Applications
Source0:	http://www.opendarwin.org/~landonf/software/openvpn-auth-ldap/auth-ldap-1.0.1.tar.gz
# Source0-md5:	3f94242db7d9b65d62657e97b799339a
Patch0:		%{name}-make.patch
URL:		http://www.opendarwin.org/~landonf/software/openvpn-auth-ldap/
BuildRequires:	gcc-objc
BuildRequires:	libstrlcpy-devel
BuildRequires:	openldap-devel
BuildRequires:	openvpn-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/openvpn/plugins
%define		_sysconfdir	/etc/openvpn

%description
The openvpn-auth-ldap plugin implements username/password
authentication via LDAP.

%description -l pl
Wtyczka openvpn-auth-ldap implementuje uwierzytelnianie nazw±
u¿ytkownika i has³em poprzez LDAP.

%prep
%setup -q -n auth-ldap-%{version}
%patch0 -p1

%build
%{__make} \
	OPTFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_plugindir}}
install openvpn-auth-ldap.so $RPM_BUILD_ROOT%{_plugindir}
install auth-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README test.c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_plugindir}/*
