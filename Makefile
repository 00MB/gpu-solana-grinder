OS := $(shell uname)

all:
ifeq ($(OS),Darwin)
SO=dylib
else
SO=so
all: cuda_crypt cuda_vanity
endif

V=release

.PHONY:cuda_crypt cuda_vanity
cuda_crypt cuda_vanity:
	$(MAKE) V=$(V) -C src

DESTDIR ?= dist
install:
	mkdir -p $(DESTDIR)
ifneq ($(OS),Darwin)
	cp -f src/$(V)/libcuda-crypt.so $(DESTDIR)
	cp -f src/$(V)/cuda_ed25519_vanity $(DESTDIR)
endif
	ls -lh $(DESTDIR)

.PHONY:clean
clean:
	$(MAKE) V=$(V) -C src clean