# Ganeti RPM Packaging

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

## Packaging status

- RHEL/CentOS/Scientific Linux 7.x: 2.16.1-1
- [RHEL/CentOS/Scientific Linux 6.x: 2.11.8-2](https://github.com/jfut/ganeti-rpm/tree/el6)

## Documentation

- [Installation and Upgrade guides](https://github.com/jfut/ganeti-rpm/tree/master/doc)

## YUM repository and binary RPM files

- http://jfut.integ.jp/linux/ganeti/

## Building RPM Packages with Docker

You can build RPM packages in Docker.

```
docker build -t ganeti-rpmbuild-centos7 -f docker/Dockerfile.centos7 .
```

Run the container with bash:

```
BUILD_HOSTNAME=ganeti-rpm-build.integ.jp
docker run -h ${BUILD_HOSTNAME} --rm -it -v $PWD:/pkg ganeti-rpmbuild-centos7 bash
cd /pkg
```

### Build the package

Uninstall, clean, and build all packages, and install:

```
./package.sh -ucia
```

Uninstall and clean all packages, and build ganeti dependencies packages only, and install:

```
./package.sh -ucid
```

Uninstall and clean all packages, and build the specified package(s) only, and install:

```
./package.sh -ucip PACKAGE
```

Build all packages with no overwrite and install:

```
./package.sh -o no -ia
```

### List ghc dependencies in target packages

```
./package.sh -ucid
./package.sh -l
```

## Signing RPM Packages

Sign all packages:

```
./package.sh -sa
```

Sign the specified package(s) only:

```
./package.sh -sp PACAKGE
```

## Other Ganeti resources

- [Ganeti](http://www.ganeti.org/)
- [Ganeti Source Repository (GitHub)](https://github.com/ganeti/ganeti)
- [Ganeti's documentation](http://docs.ganeti.org/ganeti/current/html/)

## Contributing

1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

