#!/bin/bash

DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

# custom env variables from cli
if [[ -n ${INSTANCE_ENV} ]]; then
  custom_vars=(${INSTANCE_ENV})
  var_count=${#custom_vars[@]}
  count=0
  while [ ${count} -lt ${var_count} ]; do
    export ${custom_vars[count]}
  count=$(( $count + 1 ))
  done
fi

declare -A UDF_VARS
UDF_VARS["USER_NAME"]="admin"
UDF_VARS["DISABLE_ROOT"]="No"
UDF_VARS["KALI_PACKAGE"]="Default"
UDF_VARS["VNC"]="No"
UDF_VARS["VNC_USERNAME"]="kaliuser"

# dynamic variables
if [[ -n "${KALI_PACKAGE}" ]]; then
        UDF_VARS["KALI_PACKAGE"]="${KALI_PACKAGE}"
else
        UDF_VARS["KALI_PACKAGE"]="Default" # default (kali-linux-default)
fi

if [[ -n "${VNC}" ]]; then
        UDF_VARS["VNC"]="${VNC}"
else
        UDF_VARS["VNC"]="No" # default
fi

if [[ -n "${DISABLE_ROOT}" ]]; then
        UDF_VARS["DISABLE_ROOT"]="${DISABLE_ROOT}"
else
        UDF_VARS["DISABLE_ROOT"]="No" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars 