Summary:	OpenVPN Auth-LDAP Plugin
Summary(pl):	Wtyczka Auth-LDAP dla OpenVPN
Name:		openvpn-plugin-auth-ldap
Version:	1.0.3
Release:	0.1
License:	BSD
Group:		Applications
Source0:	http://www.opendarwin.org/~landonf/software/openvpn-auth-ldap/auth-ldap-%{version}.tar.gz
# Source0-md5:	955f8f06962acb08e4da62f77fc41131
Patch0:		%{name}-make.patch
URL:		http://www.opendarwin.org/~landonf/software/openvpn-auth-ldap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-objc
BuildRequires:	openldap-devel
BuildRequires:	openvpn-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/openvpn/plugins
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
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-openldap=%{_prefix} \
	--with-openvpn=%{_prefix}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install auth-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_libdir}/*
