#!/bin/bash

DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

declare -A UDF_VARS
UDF_VARS["USER_NAME"]="admin"
UDF_VARS["DISABLE_ROOT"]="No"

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars