# Linode Marketplace Apps

The Linode Marketplace is designed to make it easier for developers and companies to share [One-Click Apps](https://www.linode.com/marketplace/) with the Linode community. One-Click Apps are portable and modular solutioning tools written as Ansible playbooks. The Linode Marketplace allows users to quickly deploy services and perform essential configurations on a Linode compute instance's first boot. 

A Marketplace deployment refers to an application (single service on a single node) or a cluster (multi-node clustered service such as MongoDB with replica sets). A combination of StackScripts and Ansible playbooks give the Marketplace a one-click installation and delivery mechanism for deployments. The end user is billed just for the underlying cloud resources (compute instances, storage volumes, etc) in addition to any applicable BYOLs.

## Marketplace App Development Guidelines.

A Marketplace application consists of three major components: a Stackscript, Ansible playbooks, and Git repository to clone from.

### Stackscript

A [Stackscript](https://www.linode.com/docs/products/tools/stackscripts/guides/write-a-custom-script) is a Bash script adhering to industry best practices that is stored on Linode hosts and is accessible to all customers.

### Ansible Playbook

All Ansible playbooks should generally adhere to the [sample directory layout](https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html#sample-ansible-setup) and best practices/recommendations from the latest Ansible [User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html).

### Helper Functions

Linode Helpers are static roles that can be called at will when we are trying to accomplish a repeatable system task. Instead of rewriting the same function for multiple One-Click Apps, we can simply import the Helper role to accomplish the same effect. This results in basic system configurations being performed predictably and reliably, without the variance of individual authors.

More detailed information on Linode Helper functions and variables can be found in the [Linode Helper Readme](apps/linode_helpers/README.md).
For more information on roles please refer to the [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-roles-at-the-play-level).

## Creating Your Own

For more information on creating and submitting a Partner App for the Linode Marketplace please see [Contributing](docs/CONTRIBUTING.md) and [Development](docs/DEVELOPMENT.md).
