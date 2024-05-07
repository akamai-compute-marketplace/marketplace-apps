# Marketplace App Development Guidelines

A Marketplace App leverages the Linode API and Ansible to deploy and configure a single node service. The end-user’s Linode API token must be scoped with appropriate permissions to add and remove the necessary platform resources, such as compute, DNS, storage, etc. In additon, please adhere to the following guidelines for Marketplace apps:

  - We recommend Marketplace applications use Ubuntu 22.04 LTS images when possible. 
  - Required Linode plans for Marketplace applications should be no more than 16GB shared CPU or 8GB dedicated  CPU. This is the default instance size limit for new user accounts. Deployments designed for larger instance sizes can be accepted on a case-by-case basis where required. 
  - The deployment of the service should be “hands-off,” requiring no command-line intervention from the user before reaching its initial state. The end user should provide all necessary details via User Defined Variables (UDF) defined in the StackScript, so that Ansible can fully automate the deployment.
  - There is not currently password strength validation for StackSctript UDFs, therefore, whenever possible credentials should be generated and provided to the end-user.
  - At no time should billable services that will not be used in the final deployment be present on the customer’s account.
  - To whatever extent possible all Marketplace applications should use fully maintained packages and automated updates. 
  - All Marketplace applications should include Linux server best practices such as a sudo-user, SSH hardening and basic firewall configurations. 
  - All Marketplace applications should generally adhere to the best practices for the deployed service, and include security such as SSL whenever possible. 
  - All Marketplace service installations should be minimal, providing no more than dependencies and removing deployment artifacts. 

## Deployment Scripts

All Bash files, including the deployment Stackscript for each Marketplace App is kept in the `deployment_scripts` directory. Deployment Stackscripts should adhere to the following conventions.

- The StackScript must implement the [Linux trap command](https://man7.org/linux/man-pages/man1/trap.1p.html) for error handling.
- The primary purposes of the Stackscript is to assign global variables, create a working directory and Python venv before cloning the correct Marketplace App repo.
  - Installations and configurations that are not necessary for supporting the Ansible environment (i.e. Python or Git dependencies) should be performed with Ansible playbooks, and not included in the Stackscript. The StackScript should be as slim as possible, letting Ansible do most of the heavy lifting.
  - All working directories should be cleaned up on successful completion of the Stackscript.
  - A public deployment script must conform to the [Stackscript requirements](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/) and we strongly suggest including a limited number of [UDF variables](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs).

## Ansible Playbooks 

- All Ansible playbooks should generally adhere to the [sample directory layout](https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html#sample-ansible-setup) and best practices/recommendations from the latest Ansible [User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html).
  - All Ansible playbooks for Marketplace applications should include common [`.ansible-lint`](../apps/linode-marketplace-wordpress/.ansible-lint), [`.yamllint`](../apps/linode-marketplace-wordpress/.yamllint), [`ansible.cfg`](../apps/linode-marketplace-wordpress/ansible.cfg) and [`.gitignore`](../.gitignore) files.
  - All Ansible playbooks should use Ansible Vault for initial secrets management. Generated credentials should be provided to the end-user in a standard `.credentials` file located in the sudo user’s home directory. 
  - Whenever possible Jinja should be leveraged to populate a consistent variable naming convention during [node provisioning](../apps/linode-marketplace-wordpress/provision.yml).
  - It is recommended to import service specific tasks as modular `.yml` files under the application’s `main.yml`. 

Marketplace App playbooks should align with the following sample directory trees. There may be certain applications that require deviation from this structure, but they should follow as close as possible. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).

```
linode-marketplace-$APP/
  ansible.cfg
  collections.yml
  provision.yml
  requirements.txt
  site.yml
  .ansible-lint
  .yamllint
  .gitignore

  group_vars/
    $APP/
      vars 
      secret_vars
  
  roles/
    $APP/
      handlers/
        main.yml
      tasks/
        main.yml
      templates/
        $FILE.j2
    common/ 
      handlers/ 
        main.yml
      tasks/ 
        main.yml
    post/ 
     handlers/ 
        main.yml
      tasks/ 
        main.yml
      templates/
        MOTD.j2  
   
```
As general guidelines: 
  - The secrets in the `secret_vars` file should be encrypted with Ansible Vault
  - The `roles` should general conform to the following standards:
    - `common` - including preliminary configurations and Linux best practices.
    - `$app` - including all necessary plays for service/app deployment and configuration.
    - `post` - any post installation tasks such as clean up operations and generating additonal user credentials. This should include the creation of a credentials file in `/home/$SUDO_USER/.credentials` and a MOTD (Message of the Day) file to display after login to provide some additional direction after the deployment. 

## Helper Functions

Linode Helpers are static roles that can be called at will when we are trying to accomplish a repeatable system task. Instead of rewriting the same function for multiple One-Click Apps, we can simply import the Helper role to accomplish the same effect. This results in basic system configurations being performed predictably and reliably, without the variance of individual authors.

Keep in mind that roles are invoked sequentially. A Linode Helper, or any other role with dependancies must come after those dependencies are met. For example, the Linode Helper role `securemysql` must be imported after the task to install MySQL.

```
- name: installing mariadb
  apt:
    pkg:
    - mariadb-server
    - python3-mysqldb
    state: present
  register: mariadb

- name: running mysql secure installation
  import_role:
    name: securemysql
```

For more information on roles please refer to the [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-roles-at-the-play-level).

## User Defined Fields (UDF)
Below are examples of UDFs your deployment can use in the [deployment StackScript](../deployment_scripts/). For consistency, please name the deployment script `$app-deploy.sh` (example [here](../deployment_scripts/linode-marketplace-wordpress/)).

```
## Example App Settings
#<UDF name="app_header" label="App Settings" default="Yes" header="yes">
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld">
#<UDF name="webserver_stack" label="The stack you are looking to deploy the app on" oneOf="LAMP,LEMP">

#<UDF name="site_title" label="Website title" example="My Blog">
#<UDF name="admin_user" label="app username" example="admin">
#<UDF name="admin_password" label="app user password" example="s3cure_p4ssw0rd" default=""> 
#<UDF name="db_name" label="app database name" example="example">

## Linode/SSH Security Settings
#<UDF name="security_header" label="Security Settings" default="Yes" header="yes">
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">
#<UDF name="pubkey" label="The SSH Public Key that will be used to access the Linode (Recommended)" default="">

## Domain Settings
#<UDF name="domain_header" label="Domain Settings" default="Yes" header="yes">
#<UDF name="token_password" label="Your Linode API token. This is needed to create your Linode's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record. `www` will be entered if no subdomain is supplied (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## Self-Signed Certificate Settings 
# <UDF name="sslheader" label="SSL Information" header="Yes" default="Yes" required="Yes">
# <UDF name="country_name" label="Details for self-signed SSL certificates: Country or Region" oneof="AD,AE,AF,AG,AI,AL,AM,AO,AQ,AR,AS,AT,AU,AW,AX,AZ,BA,BB,BD,BE,BF,BG,BH,BI,BJ,BL,BM,BN,BO,BQ,BR,BS,BT,BV,BW,BY,BZ,CA,CC,CD,CF,CG,CH,CI,CK,CL,CM,CN,CO,CR,CU,CV,CW,CX,CY,CZ,DE,DJ,DK,DM,DO,DZ,EC,EE,EG,EH,ER,ES,ET,FI,FJ,FK,FM,FO,FR,GA,GB,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GR,GS,GT,GU,GW,GY,HK,HM,HN,HR,HT,HU,ID,IE,IL,IM,IN,IO,IQ,IR,IS,IT,JE,JM,JO,JP,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LT,LU,LV,LY,MA,MC,MD,ME,MF,MG,MH,MK,ML,MM,MN,MO,MP,MQ,MR,MS,MT,MU,MV,MW,MX,MY,MZ,NA,NC,NE,NF,NG,NI,NL,NO,NP,NR,NU,NZ,OM,PA,PE,PF,PG,PH,PK,PL,PM,PN,PR,PS,PT,PW,PY,QA,RE,RO,RS,RU,RW,SA,SB,SC,SD,SE,SG,SH,SI,SJ,SK,SL,SM,SN,SO,SR,SS,ST,SV,SX,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TR,TT,TV,TW,TZ,UA,UG,UM,US,UY,UZ,VA,VC,VE,VG,VI,VN,VU,WF,WS,YE,YT,ZA,ZM,ZW" />
# <UDF name="state_or_province_name" label="State or Province" example="Example: Pennsylvania" />
# <UDF name="locality_name" label="Locality" example="Example: Philadelphia" />
# <UDF name="organization_name" label="Organization" example="Example: Akamai Technologies"  />
# <UDF name="email_address" label="Email Address" example="Example: user@domain.tld" />
# <UDF name="ca_common_name" label="CA Common Name" default="App CA" />
# <UDF name="common_name" label="Common Name" default="App Server"  />
```
### UDF Tips and Tricks 

- UDFs without a `default` are required. 
- UDFs with a `default` will write that default if the customer does not enter a value. Non printing characters are treated literally in defaults.
- UDFs containing the string `password` within the `name` will display as obfuscated dots in the Cloud Manager. They are also encrypted on the host and do not log.
- A UDF containing `label="$label" header="Yes" default="Yes" required="Yes"` will display as a header in the Cloud Manager, but does not affect deployment.

## Testing on Linode

To test your Marketplace App you can provision and deploy the app to Linodes on your account. Note that billing will occur for any Linode instances deployed.

To test your Marketplace App on Linode infrastucutre, copy and paste `$app-deploy.sh` into a new Stackscript on your account. Then update the Git Repo section of `$app-deploy.sh` to include your fork of the Marketplace repo. Finally, substitute the provided Stackscript ID into our example [API calls](apps/linode-marketplace-wordpress/README.md#use-our-api). Logging output can be viewed in `/var/log/stackscript.log` in the deployed instance.