#!/bin/bash

DEFAULT_DNS="$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"

declare -A UDF_VARS
UDF_VARS["USER_NAME"]="admin"
UDF_VARS["SOA_EMAIL_ADDRESS"]="webmaster@${DEFAULT_DNS}"
UDF_VARS["DISABLE_ROOT"]="No"
UDF_VARS["SUBDOMAIN"]=""
UDF_VARS["DOMAIN"]=""

UDF_VARS["ALLOWED_IPS"]=""
UDF_VARS["APP_NAME"]="Marketplace"
UDF_VARS["GITHUB_OAUTH_CLIENT_ID"]="ci-test"
UDF_VARS["GITHUB_OAUTH_CLIENT_SECRET"]="ci-test"
UDF_VARS["GITHUB_USERNAME"]="ci-test"
UDF_VARS["BACKSTAGE_ORGNAME"]="Marketplace"
UDF_VARS["GITHUB_PAT"]=""

set_vars() {
  for key in "${!UDF_VARS[@]}"; do
    export "${key}"="${UDF_VARS[$key]}"
  done
}

# main
set_vars