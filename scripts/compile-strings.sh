#!/bin/bash
LOCALES=$*

for LOCALE in ${LOCALES}
do
    echo "/i18n/veriso_"${LOCALE}".ts"
    # Note we don't use pylupdate with qt .pro file approach as it is flakey
    # about what is made available.
    /usr/lib/qt5/bin/lrelease i18n/veriso_${LOCALE}.ts
done
