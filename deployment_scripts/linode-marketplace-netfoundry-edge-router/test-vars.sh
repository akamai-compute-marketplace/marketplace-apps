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
UDF_VARS["SUBDOMAIN"]=""
UDF_VARS["DOMAIN"]=""
UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}"

# dynamic variables
if [[ -n "${REGISTRATION_KEY}" ]]; then
        UDF_VARS["REGISTRATION_KEY"]="${REGISTRATION_KEY}"
else
        UDF_VARS["REGISTRATION_KEY"]="none" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars