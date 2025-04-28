#!/bin/bash

DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

declare -A UDF_VARS
UDF_VARS["USER_NAME"]="admin"
UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}"
UDF_VARS["DISABLE_ROOT"]="No"
UDF_VARS["SUBDOMAIN"]=""
UDF_VARS["DOMAIN"]=""

UDF_VARS["DRUPAL_SITE_NAME"]="My Drupal Site"
UDF_VARS["DRUPAL_SITE_EMAIL"]="system@example.com"
UDF_VARS["DRUPAL_ACCOUNT_EMAIL"]="admin@example.com"
UDF_VARS["DRUPAL_USERNAME"]="admin"

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars