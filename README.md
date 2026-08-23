# INDIGO Astronomy - unofficial Fedora RPMs

https://www.indigo-astronomy.org/

## Free & non-free components

SPEC file in this reposioty covers both free base version and non-free
additional drivers (mostly cameras). Non-free drivers contain proprietary
vendor SDK libraries in a form of pre-compiled `*.a` and `*.so` files.

I build both for myself. "Free" variant together with Ain INDIGO Imager
suite and INDIGO Control Panel is available in my Copr:
https://copr.fedorainfracloud.org/coprs/ivanmironov/base-patched/

If you need non-free drivers: build yourself using following instructions.

## How to build

Non-free:

```bash
# 1. Download `indigo-X.Y-Z.tar.gz` from https://github.com/indigo-astronomy/indigo/tags

# 2. Build *.src.rpm
mock --buildsrpm --sources . --spec indigo.spec --define "_non_free 1"
cp /var/lib/mock/*/result/indigo-*.src.rpm ./

# 3. Build *.rpm
mock --rebuild ./indigo-*.src.rpm --define "_non_free 1"

# 4. Find built *.rpm
ls -lah /var/lib/mock/*/result/*.rpm
```

Free:

```bash
# 1. Download `indigo-X.Y-Z.tar.gz` from https://github.com/indigo-astronomy/indigo/tags

# 2. Remove non-free components
./deblob.sh indigo-X.Y-Z.tar.gz indigo-free-X.Y-Z.tar.xz

# 3. Build *.src.rpm
mock --buildsrpm --sources . --spec indigo.spec
cp /var/lib/mock/*/result/indigo-*.src.rpm ./

# 4. Build *.rpm
mock --rebuild ./indigo-*.src.rpm

# 5. Find built *.rpm
ls -lah /var/lib/mock/*/result/*.rpm
```

## How to install

```bash
# Non-free
sudo dnf install /var/lib/mock/*/result/indigo-free-[0-9]*.rpm /var/lib/mock/*/result/indigo-drivers-list-nonfree-[0-9]*.rpm /var/lib/mock/*/result/indigo-drivers-nonfree-[0-9]*.rpm /var/lib/mock/*/result/indigo-client-libs-free-[0-9]*.rpm

# Free
sudo dnf install /var/lib/mock/*/result/indigo-free-[0-9]*.rpm /var/lib/mock/*/result/indigo-drivers-list-free-[0-9]*.rpm /var/lib/mock/*/result/indigo-client-libs-free-[0-9]*.rpm
```
