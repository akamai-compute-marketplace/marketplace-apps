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
UDF_VARS["AKAMAI_CLIENT_SECRET"]="abcdEcSnaAt123FNkBxy456z25qx9Yp5CPUxlEfQeTDkfh4QA=I"
UDF_VARS["AKAMAI_HOST"]="akab-lmn789n2k53w7qrs10cxy-nfkxaa4lfk3kd6ym.luna.akamaiapis.net"
UDF_VARS["AKAMAI_ACCESS_TOKEN"]="akab-zyx987xa6osbli4k-e7jf5ikib5jknes3"
UDF_VARS["AKAMAI_CLIENT_TOKEN"]="akab-nomoflavjuc4422-fa2xznerxrm3teg7"

# dynamic variables
if [[ -n "${INSTALL_LOKI}" ]]; then
        UDF_VARS["INSTALL_LOKI"]="${INSTALL_LOKI}"
else
        UDF_VARS["INSTALL_LOKI"]="No" # default
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars