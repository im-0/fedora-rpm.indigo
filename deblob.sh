#!/bin/bash

set -e -u -o pipefail

if [ $# -ne 2 ]; then
    echo "Usage: ${0} indigo-X.Y-Z.tar.gz indigo-free-X.Y-Z.tar.xz" >&2
    exit 1
fi
in="${1}"
out="${2}"

set -x

tmp=$( mktemp --directory --tmpdir "indigo-deblob.tmp.XXXXXXXXXX" )
tar -C "${tmp}" -vxf "${in}"
name=$( cd "${tmp}"; echo * )

path="${tmp}/${name}"

# Remove binaries.
rm --recursive --verbose "${path}/bin_externals"
rm --recursive --verbose "${path}/indigo_libs/bin_externals"
for driver in \
        "aux_dsusb" \
        "ccd_altair" \
        "ccd_apogee" \
        "ccd_asi" \
        "ccd_atik" \
        "ccd_baccam" \
        "ccd_bresser" \
        "ccd_mallin" \
        "ccd_meade" \
        "ccd_mi" \
        "ccd_ogma" \
        "ccd_omegonpro" \
        "ccd_playerone" \
        "ccd_qhy" \
        "ccd_qhy2" \
        "ccd_qsi" \
        "ccd_rising" \
        "ccd_sbig" \
        "ccd_ssg" \
        "ccd_svb" \
        "ccd_svb2" \
        "ccd_touptek" \
        "focuser_asi" \
        "focuser_astroasis" \
        "focuser_fcusb" \
        "guider_asi" \
        "guider_gpusb" \
        "rotator_asi" \
        "wheel_asi" \
        "wheel_astroasis" \
        "wheel_atik" \
        "wheel_mi" \
        "wheel_playerone" \
        ; do
    rm --recursive --verbose "${path}/indigo_drivers/${driver}"
done

# Sanity check.
find "${path}" \
        -type "f" \
        "(" \
            -name "*.a" \
            -or \
            -name "*.so" \
            -or \
            -iname "*.dylib" \
            -or \
            -iname "*.dll" \
            -or \
            -iname "*.lib" \
            -or \
            -iname "*.tgz" \
            -or \
            -iname "*.tbz" \
            -or \
            -iname "*.tbz2" \
            -or \
            -iname "*.tar.*" \
            -or \
            -iname "*.tar" \
            -or \
            -iname "*.zip" \
        ")" \
        -print \
        -quit \
    | grep "." \
    && (
        echo "FATAL: Binaries detected in the source tree" >&2
        exit 1
    )

# Repack.
tar -C "${tmp}" -vc "${name}" | xz -9 >"${out}"

# Remove temprory directory.
rm --recursive "${tmp}"
