# Ganeti RPM Packaging

Ganeti RPM Packaging for RHEL/CentOS/Scientific Linux and Fedora.

## Packaging status

- RHEL/CentOS/Scientific Linux 7.x: 2.16.2-1
- [RHEL/CentOS/Scientific Linux 6.x: 2.11.8-2](https://github.com/jfut/ganeti-rpm/tree/el6)

## Documentation

- [Installation and Upgrade guides](https://github.com/jfut/ganeti-rpm/tree/master/doc)

## YUM repository and binary RPM files

- http://jfut.integ.jp/linux/ganeti/

## Building RPM Packages with Docker

You can build RPM packages in Docker.

- CentOS 8

```bash
docker build -t ganeti-rpmbuild-centos8 -f docker/Dockerfile.centos8 .

# pull the latest base image + no cache
docker build -t ganeti-rpmbuild-centos8 -f docker/Dockerfile.centos8 . --pull=true --no-cache
```

- CentOS 7

```bash
docker build -t ganeti-rpmbuild-centos7 -f docker/Dockerfile.centos7 .

# pull the latest base image + no cache
docker build -t ganeti-rpmbuild-centos7 -f docker/Dockerfile.centos7 . --pull=true --no-cache
```

Run the container with bash:

- CentOS 8

```bash
BUILD_HOSTNAME=ganeti-rpmbuild-centos8.integ.jp
docker run -h ${BUILD_HOSTNAME} --rm -it -v $PWD:/pkg ganeti-rpmbuild-centos8 bash
```

- CentOS 7

```bash
BUILD_HOSTNAME=ganeti-rpmbuild-centos7.integ.jp
docker run -h ${BUILD_HOSTNAME} --rm -it -v $PWD:/pkg ganeti-rpmbuild-centos7 bash
```

### Run build command in the container

Uninstall, clean, and build all packages, and install:

```
./build-rpm -ucia
```

Uninstall and clean all packages, and build ganeti dependencies packages only, and install:

```
./build-rpm -ucid
```

Uninstall and clean all packages, and build the specified package(s) only, and install:

```
./build-rpm -ucip PACKAGE
```

Build all packages with no overwrite and install:

```
./build-rpm -o no -ia
```

Build the new ganeti RPM package version using the already released dependency libraries and install:

```
yum install http://jfut.integ.jp/linux/ganeti/7/x86_64/integ-ganeti-release-7-2.el7.noarch.rpm
yum-config-manager --enable integ-ganeti
./build-rpm -ip ganeti
```

### List ghc dependencies in target packages

```
./build-rpm -ucid
./build-rpm -l
```

## Signing RPM Packages

Run the container with bash:

```
BUILD_HOSTNAME=ganeti-rpm-build.integ.jp
docker run -h ${BUILD_HOSTNAME} --rm -it -v $PWD:/pkg -v ~/.gnupg:/root/.gnupg ganeti-rpmbuild-centos7 bash
cd /pkg

# Set your gpg name
echo "%_gpg_name jfut-rpm@integ.jp" >> ~/.rpmmacros
```

Sign all packages:

```
./build-rpm -sa
```

Sign the specified package(s) only:

```
./build-rpm -sp PACAKGE
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

