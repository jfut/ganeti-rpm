#!/bin/bash -ue
#
# Build RPMs for Ganeti and Tools

# single packages
GANETI_DEPENDS_PACKAGES1="ghc-Crypto ghc-curl ghc-regex-pcre"
# in order of dependencies
# (base-orphans | tagged -> (contravariant | distributive) -> comonad)) -> semigroupoids
GANETI_DEPENDS_PACKAGES2="ghc-base-orphans ghc-tagged ghc-contravariant ghc-distributive ghc-comonad ghc-semigroupoids"
# (bifunctors | profunctors | generic-derivin | reflectiong) -> lens
GANETI_DEPENDS_PACKAGES3="ghc-bifunctors ghc-profunctors ghc-generic-deriving ghc-reflection ghc-lens"
# mond/metad dependencies
# ghc-PSQueue | ghc-clock | ghc-bytestring-builder -> ghc-zlib-bindings -> ghc-io-streams
# ghc-enumerator -> (ghc-attoparsec-enumerator ghc-blaze-builder-enumerator
# ghc-bytestring-mmap ghc-zlib-enum) -> ghc-snap-core -> ghc-snap-server
GANETI_DEPENDS_PACKAGES4="ghc-PSQueue ghc-clock ghc-bytestring-builder ghc-zlib-bindings ghc-io-streams"
GANETI_DEPENDS_PACKAGES5="ghc-enumerator ghc-attoparsec-enumerator ghc-blaze-builder-enumerator ghc-bytestring-mmap ghc-zlib-enum ghc-snap-core ghc-snap-server"
# ganeti
GANETI_PACKAGES="ganeti ganeti-instance-debootstrap"

# integ-ganeti repo
INTEG_GANETI_REPO_PACKAGES="integ-ganeti-release"

# sng-image
SNF_IMAGE_PACKAGES="python-prctl snf-image"

# all packages
PACKAGES="${GANETI_DEPENDS_PACKAGES1}
            ${GANETI_DEPENDS_PACKAGES2}
            ${GANETI_DEPENDS_PACKAGES3}
            ${GANETI_DEPENDS_PACKAGES4}
            ${GANETI_DEPENDS_PACKAGES5}
            ${GANETI_PACKAGES}
            ${SNF_IMAGE_PACKAGES}
            ${INTEG_GANETI_REPO_PACKAGES}"

# Directories
PACKAGER="$(basename "${0}")"
PACKAGER_DIR="$(cd "$(dirname "${0}")" && echo "${PWD}")"
PACKAGER_RPM_DIR="${PACKAGER_DIR}/rpmbuild"

# RPM macros
RPM_DIST=$(egrep "\%dist" /etc/rpm/macros.dist | awk '{ print $2 }' | sed -E 's|^(\..*)\..*|\1|')

# Usage
usage() {
    cat << _EOF_

Usage:
    ${PACKAGER} [-s] [-i] [-u] [-c|-C] [-l] [-o yes|no] [-a|-d|-p package...]]

    Options:
        -a Build all packages (ganeti and its dependencies and integ-ganeti repo, snf-image).
        -d Build ganeti dependencies packages only.
        -p Build the specified package(s) only. Available packages are:
            ganeti dependencies:
                ${GANETI_DEPENDS_PACKAGES1}
                ${GANETI_DEPENDS_PACKAGES2}
                ${GANETI_DEPENDS_PACKAGES3}
                ${GANETI_DEPENDS_PACKAGES4}
                ${GANETI_DEPENDS_PACKAGES5}
            ganeti:
                ${GANETI_PACKAGES}
            snf-image:
                ${SNF_IMAGE_PACKAGES}
            integ-ganeti-repo:
                ${INTEG_GANETI_REPO_PACKAGES}

        -o Overwrite built package: yes|no (Default: manual)

        -s Sign built packages.

        -i Install built packages.
        -u Uninstall installed packages.

        -c Clean the rpmbuild directory, but preserve downloaded archives.
        -C Completely clean the rpmbuild directory.

        -l List ghc dependencies in target packages.

_EOF_
}

# Check old package
check_oldpackage() {
    local PACKAGE="${1}"
    local is_first=0
    is_overwrite="-1"

    SPEC_FILE="SPECS/${PACKAGE}.spec"
    RPM_VERSION=$(egrep -i "^Version:" "${SPEC_FILE}" | awk '{ print $2 }')
    RPM_RELEASE=$(egrep -i "^Release:" "${SPEC_FILE}" | awk '{ print $2 }' | cut -d'%' -f 1)
    RPM_ARCHITECTURE=$(egrep -i "^(BuildArchitectures|BuildArch):" "${SPEC_FILE}" | awk '{ print $2 }' | tail -1)
    if [ -z "${RPM_ARCHITECTURE}" ]; then
        RPM_ARCHITECTURE=$(uname -i)
    fi

    RPM_FILE="RPMS/${RPM_ARCHITECTURE}/${PACKAGE}-${RPM_VERSION}-${RPM_RELEASE}${RPM_DIST}.${RPM_ARCHITECTURE}.rpm"
    if [ -f "${RPM_FILE}" ]; then
        if [ "${OVERWRITE_MODE}" = "yes" ]; then
            is_overwrite="y"
            return
        elif [ "${OVERWRITE_MODE}" = "no" ]; then
            is_overwrite="n"
            return
        fi

        while [ "${is_overwrite}" != "y" -a "${is_overwrite}" != "n" ];
        do
            if [ "${is_first}" -ne 0 ]; then
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

# Check sign key
check_signkey() {
    SIGNKEY=$(gpg --list-keys | grep "Ganeti RPM Packages" | wc -l)
    if [ "${SIGNKEY}" -lt 1 ]; then
        echo "Error: Ganeti RPM Packages sign key not found."
        exit 1
        SIGN_MODE="no"
    fi
}

# Clean but preserve downloaded archives
clean_minimal() {
    echo "Cleaning..."
    rm -rf "${PACKAGER_RPM_DIR}"/*/{BUILD,BUILDROOT,RPMS,SRPMS}
}

# Clean everything
clean_all() {
    echo "Cleaning Everything..."
    rm -rf "${PACKAGER_RPM_DIR}"/*/{BUILD,BUILDROOT,RPMS,SRPMS}
    rm -f "${PACKAGER_RPM_DIR}"/*/SOURCES/*.{gz,bz2}
}

# Uninstall packages
uninstall_package() {
    echo "Uninstall packages..."
    REMOVE_PACKAGES=""
    for PACKAGE in ${@}; do
        REMOVE_PACKAGES="${REMOVE_PACKAGES} ${PACKAGE} ${PACKAGE}-devel ${PACKAGE}-debuginfo"
    done
    yum -y remove ${REMOVE_PACKAGES}
}

install_package() {
    echo "Install packages..."
    for PACKAGE in ${@}; do
        pushd "${PACKAGER_RPM_DIR}/${PACKAGE}"

        set +e
        yum list installed "${PACKAGE}"
        RET=$?
        set -e
        if [ "${RET}" -ne 0 ]; then
            SPEC_FILE="SPECS/${PACKAGE}.spec"
            RPM_VERSION=$(egrep -i "^Version:" "${SPEC_FILE}" | awk '{ print $2 }')
            RPM_RELEASE=$(egrep -i "^Release:" "${SPEC_FILE}" | awk '{ print $2 }' | cut -d'%' -f 1)
            RPM_ARCHITECTURE=$(egrep -i "^(BuildArchitectures|BuildArch):" "${SPEC_FILE}" | awk '{ print $2 }' | tail -1)
            if [ -z "${RPM_ARCHITECTURE}" ]; then
                RPM_ARCHITECTURE=$(uname -i)
            fi

            # Install target version packages only
            echo "Instal ${PACKAGE} packages..."
            yum -y install RPMS/${RPM_ARCHITECTURE}/${PACKAGE}-*${RPM_VERSION}-${RPM_RELEASE}${RPM_DIST}.${RPM_ARCHITECTURE}.rpm
        fi

        popd
    done
}

# Build packages
build_package() {
    for PACKAGE in ${@}; do
        echo "Building package for ${PACKAGE}..."
        pushd "${PACKAGER_RPM_DIR}/${PACKAGE}"
        check_oldpackage "${PACKAGE}"
        local PACKAGE_SPEC_FILE="SPECS/${PACKAGE}.spec"
        if [ "${is_overwrite}" = "y" ]; then
            # Install build dependencies
            yum-builddep -y "${PACKAGE_SPEC_FILE}"

            # Download source and patch files
            if [ ! -d SOURCES ]; then
                mkdir SOURCES
            fi
            spectool -g -A "${PACKAGE_SPEC_FILE}" -C SOURCES/

            # Build package
            rpmbuild \
                --define "%_topdir ${PACKAGER_RPM_DIR}/${PACKAGE}" \
                --define "%dist ${RPM_DIST}" \
                -ba "${PACKAGE_SPEC_FILE}"

        fi

        # Install packages
        if [ "${INSTALL_MODE}" = "yes" ]; then
            install_package ${PACKAGE}
        fi

        echo
        popd
    done
}

sign_package() {
    for PACKAGE in ${@}; do
        echo "Signing package for ${PACKAGE}..."
        pushd "${PACKAGER_RPM_DIR}/${PACKAGE}"

        SIGN_RPM_LIST=""
        RPM_FILE_LIST=$(find SRPMS RPMS -name "*.rpm")
        for RPM_FILE in ${RPM_FILE_LIST}; do
            IS_SIGNED=$(rpm -K "${RPM_FILE}" | grep -i "(md5) pgp" | wc -l)
            if [ "${IS_SIGNED}" -eq 0 ]; then
                SIGN_RPM_LIST="${SIGN_RPM_LIST} ${RPM_FILE}"
            else
                echo "Skip sign: ${RPM_FILE} is already signed."
            fi
        done
        [ ! -z "${SIGN_RPM_LIST}" ] && rpm --addsign ${SIGN_RPM_LIST}

        echo
        popd
    done
}

ghc_dependency_list() {
    EGREP_REGEX=""
    for PACKAGE in ${PACKAGES}; do
        if [[ "${PACKAGE}" =~ ^ghc-(.*) ]]; then
            EGREP_REGEX="${EGREP_REGEX}|${BASH_REMATCH[1]}"
        fi
    done

    # echo "REGEX: \"(${EGREP_REGEX:1})-"
    ghc-pkg dot | tred | egrep "\"(${EGREP_REGEX:1})-" | sort
}

# Main
main() {
    [ $# -lt 1 ] && usage && exit 1

    # See how we're called.
    SIGN_MODE="no"
    INSTALL_MODE="no"
    UNINSTALL_MODE="no"
    BUILD_ALL="no"
    BUILD_PACKAGES="no"
    BUILD_GANETI_DEPENDS_PACKAGES="no"
    CLEAN_MODE="no"
    OVERWRITE_MODE="manual"
    GHC_DEPENDENCY_LIST="no"
    while getopts siuadpcCo:l OPT; do
        case "${OPT}" in
            "s" )
                SIGN_MODE="yes"
                check_signkey ;;
            "i" )
                INSTALL_MODE="yes" ;;
            "u" )
                UNINSTALL_MODE="yes" ;;
            "a" )
                BUILD_ALL="yes" ;;
            "d" )
                BUILD_GANETI_DEPENDS_PACKAGES="yes" ;;
            "p" )
                BUILD_PACKAGES="yes" ;;
            "c" )
                CLEAN_MODE="minimal" ;;
            "C" )
                CLEAN_MODE="all" ;;
            "o" )
                OVERWRITE_MODE="${OPTARG}" ;;
            "l" )
                GHC_DEPENDENCY_LIST="yes" ;;
            * )
                usage
                exit 1
                ;;
        esac
    done
    shift $((OPTIND - 1))

    # Clean task
    if [ "${CLEAN_MODE}" = "minimal" ]; then
        clean_minimal
    elif [ "${CLEAN_MODE}" = "all" ]; then
        clean_all
    fi

    # Uninstall task
    if [ "${UNINSTALL_MODE}" = "yes" ]; then
        if [ "${BUILD_ALL}" = "yes" ]; then
            uninstall_package "${PACKAGES}"
        elif [ "${BUILD_PACKAGES}" = "yes" ]; then
            uninstall_package "${@}"
        fi
    fi

    # Sign or Build task
    if [ "${SIGN_MODE}" = "yes" ]; then
        if [ "${BUILD_ALL}" = "yes" ]; then
            sign_package "${PACKAGES}"
        elif [ "${BUILD_PACKAGES}" = "yes" ]; then
            sign_package "${@}"
        fi
    elif [ "${BUILD_ALL}" = "yes" ]; then
        build_package "${PACKAGES}"
    elif [ "${BUILD_GANETI_DEPENDS_PACKAGES}" = "yes" ]; then
        build_package "${GANETI_DEPENDS_PACKAGES1} ${GANETI_DEPENDS_PACKAGES2} ${GANETI_DEPENDS_PACKAGES3} ${GANETI_DEPENDS_PACKAGES4} ${GANETI_DEPENDS_PACKAGES5}"
    elif [ "${BUILD_PACKAGES}" = "yes" ]; then
        build_package "${@}"
    fi

    # GHC dependency list task
    if [ "${GHC_DEPENDENCY_LIST}" = "yes" ]; then
        ghc_dependency_list
    fi

    echo
    echo "# Success: (${SECONDS} seconds)"
}

[ ${#BASH_SOURCE[@]} = 1 ] && main "${@}"

