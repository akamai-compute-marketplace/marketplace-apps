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
UDF_VARS["WIREGUARD_CLIENT_TUNNEL_IP"]="10.0.0.2/32"
UDF_VARS["WIREGUARD_ALLOWED_IPS"]="10.0.0.1/32,192.0.2.0/24"

# dynamic variables - these can be set via environment variables after server deployment
if [[ -n "${WIREGUARD_SERVER_PUBLIC_KEY}" ]]; then
        UDF_VARS["WIREGUARD_SERVER_PUBLIC_KEY"]="${WIREGUARD_SERVER_PUBLIC_KEY}"
else
        UDF_VARS["WIREGUARD_SERVER_PUBLIC_KEY"]="" # default
fi

if [[ -n "${WIREGUARD_SERVER_ENDPOINT}" ]]; then
        UDF_VARS["WIREGUARD_SERVER_ENDPOINT"]="${WIREGUARD_SERVER_ENDPOINT}"
else
        UDF_VARS["WIREGUARD_SERVER_ENDPOINT"]="" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars