#!/bin/bash
DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

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

if [[ -n "${SUBDOMAIN}" ]]; then 
	UDF_VARS["SUBDOMAIN"]="${SUBDOMAIN}" 
else 
	UDF_VARS["SUBDOMAIN"]="${DEFAULT_DNS%%.*}" 
fi

if [[ -n "${DOMAIN}" ]]; then 
	UDF_VARS["DOMAIN"]="${DOMAIN}"
else 
	UDF_VARS["DOMAIN"]=""
fi

if [[ -n "${ADMIN_EMAIL}" ]]; then 
	UDF_VARS["ADMIN_EMAIL"]="${ADMIN_EMAIL}"
else 
	UDF_VARS["ADMIN_EMAIL"]="admin@${DEFAULT_DNS}" 
fi

if [[ -n "${SMTP_ADDRESS}" ]]; then 
	UDF_VARS["SMTP_ADDRESS"]="${SMTP_ADDRESS}"
else 
	UDF_VARS["SMTP_ADDRESS"]="${DEFAULT_DNS}"
fi

if [[ -n "${SMTP_PORT}" ]]; then 
	UDF_VARS["SMTP_PORT"]="${SMTP_PORT}"
else 
	UDF_VARS["SMTP_PORT"]="587"
fi

if [[ -n "${SMTP_USER_NAME}" ]]; then 
	UDF_VARS["SMTP_USER_NAME"]="${SMTP_USER_NAME}"
else 
	UDF_VARS["SMTP_USER_NAME"]="test"
fi

if [[ -n "${SMTP_PASSWORD}" ]]; then 
	UDF_VARS["SMTP_PASSWORD"]="${SMTP_PASSWORD}"
else 
	UDF_VARS["SMTP_PASSWORD"]="testpassword"
fi

if [[ -n "${SMTP_NOTIFICATION_EMAIL}" ]]; then 
	UDF_VARS["SMTP_NOTIFICATION_EMAIL"]="${SMTP_NOTIFICATION_EMAIL}"
else 
	UDF_VARS["SMTP_NOTIFICATION_EMAIL"]="noreply@${DEFAULT_DNS}"
fi

if [[ -n "${DISCOURSE_SMTP_DOMAIN}" ]]; then 
	UDF_VARS["DISCOURSE_SMTP_DOMAIN"]="${DISCOURSE_SMTP_DOMAIN}"
else 
	UDF_VARS["DISCOURSE_SMTP_DOMAIN"]="${DEFAULT_DNS}"
fi

if [[ -n "${ADD_ONS}" ]]; then 
	UDF_VARS["ADD_ONS"]="${ADD_ONS}"
else
	UDF_VARS["ADD_ONS"]="none"
fi

set_vars() {
	for key in "${!UDF_VARS[@]}"; do
		export "${key}"="${UDF_VARS[$key]}"
	done
}

set_vars
