# Slurm SPANK Lua plugin

The Lua SPANK plugin for Slurm allows Lua scripts to take the place of compiled C shared objects in the Slurm `spank(8)` framework. All the power of the C SPANK API is exported to Lua via this plugin, which loads one or scripts and executes Lua functions during the appropriate Slurm phase (as described in the `spank(8)` manpage).

This is extracted from [LLNL's Slurml SPANK plugins](https://github.com/grondo/slurm-spank-plugins) and re-packaged to only provide the LUA SPANK plugin.


## Installation

Get the source and build the RPM:

```
$ VER=0.37
$ wget https://github.com/kcgthb/slurm-spank-lua/archive/v${VER}.tar.gz -O slurm-spank-lua-${VER}.tar.gz
$ rpmbuild -ta slurm-spank-lua-${VER}.tar.gz
```

Then install the generated RPM.


## Usage 

See the man page (`man 8 spank-lua`) for details.
