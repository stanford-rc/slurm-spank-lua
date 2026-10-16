> [!NOTE]
> The Lua SPANK plugin for Slurm has been originally developed by [Mark
Grondo](https://github.com/grondo) at [Lawrence Livermore National
Laboratory](https://www.llnl.gov/). This is extracted from the [LLNL Slurm
SPANK plugins](https://github.com/grondo/slurm-spank-plugins) project and
re-packaged to only provide the LUA SPANK plugin, for easier installation.


# Slurm SPANK Lua plugin

The [Lua](https://www.lua.org/) [SPANK](https://slurm.schedmd.com/spank.html)
plugin for [Slurm](https://slurm.schedmd.com/) allows Lua scripts to take the
place of compiled C shared objects in the Slurm `spank(8)` framework. All the
power of the C SPANK API is exported to Lua via this plugin, which loads one or
more scripts and executes Lua functions during the appropriate Slurm phase (as
described in the `spank(8)` manpage).




## Installation

### Assumptions

To facilitate co-existence with other SPANK plugins, we'll assume that the file
defined in `PlugStackConfig` (by default, `/etc/slurm/plugstack.conf`) contains
something like:
```
include /etc/slurm/plugstack.conf.d/*.conf
```
so we can enable the Slurm SPANK Lua plugin by adding a `lua.conf` file in
`/etc/slurm/plugstack.conf.d/`

### RPM-based installation

Get the source and build the RPM:

```
$ REPO=stanford-rc
$ PROJ=slurm-spank-lua
$ VER=$(curl -s https://api.github.com/repos/$REPO/$PROJ/releases/latest | awk '/tag_name/ {gsub(/"|,/,""); print $2}')
$ wget https://github.com/$REPO/$PROJ/archive/${VER}.tar.gz -O slurm-spank-lua-${VER//v}.tar.gz
$ rpmbuild -ta slurm-spank-lua-${VER//v}.tar.gz
```

Install the generated RPM. For instance (paths, arch and version may vary):

```
# rpm -Uvh ~/rpmbuild/RPMS/x86_64/slurm-spank-lua-0.38-1.x86_64.rpm
```

### Debian package

The Debian packaging targets Debian 13 with Lua 5.4 and SchedMD's
`slurm-smd` packages. Install `slurm-smd-dev` matching the Slurm version on
your cluster, plus the build tools:

```sh
# apt install build-essential debhelper devscripts pkg-config liblua5.4-dev
```

From the source directory, run as an unprivileged user:

```sh
$ ./build_deb.sh
```

Packages, build metadata, and the build log are written to `pkg/<version>/`.
Set `OUT_DIR` to use a different output directory. Failed builds remain in
the printed temporary directory, with details in `build.log`.

The package version includes the Slurm series used for the build as a
suffix, for example `+slurm25.11`. Its dependencies require at least the
installed Slurm package version and exclude the next Slurm series. Rebuild the plugin
when upgrading to a new Slurm series. For changed builds within a series,
increment the Debian revision in `debian/changelog`.

Install the generated package on submission and compute hosts:

```sh
$ SLURM_VER=$(dpkg-query -W -f='${Version}' slurm-smd-dev)
$ VER="$(dpkg-parsechangelog -S Version)+slurm${SLURM_VER%.*}"
$ ARCH=$(dpkg-architecture -qDEB_HOST_ARCH)
$ sudo apt install "./pkg/$VER/slurm-spank-lua_${VER}_${ARCH}.deb"
```

Run these commands from the source directory on the build host. Adjust `pkg/` if 
you set `OUT_DIR`. The package installs:
* the plugin in `/usr/lib/<multiarch>/slurm/`, 
* its configuration in `/etc/slurm/plugstack.conf.d/lua.conf`, 
* and the demo script under `/etc/slurm/lua.d/disabled/`. 
Enable the configuration include described above.

### Manual installation

The source can be compiled with:
```
$ cc -o lua.o -fPIC -c lua.c
$ cc -o lib/list.o -fPIC -c lib/list.c
$ cc -shared -fPIC -o lua.so lua.o lib/list.o -llua
```

or just:
```
$ make
```

The Makefile uses `pkg-config` to locate Lua. For a versioned pkg-config
name, use `make LUA_PKG=lua5.4` (and install the corresponding development
package).

Then, the generated `lua.so` should be placed in `/usr/lib/slurm`, and
`lua.conf` in `/etc/slurm/plugstack.conf.d/`.


## Configuration

The packages install a `lua.conf` file in `/etc/slurm/plugstack.conf.d/` that
contains:
```
required  lua.so  /etc/slurm/lua.d/*.lua
```
Then, Lua scripts could simply be dropped in `/etc/slurm/lua.d/` to be
automatically executed by Slurm.




The packages provide a demo script, `spank_demo.lua`, based on the [C SPANK demo
plugin](https://github.com/yqin/slurm-plugins/blob/master/spank_demo.c) by
[Yong Qin](https://github.com/yqin). Its goal is simply to demonstrate all the
different SPANK functions and the context in which they're called. The plugin
does nothing else than logging function calls.

The demo script is installed `/etc/slurm/lua.d/disabled/`, so it won't be
automatically executed.  To enable it, one could simply move it to
`/etc/slurm/lua.d/`


> Note that both the Slurm SPANK Lua plugin (`lua.so`) and the Lua scripts will
need to be present on both the submission host (the node where `srun`/`sbatch`
commands are executed) and the execution host(s) (the compute nodes).


## Writing your own Lua scripts

For more info about how the Slurm SPANK Lua plugin works, and how to write your
own Lua scripts, see the man page (`man 8 spank-lua`).

Other useful information sources:

* Slurm SPANK documentation: https://slurm.schedmd.com/spank.html
* SPANK functions and variables are defined in
  [spank.h](https://github.com/SchedMD/slurm/blob/master/slurm/spank.h)
