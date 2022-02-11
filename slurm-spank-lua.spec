%global slurm_version  %(rpm -q slurm-devel --qf "%{VERSION}" 2>/dev/null)
%define _use_internal_dependency_generator 0
%define __find_requires %{_builddir}/find-requires

Summary: Slurm Lua SPANK plugin
Name: slurm-spank-lua
Version: 0.44
Release: %{slurm_version}.1%{?dist}
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
# Dummy file used to get a RPM dependency on libslurm.so
echo 'int main(){}' > %{_builddir}/libslurm_dummy.c
cat <<EOF > %{_builddir}/find-requires
#!/bin/sh
# Add dummy to list of files sent to the regular find-requires
{ echo %{_builddir}/libslurm_dummy; cat; } | \
    %{_rpmconfigdir}/find-requires
EOF
chmod +x %{_builddir}/find-requires

%build
%{__cc} -g -o lua.o -fPIC -c lua.c
%{__cc} -g -o lib/list.o -fPIC -c lib/list.c
%{__cc} -g -shared -fPIC -o lua.so lua.o lib/list.o -llua
# Dummy file to get a dependency on libslurm
%{__cc} -lslurm -o %{_builddir}/libslurm_dummy %{_builddir}/libslurm_dummy.c


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/slurm
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/slurm/plugstack.conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/slurm/lua.d/disabled
install -m 755 lua.so $RPM_BUILD_ROOT%{_libdir}/slurm
install -m 644 scripts/spank_demo.lua \
    $RPM_BUILD_ROOT%{_sysconfdir}/slurm/lua.d/disabled
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
%{_sysconfdir}/slurm/lua.d/disabled/spank_demo.lua
%{_mandir}/man8/spank-lua*


%changelog
* Tue May 11 2021 Trey Dockendorf <tdockendorf@osc.edu> - 0.43-1
- Add support for Lua 5.3
* Tue Mar 02 2021 Trey Dockendorf <tdockendorf@osc.edu> - 0.42-1
- Force a dependency on versioned libslurm.so
* Tue Aug 11 2020 Trey Dockendorf <tdockendorf@osc.edu> - 0.41-1
- Keep dist in RPM release
* Tue Aug 11 2020 Trey Dockendorf <tdockendorf@osc.edu> - 0.40-1
- Add Slurm version in RPM release
- Add "package" target in Makefile
* Thu Nov 29 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.39-1
- Added missing SPEC %files entry for spank_demo.lua
* Mon Jan 22 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.38-2
- Provides spank_demo.lua script
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.38-1
- Fix segfault if no Lua scripts are present
- Include the slurm/lua.d directory
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.37-2
- Requires lua-devel, as the liblua.so symlink, which is required by the
  plugin, is only provided in the -devel package.
* Tue Jan 16 2018 Kilian Cavalotti <kilian@stanford.edu> - 0.37-1
- Initial build, extracted and repackaged from LLNL's slurm-spank-plugins.
