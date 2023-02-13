#! /bin/bash

USER=ristop
PYSCRIPT="vr_park_remap.py"

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PYSCRIPT_PATH="${SCRIPTPATH}/${PYSCRIPT}"

# Hack to get Notifications to work, maybe needs modifying
export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/1000

/bin/su $USER -c "/usr/bin/python3 $PYSCRIPT_PATH $1"
