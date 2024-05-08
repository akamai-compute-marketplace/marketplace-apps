# Linode cPanel Deployment One-Click APP

cPanel is a Linux-based server/website administration platform that streamlines publishing and managing websites. It is widely used by individual businesses, web development agencies, and hosting platforms. cPanel (and the included WHM interface) provides an easy and intuitive method for managing all aspects of website administration, including software installation, DNS, databases, email, and much more.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| cPanel   | latest    | Control Panel |
| WHM  | latest   | Web Hosting Manager |


**Supported Distributions:**

- Ubuntu 20.04 LTS, AlmaLinux 9, AlmaLinux 8, Rocky Linux 9, Rocky Linux 8


## Use our API

Customers can choose to the deploy the cPanel app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.


Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN
- ROOT_PASS

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"

curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "backups_enabled": true,
    "booted": true,
    "image": "linode/ubuntu20.04",
    "label": "cPanellabel",
    "private_ip": false,
    "region": "us-central",
    "root_pass": "$ROOT_PASS",
    "stackscript_data": {},
    "stackscript_id": 595742,
    "type": "g6-dedicated-2"
}' https://api.linode.com/v4/linode/instances 
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"

linode-cli linodes create \
  --backups_enabled true \
  --booted true \
  --image 'linode/ubuntu20.04' \
  --label cpanellabel \
  --private_ip false \
  --region us-southeast \
  --root_pass '$ROOT_PASS' \
  --stackscript_data '{}' \
  --stackscript_id 595742 \
  --type g6-dedicated-2
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)

