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
UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}"
UDF_VARS["COUNTRY_NAME"]="US"
UDF_VARS["STATE_OR_PROVINCE_NAME"]="Pennsylvania"
UDF_VARS["LOCALITY_NAME"]="Philadelphia"
UDF_VARS["ORGANIZATION_NAME"]="Akamai"
UDF_VARS["EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}"

# dynamic variables
#if [[ -n "${CHANGE_ME}" ]]; then
#        UDF_VARS["CHANGE_ME"]="${CHANGE_ME}"
#else
#        UDF_VARS["CHANGE_ME"]="some value" # default
#fi

if [[ -n "${DOMAIN}" ]]; then
        UDF_VARS["DOMAIN"]="${DOMAIN}"
else
        UDF_VARS["DOMAIN"]="" # default
fi

if [[ -n "${SUBDOMAIN}" ]]; then
        UDF_VARS["SUBDOMAIN"]="${SUBDOMAIN}"
else
        UDF_VARS["SUBDOMAIN"]="" # default
fi

# openbao vars

if [[ -n "${CLIENT_IPS}" ]]; then
        UDF_VARS["CLIENT_IPS"]="${CLIENT_IPS}"
else
        UDF_VARS["CLIENT_IPS"]="" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars