#!/bin/bash -ue
#
# Build RPMs for Ganeti & Tools

# Packages to be built
PACKAGES="ganeti ganeti-instance-debootstrap python-affinity"

# Directories
PACKAGER="$(basename "${0}")"
PACKAGER_DIR="$(cd $(dirname ${0}) && echo ${PWD})"
PACKAGER_RPM_DIR="${PACKAGER_DIR}/rpmbuild"

# Includes
#. ${PACKAGER_DIR}/package-config
#. ${PACKAGER_DIR}/package-prebuild

# Build packages
build_package() {
    for PACKAGE in ${@}; do
        echo "Building package for ${PACKAGE}..."
        pushd "${PACKAGER_RPM_DIR}/${PACKAGE}"
        rpmbuild --define "%_topdir "${PACKAGER_RPM_DIR}"/"${PACKAGE}"" -ba SPECS/${PACKAGE}.spec
        popd
    done
}

# Main
main() {
    build_package ${PACKAGES}
}

[ ${#BASH_SOURCE[@]} = 1 ] && main "$@"
