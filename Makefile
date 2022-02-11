VERSION = $(shell git describe --tags --abbrev=0 | sed -r 's/^v//g')
PKGDIR = $(shell pwd)/pkg
package:
	mkdir -p $(PKGDIR)
	git ls-files | tar -c --transform 's,^,slurm-spank-lua-$(VERSION)/,' -T - | gzip > $(PKGDIR)/slurm-spank-lua-$(VERSION).tar.gz

CFLAGS = -fPIC -g
clean:
	rm -f lua.o run_scripts.o lib/list.o lua.so run_scripts
lua.so: lua.o lib/list.o
	cc -shared -fPIC -o $@ $^ -llua
run_scripts: run_scripts.o lua.o lib/list.o
	cc $^ -o $@ -llua -ldl
