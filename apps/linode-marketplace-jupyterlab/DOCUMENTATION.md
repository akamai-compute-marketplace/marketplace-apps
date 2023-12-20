---
description: "Deploy JupyterLab on a Linode Compute Instance. JupyterLab is a web-based interactive development environment for notebooks, code, and data."
keywords: ['productivity','notebook','data science']
tags: ["marketplace", "linode platform", "cloud manager"]
published: 2023-12-21
modified_by:
  name: Linode
title: "Deploy JupyterLab through the Linode Marketplace"
external_resources:
- '[Project Jupyter](https://jupyter.org/)'
authors: ["Linode"]
---

[JupyterLab](https://jupyter.org/) stands as the cutting-edge web-based interactive development environment, catering to notebooks, code, and data. With a flexible interface, users can effortlessly configure and arrange workflows in data science, scientific computing, computational journalism, and machine learning. Its modular design welcomes extensions, offering the flexibility to expand and enrich functionality as needed. Explore the limitless possibilities of JupyterLab for seamless and powerful interactive computing.

## Deploying a Marketplace App

{{< content "deploy-marketplace-apps-shortguide">}}

{{< content "marketplace-verify-standard-shortguide">}}

{{< note >}}
**Estimated deployment time:** JupyterLab should be fully installed within 10-15 minutes after the Compute Instance has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:** Ubuntu 22.04 LTS
- **Recommended plan:** All plan types and sizes can be used.

### JupyterLab Options

- **Email address** *(required)*: Enter the email address to use for generating the SSL certificates.

{{< content "marketplace-limited-user-fields-shortguide">}}

{{< content "marketplace-custom-domain-fields-shortguide">}}

{{< content "marketplace-special-character-limitations-shortguide">}}

### Getting Started after Deployment

## Accessing the JupyterLab Server

Open your web browser and go to the custom domain you specified during deployment or the rDNS domain of your Compute Instance (e.g., `192-0-2-1.ip.linodeusercontent.com`). This will take you to the Jupyter Server login page, where you'll be prompted to enter a token or password. Refer to the [Managing IP Addresses](/docs/products/compute/compute-instances/guides/manage-ip-addresses/) guide for details on finding IP addresses and rDNS information. 

## Obtaining the JupyterLab Access Token

By default, JupyterLab issues a token for authentication. The Jupyter server access token was automatically generated during the initial install process. To obtain this token, log in to your Compute Instance either through the [LISH Console](https://www.linode.com/docs/products/compute/compute-instances/guides/lish/#through-the-cloud-manager-weblish) or via SSH, and run the following pre-defined script: 
```
./get_jupyter_token.sh
```
Executing this action will display the JupyterLab access token in your current terminal session. Copy and paste this token into the **Password or token:** field on the Jupyter Server login page.

Alternatively, if you favor password authentication, utilize the token to establish a password in the **Setup a Password** field on the login page. Once this is done, you can employ both the token and the password for accessing JupyterLab.

### More Information

You may wish to consult the following resources for additional information on this topic. While these are provided in the hope that they will be useful, please note that we cannot vouch for the accuracy or timeliness of externally hosted materials.

- [Project Jupyter](https://jupyter.org/)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/en/latest/)

{{< content "marketplace-update-note-shortguide">}}