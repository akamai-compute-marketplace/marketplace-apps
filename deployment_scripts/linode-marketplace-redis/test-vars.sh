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

# UDF Variables

declare -A UDF_VARS

if [[ -n "${USER_NAME}" ]]; then
        UDF_VARS["USER_NAME"]="${USER_NAME}"
else
        UDF_VARS["USER_NAME"]="admin" # default
fi

if [[ -n "${DISABLE_ROOT}" ]]; then
        UDF_VARS["DISABLE_ROOT"]="${DISABLE_ROOT}"
else
        UDF_VARS["DISABLE_ROOT"]="No" # default
fi

if [[ -n "${COUNTRY_NAME}" ]]; then
        UDF_VARS["COUNTRY_NAME"]="${COUNTRY_NAME}"
else
        UDF_VARS["COUNTRY_NAME"]="US" # default
fi

if [[ -n "${STATE_OR_PROVINCE_NAME}" ]]; then
        UDF_VARS["STATE_OR_PROVINCE_NAME"]="${STATE_OR_PROVINCE_NAME}"
else
        UDF_VARS["STATE_OR_PROVINCE_NAME"]="Pennsylvania" # default
fi

if [[ -n "${LOCALITY_NAME}" ]]; then
        UDF_VARS["LOCALITY_NAME"]="${LOCALITY_NAME}"
else
        UDF_VARS["LOCALITY_NAME"]="Philadelphia" # default
fi

if [[ -n "${ORGANIZATION_NAME}" ]]; then
        UDF_VARS["ORGANIZATION_NAME"]="${ORGANIZATION_NAME}"
else
        UDF_VARS["ORGANIZATION_NAME"]="Akamai Technologies" # default
fi

if [[ -n "${SOA_EMAIL_ADDRESS}" ]]; then
        UDF_VARS["SOA_EMAIL_ADDRESS"]="${SOA_EMAIL_ADDRESS}"
else
        UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}" # default
fi

if [[ -n "${CA_COMMON_NAME}" ]]; then
        UDF_VARS["CA_COMMON_NAME"]="${CA_COMMON_NAME}"
else
        UDF_VARS["CA_COMMON_NAME"]="Redis CA" # default
fi

if [[ -n "${CLIENT_COUNT}" ]]; then
        UDF_VARS["CLIENT_COUNT"]="${CLIENT_COUNT}"
else
        UDF_VARS["CLIENT_COUNT"]="1" # default
fi

if [[ -n "${ADD_ONS}" ]]; then
        UDF_VARS["ADD_ONS"]="${ADD_ONS}"
else
        UDF_VARS["ADD_ONS"]="none" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars