#!/bin/bash

DEFAULT_DNS="$(hostname -I | awk '{print $1}' | tr '.' '-' | awk '{print $1 ".ip.linodeusercontent.com"}')"

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

# UDF Variables

declare -A UDF_VARS

if [[ -n "${SUDO_USERNAME}" ]]; then
        UDF_VARS["SUDO_USERNAME"]="${SUDO_USERNAME}"
else
        UDF_VARS["SUDO_USERNAME"]="rtuser" # default
fi

if [[ -n "${SUDO_PASSWORD}" ]]; then
        UDF_VARS["SUDO_PASSWORD"]="${SUDO_PASSWORD}"
else
        UDF_VARS["SUDO_PASSWORD"]="rtSurveyTest1!" # default
fi

if [[ -n "${SSH_PUBLIC_KEY}" ]]; then
        UDF_VARS["SSH_PUBLIC_KEY"]="${SSH_PUBLIC_KEY}"
else
        UDF_VARS["SSH_PUBLIC_KEY"]="" # default
fi

if [[ -n "${TIMEZONE}" ]]; then
        UDF_VARS["TIMEZONE"]="${TIMEZONE}"
else
        UDF_VARS["TIMEZONE"]="UTC" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars
