.PHONY: default
default: lua.so ;

VERSION = $(shell git describe --tags --abbrev=0 | sed -r 's/^v//g')
PKGDIR = $(shell pwd)/pkg
package:
	mkdir -p $(PKGDIR)
	git ls-files | tar -c --transform 's,^,slurm-spank-lua-$(VERSION)/,' -T - | gzip > $(PKGDIR)/slurm-spank-lua-$(VERSION).tar.gz

PKG_CONFIG ?= pkg-config
LUA_PKG ?= lua
CPPFLAGS += $(shell $(PKG_CONFIG) --cflags $(LUA_PKG))
CFLAGS += -fPIC -g
LDLIBS += $(shell $(PKG_CONFIG) --libs $(LUA_PKG)) -ldl
clean:
	rm -f lua.o lib/list.o lua.so
lua.so: lua.o lib/list.o
	$(CC) $(LDFLAGS) -shared -fPIC -o $@ $^ $(LDLIBS)
