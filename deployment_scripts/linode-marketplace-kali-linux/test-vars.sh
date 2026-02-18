#!/bin/zsh

DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

# custom env variables from cli
if [[ -n ${INSTANCE_ENV} ]]; then
  custom_vars=(${=INSTANCE_ENV})
  for var in "${custom_vars[@]}"; do
    export "${var}"
  done
fi

# UDF Variables

typeset -A UDF_VARS

if [[ -n "${USER_NAME}" ]]; then
        UDF_VARS[USER_NAME]="${USER_NAME}"
else
        UDF_VARS[USER_NAME]="admin" # default
fi

if [[ -n "${DISABLE_ROOT}" ]]; then
        UDF_VARS[DISABLE_ROOT]="${DISABLE_ROOT}"
else
        UDF_VARS[DISABLE_ROOT]="No" # default
fi

if [[ -n "${KALI_PACKAGE}" ]]; then
        UDF_VARS[KALI_PACKAGE]="${KALI_PACKAGE}"
else
        UDF_VARS[KALI_PACKAGE]="Default" # default
fi

if [[ -n "${VNC}" ]]; then
        UDF_VARS[VNC]="${VNC}"
else
        UDF_VARS[VNC]="No" # default
fi

if [[ -n "${VNC_USERNAME}" ]]; then
        UDF_VARS[VNC_USERNAME]="${VNC_USERNAME}"
else
        UDF_VARS[VNC_USERNAME]="vncuser" # default
fi

if [[ -n "${ADD_ONS}" ]]; then
        UDF_VARS[ADD_ONS]="${ADD_ONS}"
else
        UDF_VARS[ADD_ONS]="none" # default
fi


set_vars() {
  for key in "${(@k)UDF_VARS}"; do
    export "${key}=${UDF_VARS[$key]}"
  done
}

# main
set_vars