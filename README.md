# Ganeti RPM Packaging

[![Build Test](https://github.com/jfut/ganeti-rpm/workflows/Build%20Test/badge.svg?branch=master)](https://github.com/jfut/ganeti-rpm/actions?query=workflow%3A%22Build+Test%22)

Ganeti RPM Packaging for RHEL/AlmaLinux/CentOS/Rocky Linux/others.

## Packaging status

- RHEL/AlmaLinux/CentOS/Rocky Linux/others 9.x: 3.0.2-2
- RHEL/AlmaLinux/CentOS/Rocky Linux/others 8.x: 3.0.2-2
- RHEL/CentOS/others 7.x: 3.0.2-2

## Documentation

- [Installation tutorial](https://github.com/jfut/ganeti-rpm/blob/master/doc/install-rhel.md)
- [Upgrade / update guides (update-rhel-*)](https://github.com/jfut/ganeti-rpm/tree/master/doc)

## YUM/DNF repository and binary RPM files

- https://jfut.integ.jp/linux/ganeti/
- https://ftp.osuosl.org/pub/ganeti-rpm/ (mirror, thanks to the OSU Open Source Lab)

## Building RPM Packages with Docker

You can build RPM packages in Docker.

```bash
# AlmaLinux 9
./build almalinux:9
# or ./build rockylinux:9

# AlmaLinux 8
./build almalinux:8
# or ./build rockylinux:8

# CentOS 7
./build centos:7
```

Debug and manual mode:

```bash
# AlmaLinux 9
./build -d almalinux:9
# or ./build -d rockylinux:9

# AlmaLinux 8
./build -d almalinux:8
# or ./build -d rockylinux:8

# CentOS 7
./build -d centos:7

# Setup
cd /pkg
./setup

# Build
./build-rpm ...
```

## Usage: build

Run on host.

```bash
Usage:
    build [-d] BUILD_IMAGE_NAME:BUILD_IMAGE_TAG [BUILD_RPM_OPTIONS]

    Options:
        -d Debug mode

        BUILD_RPM_OPTIONS
            build-rpm options (default: -a -bi -o yes)

    Environment variables:
        BUILD_HOSTNAME: container host name

    Build for AlmaLinux 9:
        build almalinux:9

    Build for AlmaLinux 8:
        build almalinux:8

    Build for CentOS 7:
        build centos:7
```

## Usage: build-rpm

Run in a container.

```bash
Usage:
    build-rpm [-a|-d|-p] [-c|-C] [-b] [-s] [-i] [-u] [-o yes|no] [package...]

    Target Options:
        -a all packages (ganeti and its dependencies and integ-ganeti repo, snf-image)
        -d ganeti dependencies packages only
        -p the specified package(s) only. Available packages are:
            ganeti dependencies (el8 only):
                python-bitarray
            ganeti:
                ganeti ganeti-instance-debootstrap
            snf-image:
                python-prctl snf-image
            integ-ganeti-repo:
                integ-ganeti-release

    Task Options:
        -c Clean clean the rpmbuild directory, but preserve downloaded archives
        -C Completely clean the rpmbuild directory

        -b Build packages
        -o Overwrite built package: yes|no (Default: manual)

        -s Sign built packages

        -i Install built packages
        -u Uninstall installed packages

        Task Execution Order:
            Uninstall -> Clean -> Build -> Sign -> Install

        If the build (-b) and install (-i) options are specified at the same time,
        the installation will be done immediately after the individual packages are built.
        This is to resolve dependencies needed to build the next package.
```

### Run build command in the container

All packages + uninstall, clean, build, and install:

```bash
./build-rpm -a -ucbi
```

Ganeti dependencies packages + uninstall, clean, build, and install:

```bash
./build-rpm -d -ucbi
```

The specified package(s) + uninstall, clean, build, and install:

```bash
./build-rpm -p -ucbi PACKAGE
```

Build all packages with no overwrite and install:

```bash
./build-rpm -a -bi -o no
```

Build the new ganeti RPM package version using the already released dependency libraries and install:

```bash
# AlmaLinux 9 or Rocky Linux 9
dnf install https://jfut.integ.jp/linux/ganeti/9/x86_64/integ-ganeti-release-9-1.el9.noarch.rpm
dnf config-manager --enable integ-ganeti
./build-rpm -p -bi ganeti

# AlmaLinux 8 or Rocky Linux 8
dnf install https://jfut.integ.jp/linux/ganeti/8/x86_64/integ-ganeti-release-8-1.el8.noarch.rpm
dnf config-manager --enable integ-ganeti
./build-rpm -p -bi ganeti

# CentOS 7
yum install https://jfut.integ.jp/linux/ganeti/7/x86_64/integ-ganeti-release-7-3.el7.noarch.rpm
yum-config-manager --enable integ-ganeti
./build-rpm -p -bi ganeti
```

## Signing RPM Packages

Run the container with bash:

```bash
# AlmaLinux 9
BUILD_HOSTNAME=almalinux-9.github.integ.jp
docker run -h "${BUILD_HOSTNAME}" --rm -it -v $PWD:/pkg -v ~/.gnupg.el9:/root/.gnupg almalinux:9 bash

# AlmaLinux 8
BUILD_HOSTNAME=almalinux-8.github.integ.jp
docker run -h "${BUILD_HOSTNAME}" --rm -it -v $PWD:/pkg -v ~/.gnupg.el8:/root/.gnupg almalinux:8 bash

# CentOS 7
BUILD_HOSTNAME=centos-7.github.integ.jp
docker run -h "${BUILD_HOSTNAME}" --rm -it -v $PWD:/pkg -v ~/.gnupg.el7:/root/.gnupg centos:7 bash

# Setup
yum -y install findutils rpm-sign pinentry

# Set your gpg name
echo "%_gpg_name jfut-rpm@integ.jp" >> ~/.rpmmacros
```

Sign all packages:

```bash
cd /pkg
./build-rpm -a -s
```

Sign the specified package(s) only:

```bash
./build-rpm -p -s PACAKGE
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

## Release tag

e.g.:

```bash
git tag -a v3.0.2-2 -m "v3.0.2-2"
git push origin refs/tags/v3.0.2-2
```
