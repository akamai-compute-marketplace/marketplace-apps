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

if [[ -n "${TOKEN_PASSWORD}" ]]; then
        UDF_VARS["TOKEN_PASSWORD"]="${TOKEN_PASSWORD}"
else
        UDF_VARS["TOKEN_PASSWORD"]="" # default
fi

if [[ -n "${SUBDOMAIN}" ]]; then
        UDF_VARS["SUBDOMAIN"]="${SUBDOMAIN}"
else
        UDF_VARS["SUBDOMAIN"]="" # default
fi

if [[ -n "${DOMAIN}" ]]; then
        UDF_VARS["DOMAIN"]="${DOMAIN}"
else
        UDF_VARS["DOMAIN"]="" # default
fi

if [[ -n "${SOA_EMAIL_ADDRESS}" ]]; then
        UDF_VARS["SOA_EMAIL_ADDRESS"]="${SOA_EMAIL_ADDRESS}"
else
        UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}" # default
fi

if [[ -n "${SPLUNK_USER}" ]]; then
        UDF_VARS["SPLUNK_USER"]="${SPLUNK_USER}"
else
        UDF_VARS["SPLUNK_USER"]="splunkuser" # default
fi

if [[ -n "${SSLHEADER}" ]]; then
        UDF_VARS["SSLHEADER"]="${SSLHEADER}"
else
        UDF_VARS["SSLHEADER"]="Yes" # default
fi

if [[ -n "${ACCESS_TOKEN_PASSWORD}" ]]; then
        UDF_VARS["ACCESS_TOKEN_PASSWORD"]="${ACCESS_TOKEN_PASSWORD}"
else
        UDF_VARS["ACCESS_TOKEN_PASSWORD"]="" # default
fi

if [[ -n "${CLIENT_SECRET_PASSWORD}" ]]; then
        UDF_VARS["CLIENT_SECRET_PASSWORD"]="${CLIENT_SECRET_PASSWORD}"
else
        UDF_VARS["CLIENT_SECRET_PASSWORD"]="" # default
fi

if [[ -n "${CLIENT_TOKEN_PASSWORD}" ]]; then
        UDF_VARS["CLIENT_TOKEN_PASSWORD"]="${CLIENT_TOKEN_PASSWORD}"
else
        UDF_VARS["CLIENT_TOKEN_PASSWORD"]="" # default
fi

if [[ -n "${HOSTNAME}" ]]; then
        UDF_VARS["HOSTNAME"]="${HOSTNAME}"
else
        UDF_VARS["HOSTNAME"]="" # default
fi

if [[ -n "${SECURITY_CONFIG_ID}" ]]; then
        UDF_VARS["SECURITY_CONFIG_ID"]="${SECURITY_CONFIG_ID}"
else
        UDF_VARS["SECURITY_CONFIG_ID"]="" # default
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