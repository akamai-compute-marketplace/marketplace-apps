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

if [[ -n "${WIREGUARD_SERVER_PUBLIC_KEY}" ]]; then
        UDF_VARS["WIREGUARD_SERVER_PUBLIC_KEY"]="${WIREGUARD_SERVER_PUBLIC_KEY}"
else
        UDF_VARS["WIREGUARD_SERVER_PUBLIC_KEY"]="Aok+csm4V2GoT81orYzU4Y+AgZT1WHkvDnGv4Hb4CWQ=" # default
fi

if [[ -n "${WIREGUARD_SERVER_ENDPOINT}" ]]; then
        UDF_VARS["WIREGUARD_SERVER_ENDPOINT"]="${WIREGUARD_SERVER_ENDPOINT}"
else
        UDF_VARS["WIREGUARD_SERVER_ENDPOINT"]="127.0.0.1:51820" # default
fi

if [[ -n "${WIREGUARD_CLIENT_TUNNEL_IP}" ]]; then
        UDF_VARS["WIREGUARD_CLIENT_TUNNEL_IP"]="${WIREGUARD_CLIENT_TUNNEL_IP}"
else
        UDF_VARS["WIREGUARD_CLIENT_TUNNEL_IP"]="10.0.0.2/32" # default
fi

if [[ -n "${WIREGUARD_ALLOWED_IPS}" ]]; then
        UDF_VARS["WIREGUARD_ALLOWED_IPS"]="${WIREGUARD_ALLOWED_IPS}"
else
        UDF_VARS["WIREGUARD_ALLOWED_IPS"]="10.0.0.1/32" # default
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