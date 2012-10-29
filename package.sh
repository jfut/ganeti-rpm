#!/bin/bash -ue
#
# Build RPMs for Ganeti & Tools

# Packages to be built
PACKAGES="ghc-curl ganeti ganeti-instance-debootstrap python-affinity"

# Directories
PACKAGER="$(basename "${0}")"
PACKAGER_DIR="$(cd $(dirname ${0}) && echo ${PWD})"
PACKAGER_RPM_DIR="${PACKAGER_DIR}/rpmbuild"

# Includes
#. ${PACKAGER_DIR}/package-config
#. ${PACKAGER_DIR}/package-prebuild

RPM_DIST=$(cat /etc/rpm/macros.dist | egrep "^%dist" | awk '{ print $2 }')

# Check old package
check_oldpackage() {
    PACKAGE="${1}"
    local is_first=0
    is_overwrite="-1"

    SPEC_FILE="SPECS/${PACKAGE}.spec"
    RPM_VERSION=$(egrep -i "^Version:" ${SPEC_FILE} | awk '{ print $2 }')
    RPM_RELEASE=$(egrep -i "^Release:" ${SPEC_FILE} | awk '{ print $2 }' | cut -d'%' -f 1)
    RPM_ARCHITECTURE=$(egrep -i "^BuildArchitectures:" ${SPEC_FILE} | awk '{ print $2 }')

    if [ -z ${RPM_ARCHITECTURE} ]; then
        RPM_ARCHITECTURE=$(uname -i)
    fi

    RPM_FILE="RPMS/${RPM_ARCHITECTURE}/${PACKAGE}-${RPM_VERSION}-${RPM_RELEASE}${RPM_DIST}.${RPM_ARCHITECTURE}.rpm"
    if [ -f ${RPM_FILE} ]; then
        while [ ${is_overwrite} != "y" -a ${is_overwrite} != "n" ];
        do
            if [ ${is_first} -ne 0 ]; then
                echo "-> BAD INPUT: Invalid charactor."
            fi
            echo "${RPM_FILE} already exists."
            echo -n "Do you want to overwrite it? [y/n]: "
            read is_overwrite < /dev/tty
            is_first=1
        done
    else
        is_overwrite="y"
    fi
}

# Build packages
build_package() {
    for PACKAGE in ${@}; do
        echo "Building package for ${PACKAGE}..."
        pushd "${PACKAGER_RPM_DIR}/${PACKAGE}"
        check_oldpackage ${PACKAGE}
        if [ ${is_overwrite} = "y" ]; then
            rpmbuild --define "%_topdir "${PACKAGER_RPM_DIR}"/"${PACKAGE}"" -ba SPECS/${PACKAGE}.spec
        fi
        echo
        popd
    done
}

# Main
main() {
    build_package ${PACKAGES}
}

[ ${#BASH_SOURCE[@]} = 1 ] && main "$@"
