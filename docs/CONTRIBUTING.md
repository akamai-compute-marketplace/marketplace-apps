# Contributing

Thanks for your interest in contributing to the Linode Marketplace!

You can contribute by [opening an issue](https://github.com/akamai-compute-marketplace/marketplace-apps/issues) or submitting a pull request. Best practices for development of Linode Marketplace Apps are discussed in the [Development Readme](docs/DEVELOPMENT.md).

## Opening an issue

Feel free to open an issue to report a bug or request a feature.

## Submitting a pull request

1. Fork this repository.
2. Clone your fork to your local machine.
3. Create a branch from `develop`, e.g. `$ git checkout develop && git pull && git checkout -b feature/my-feature`.
4. Make your changes, commit them, then push them to your fork.
5. Open a pull request against `develop`.

## App information

In addition to submitting your [Ansible playbook](https://docs.ansible.com/ansible/2.8/user_guide/playbooks.html) that will run on Linode Compute Instances to install the application, Linode requires additional information and brand assets for your Marketplace listing on Linode.com. Submit the following required information as a .txt or .md file along with your StackScript and assets folder in your submission pull request.

**App Name**

**App README** \
*Please write a README.md following the format of this [example](../apps/linode-marketplace-wordpress/README.md).*

**App Description**  
*A short description (100-125 words) to go with your app listing in Marketplace on Linode.com. Note that this description is subject to edits before publication.*

**Version Number**

**Support URL**  
*All apps must have a designated support URL to direct users to a resource like a Contact form, specific Community forum, or active social media account they can contact for help.*

**Operating System**  
*One-Click Apps currently support Debian 11, and Ubuntu 22.04 LTS.*

**Documentation**  
Providing thorough technical documentation is a requirement of submitting a One-Click App to Linode’s Marketplace for both testing purposes and publishing the Doc to our Docs Library.

[Documentation Example: Deploying WordPress with One-Click Apps.](https://www.linode.com/docs/platform/one-click/deploying-wordpress-with-one-click-apps/)

Add your documentation as an additional file in your pull request or add a link to documentation on your company website.

## App Assets

*Submit assets via .zip folder with your pull request.*

Linode’s Marketplace listings features gradient backgrounds and a prominent logo display, as well as the logos in Cloud Manager. Please follow the directions for submitting design assets. Application submissions will not be accepted without the required assets.

**Brand Color 1 (HEX Code)**  
*Linode’s Marketplace listings feature gradient hero graphics to showcase brand colors. Please select a brand color to display on the left side of the gradient.*

**Brand Color 2 (HEX Code)**  
*Linode’s Marketplace listings feature gradient hero graphics to showcase brand colors. Please select a brand color to show on the right side of the gradient. If left blank, Linode will substitute the secondary brand color with black.*

**Logo**  
*Submit vector files of your app's logo in white and full color. (SVG, EPS, or AI files accepted.)*

## Become a Marketplace Partner

If you're interested in becoming a Marketplace App Partner you can [register your App](https://www.linode.com/marketplace/app-partners/) to start a conversation with our Marketplace team.
