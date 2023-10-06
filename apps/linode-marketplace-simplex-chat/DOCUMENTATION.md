---
slug: deploy-simplex-with-marketplace-apps
author:
  name: shum
  email: sh@simplex.chat
description: 'Deploy a SimpleX Servers on Linode using Marketplace Apps.'
og_description: 'Deploy a SimpleX Servers on Linode using Marketplace Apps.'
keywords: [ 'simplex','marketplace', 'server']
tags: ["cloud","linode platform", "marketplace"]
published: 2023-09-10
modified: 2023-09-10
modified_by:
  name: shum
title: "How to Deploy a SimpleX Servers with Marketplace Apps"
h1_title: "Deploying a SimpleX Servers with Marketplace Apps"
contributor:
  name: shum
external_resources:
- '[SimpleX Official](https://simplex.chat/)'
aliases: ['/platform/marketplace/deploy-simplex-with-marketplace-apps/', '/platform/one-click/deploy-simplex-with-one-click-apps/']
---

## SimpleX Marketplace App

SimpleX Chat is the first messaging platform that has no user identifiers of any kind - 100% private by design.

## Deploy SimpleX with Marketplace Apps

{{< content deploy-marketplace-apps >}}

### SimpleX Options

| **Configuration** | **Description** |
|-------------------|-----------------|
| **SMP server password (optional)** | Sets the password for smp-server. |
| **XFTP server quota (optional)** | Sets the file server storage quota in GB. |
| **Your Linode API Token (optional)** | Your Linode `API Token` is needed to create DNS records. If this is provided along with the `subdomain` and `domain` fields, the installation attempts to create DNS records via the Linode API. If you don't have a token, but you want the installation to create DNS records, you must [create one](/docs/platform/api/getting-started-with-the-linode-api/#get-an-access-token) before continuing. |
| **The subdomain for Linode's DNS record (optional)** | The subdomain you wish the installer to create a DNS record for during setup. The subdomain should only be provided if you also provide a `domain` and `API Token`. |
| **The domain for the Linode's DNS record (optional)** | The domain name where you wish to host your  server. The installer creates a DNS record for this domain during setup if you provide this field along with your `API Token`. |
| **The SSH Public Key that will be used to access the Linode (optional)** | If you wish to access [SSH via Public Key](/docs/security/authentication/use-public-key-authentication-with-ssh/) (recommended) rather than by password, enter the public key here. |
| **Disable root access over SSH? (optional)** | Select `Yes` to block the root account from logging into the server via SSH. Select `No` to allow the root account to login via SSH. |

### Linode Options

After providing the app-specific options, provide configurations for your Linode server:

| **Configuration** | **Description** |
|-------------------|-----------------|
| **Select an Image** | Default is Ubuntu 22.04 *Required* |
| **Region** | The region where you would like your Linode to reside. In general, it's best to choose a location that's closest to you. For more information on choosing a DC, review the [How to Choose a Data Center](/docs/platform/how-to-choose-a-data-center) guide. You can also generate [MTR reports](/docs/networking/diagnostics/diagnosing-network-issues-with-mtr/) for a deeper look at the network routes between you and each of our data centers. *Required*. |
| **Linode Plan** | Your Linode's [hardware resources](/docs/platform/how-to-choose-a-linode-plan/#hardware-resource-definitions). You can use any size Linode for your SimpleX server. The Linode plan that you select should be appropriate for the amount of data transfer, users, storage, and other stress that may affect the performance of server.  *Required* |
| **Linode Label** | The name for your Linode, which must be unique between all of the Linodes on your account. This name is how you identify your server in the Cloud Manager’s Dashboard. *Required*. |
| **Root Password** | The primary administrative password for your Linode instance. This password must be provided when you log in to your Linode via SSH. The password must meet the complexity strength validation requirements for a strong password. Your root password can be used to perform any action on your server, so make it long, complex, and unique. *Required* |
| **The limited sudo user to be created for the Linode** | This is the limited user account to be created for the Linode. This account has sudo user privileges. |
| **The password for the limited sudo user** | Set a password for the limited sudo user. The password must meet the complexity strength validation requirements for a strong password. This password can be used to perform any action on your server, similar to root, so make it long, complex, and unique. |

When you've provided all required Linode Options, click on the **Create** button. **Your SimpleX Servers  will complete installation anywhere between 5-10 minutes after your Linode has finished provisioning**.

## Setting up the SimpleX Server

Once the SimpleX Server is up and running you can display your SMP and XFTP connection strings with this command on the server:

```sh
docker-compose --project-directory /etc/docker/compose/simplex logs | grep 'Server address' | uniq
```

Please see the following documentation: [SMP Documentation](https://simplex.chat/docs/server.html) and [XFTP Documentation](https://simplex.chat/docs/xftp-server.html)
