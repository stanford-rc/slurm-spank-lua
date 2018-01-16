Summary: Slurm Lua SPANK plugin
Name: slurm-spank-lua
Version: 0.38
Release: 1
License: GPL
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}

BuildRequires: slurm-devel bison flex
BuildRequires: lua-devel >= 5.1
Requires:      slurm lua-devel >= 5.1

%description
The lua.so spank plugin for Slurm allows lua scripts to take the place of
compiled C shared objects in the Slurm spank(8) framework. All the power of the
C SPANK API is exported to lua via this plugin, which loads one or scripts and
executes lua functions during the appropriate Slurm phase (as described in the
spank(8) manpage).


%prep
%setup -q

%build
%{__cc} -g -o lua.o -fPIC -c lua.c
%{__cc} -g -o lib/list.o -fPIC -c lib/list.c
%{__cc} -g -shared -fPIC -o lua.so lua.o lib/list.o -llua


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/slurm
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/slurm/plugstack.conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/slurm/lua.d
install -m 755 lua.so $RPM_BUILD_ROOT%{_libdir}/slurm
echo "required  lua.so  /etc/slurm/lua.d/*.lua" > \
     $RPM_BUILD_ROOT/%{_sysconfdir}/slurm/plugstack.conf.d/lua.conf
install -D -m0644 spank-lua.8 $RPM_BUILD_ROOT/%{_mandir}/man8/spank-lua.8


%clean
rm -rf "$RPM_BUILD_ROOT"


%files
%defattr(-,root,root,-)
%dir %attr(0755,root,root) %{_sysconfdir}/slurm/lua.d
%{_libdir}/slurm/lua.so
%{_sysconfdir}/slurm/plugstack.conf.d/lua.conf
%{_mandir}/man8/spank-lua*


%changelog
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.38-1
- Fix segfault if no Lua scripts are present
- Include the slurm/lua.d directory
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.37-2
- Requires lua-devel, as the liblua.so symlink, which is required by the
  plugin, is only provided in the -devel package.
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.37-1
- Initial build, extracted and repackaged from LLNL's slurm-spank-plugins.

