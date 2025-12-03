# Conditional build:
%bcond_with	tests		# check-based tests

Summary:	OpenVPN Auth-LDAP Plugin
Summary(pl.UTF-8):	Wtyczka Auth-LDAP dla OpenVPN
Name:		openvpn-plugin-auth-ldap
Version:	2.0.4
Release:	3
License:	BSD + others
Group:		Applications
Source0:	https://github.com/threerings/openvpn-auth-ldap/archive/auth-ldap-%{version}.tar.gz
# Source0-md5:	c4985fbbf88042e28efd1521d03bf658
Patch0:		debian.patch
URL:		https://github.com/threerings/openvpn-auth-ldap
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_tests:BuildRequires:	check}
BuildRequires:	gcc-objc
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
%setup -q -n openvpn-auth-ldap-auth-ldap-%{version}
%patch -P0 -p1

#:> objc.m4

%build
#%%{__aclocal}
%{__autoconf}
%{__autoheader}
cp -f /usr/share/automake/config.sub .
%configure \
	OBJCFLAGS="-std=gnu11" \
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
%doc LICENSE README.md
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{_sysconfdir}/auth-ldap.conf
%attr(755,root,root) %{_libdir}/openvpn-auth-ldap.so
