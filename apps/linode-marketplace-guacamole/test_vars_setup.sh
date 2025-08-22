#!/bin/bash
WORK_DIR="/tmp/marketplace-apps"
MARKETPLACE_APP="apps/linode-marketplace-guacamole"
USER_NAME="testuser"
DISABLE_ROOT="No"
SOA_EMAIL_ADDRESS="test@example.com"

group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
mkdir -p $(dirname ${group_vars})

sed 's/  //g' <<EOV > ${group_vars}
# sudo username
username: ${USER_NAME}
webserver_stack: lemp
EOV

if [ "$DISABLE_ROOT" = "Yes" ]; then
  echo "disable_root: yes" >> ${group_vars};
else echo "Leaving root login enabled";
fi

# Set default DNS using server IP  
echo "default_dns: 66-228-36-22.ip.linodeusercontent.com" >> ${group_vars}
echo "subdomain: www" >> ${group_vars}

if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
  echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars}
fi

echo "mode: production" >> ${group_vars}

echo "Generated group_vars file:"
cat ${group_vars}
