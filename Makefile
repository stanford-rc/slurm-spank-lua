VERSION = $(shell git describe --tags --abbrev=0 | sed -r 's/^v//g')
PKGDIR = $(shell pwd)/pkg
package:
	mkdir -p $(PKGDIR)
	git ls-files | tar -c --transform 's,^,slurm-spank-lua-$(VERSION)/,' -T - | gzip > $(PKGDIR)/slurm-spank-lua-$(VERSION).tar.gz
