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

if [[ -n "${DOMAIN}" ]]; then
        UDF_VARS["DOMAIN"]="${DOMAIN}"
else
        UDF_VARS["DOMAIN"]="${DEFAULT_DNS}" # default
fi

if [[ -n "${SUBDOMAIN}" ]]; then
        UDF_VARS["SUBDOMAIN"]="${SUBDOMAIN}"
else
        UDF_VARS["SUBDOMAIN"]="www" # default
fi

if [[ -n "${TOKEN_PASSWORD}" ]]; then
        UDF_VARS["TOKEN_PASSWORD"]="${TOKEN_PASSWORD}"
else
        UDF_VARS["TOKEN_PASSWORD"]="HugsAreWorthMoreThanHandshakes" # default
fi

if [[ -n "${SOA_EMAIL_ADDRESS}" ]]; then
        UDF_VARS["SOA_EMAIL_ADDRESS"]="${SOA_EMAIL_ADDRESS}"
else
        UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}" # default
fi

if [[ -n "${PASSBOLT_FIRST_ADMIN_USERNAME}" ]]; then
        UDF_VARS["PASSBOLT_FIRST_ADMIN_USERNAME"]="${PASSBOLT_FIRST_ADMIN_USERNAME}"
else
        UDF_VARS["PASSBOLT_FIRST_ADMIN_USERNAME"]="passboltadmin" # default
fi

if [[ -n "${PASSBOLT_FIRST_ADMIN_SURNAME}" ]]; then
        UDF_VARS["PASSBOLT_FIRST_ADMIN_SURNAME"]="${PASSBOLT_FIRST_ADMIN_SURNAME}"
else
        UDF_VARS["PASSBOLT_FIRST_ADMIN_SURNAME"]="passboltsurname" # default
fi

if [[ -n "${PASSBOLT_FIRST_ADMIN_EMAIL}" ]]; then
        UDF_VARS["PASSBOLT_FIRST_ADMIN_EMAIL"]="${PASSBOLT_FIRST_ADMIN_EMAIL}"
else
        UDF_VARS["PASSBOLT_FIRST_ADMIN_EMAIL"]="passbolt@{DEFAULT_DNS}" # default
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