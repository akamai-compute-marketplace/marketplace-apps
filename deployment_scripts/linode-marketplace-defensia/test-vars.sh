#!/bin/bash

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

# Defensia install token (required)
if [[ -n "${TOKEN}" ]]; then
        UDF_VARS["TOKEN"]="${TOKEN}"
else
        UDF_VARS["TOKEN"]=""
fi

# Server name in dashboard (optional, defaults to hostname)
if [[ -n "${AGENT_NAME}" ]]; then
        UDF_VARS["AGENT_NAME"]="${AGENT_NAME}"
else
        UDF_VARS["AGENT_NAME"]="$(hostname -s)"
fi

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars
