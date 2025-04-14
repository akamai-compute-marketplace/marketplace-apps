---
title: "Deploy NetFoundry Edge Router through the Linode Marketplace"
description: "Follow this guide to deploy NetFoundry Edge Router on Linode using Marketplace Apps."
published: 2025-04-01
modified: 2025-04-01
keywords: ['netfoundry','marketplace apps', 'overlay', 'application defined network', 'secure network']
tags: ["ubuntu","cloud manager","linode platform","network","netfoundry","marketplace","ssl","connectivity"]
external_resources:
- '[NetFoundry (Documentation)](https://support.netfoundry.io/hc/en-us)'
---

[NetFoundry Edge Router](https://netfoundry.io/) NetFoundry Zero Trust is a secure networking solution that eliminates the need for traditional VPNs by implementing a zero-trust architecture. It ensures that only authenticated users and devices can access specific applications or resources, regardless of their location. By leveraging software-defined networking (SDN) and identity-based access controls, NetFoundry provides enhanced security, scalability, and performance for modern cloud and hybrid environments.

## Deploying a Marketplace App

{{< content "deploy-marketplace-apps-shortguide">}}

{{< content "marketplace-verify-standard-shortguide">}}

{{< note >}}
**Estimated deployment time:** NetFoundry Edge Router should be fully installed within 5-10 minutes after the Compute Instance has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:**  Ubuntu 24.04 LTS
- **Recommended minimum plan:** All plan types and sizes can be used, though a minimum of a 8GB Dedicated CPU Compute Instance is recommended for production.
- **VLAN support:** The registration will adjust itself to take advantage of a VLAN if one is configured during deployment.

### NetFoundry Edge Router Options

- **Registration Key**: Provide the registration key for the NetFoundry Edge Router deployment to register with your network.

    {{< note >}}
    The passwords for the NetFoundry Edge Router Admin User are automatically generated and provided in the file `/home/$USERNAME/.credentials` when the NetFoundry Edge Router deployment completes.
    {{< /note >}}

{{< content "marketplace-required-limited-user-fields-shortguide">}}

{{< content "marketplace-custom-domain-fields-shortguide">}}

{{< content "marketplace-special-character-limitations-shortguide">}}

## Getting Started After Deployment

### Obtain the Credentials

1.  Log in to your new Compute Instance using one of the methods below:

    - **Lish Console:** Within the Cloud Manager, navigate to **Linodes** from the left menu, select the Compute Instance you just deployed, and click the **Launch LISH Console** button. Log in as the `root` user. See [Using the Lish Console](/docs/products/compute/compute-instances/guides/lish/).
    - **SSH:** Log in to your Compute Instance over SSH using the `root` user. See [Connecting to a Remote Server Over SSH](/docs/guides/connect-to-server-over-ssh/) for assistance.

1.  Once logged in, access the credentials file by running the following command:

    ```command
    cat /home/$USERNAME/.credentials
    ```

1.  This displays the passwords that were automatically generated when the instance was deployed. Once you save these passwords, you can safely delete this file.

### Registering the Edge Router Manually

If you provided the registration key and the app has been *fully* deployed, everything is complete. If you did not provide a registration key, please continue:

1.  Once again log into your new Compute Instace via **List Console** or **SSH**

1.  Issue one of the following registration commmands:

   ```command
   # Single interface
   sudo router-registration {registration key}
   ```

   ```command
   # Multiple Interface(VLAN)
   sudo router-registration {registration key} -e {IP of Second Interface} -i {IP of Second Interface}
   ```

## Going Further

Now that your NetFoundry Edge Router installation is deployed, you can continue your configuration of your NetFoundry network.  Here are a few links to help get you started:

- [NetFoundry Console](https://nfconsole.io/login): Configure your network.
- [NetFoundry Edge Router Support](https://support.netfoundry.io/hc/en-us): Learn the basics for using NetFoundry Edge Router.
- [NetFoundry Videos](https://www.youtube.com/c/NetFoundry): A YouTube channel dedicated to NetFoundry.

{{< content "marketplace-update-note-shortguide">}}