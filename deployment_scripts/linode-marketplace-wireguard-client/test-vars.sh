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
UDF_VARS["WIREGUARD_SERVER_PUBLIC_KEY"]="5+m82uxMXQchGKbTb3lpQbxxG9g+GXz1vjFC6Pa8zi8="
UDF_VARS["WIREGUARD_SERVER_ENDPOINT"]="170.187.144.181:51820"
UDF_VARS["WIREGUARD_CLIENT_TUNNEL_IP"]="10.0.0.2/32"
UDF_VARS["WIREGUARD_ALLOWED_IPS"]="10.0.0.1/32"
UDF_VARS["WIREGUARD_PERSISTENT_KEEPALIVE"]="25"
UDF_VARS["WIREGUARD_MTU"]="1420"
UDF_VARS["WIREGUARD_DNS"]="1.1.1.1,8.8.8.8"

# dynamic variables
#if [[ -n "${CHANGE_ME}" ]]; then
#        UDF_VARS["CHANGE_ME"]="${CHANGE_ME}"
#else
#        UDF_VARS["CHANGE_ME"]="some value" # default
#fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars