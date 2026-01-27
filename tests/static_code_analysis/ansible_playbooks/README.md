# Ansible Playbook Linting Utilities

This folder contains scripts and configuration files to automatically **lint** Ansible playbooks and roles (`.yml`/`.yaml`) files.

- **ansible-lint** is a _linter_ specifically for Ansible content. It checks playbooks, roles, and tasks for errors, best-practice violations, deprecated behavior, and style issues.

## Requirements

Install the required tool:

- [ansible-lint](https://docs.ansible.com/projects/lint/installing/)

## How to Use

**Running the script:**

- To lint a specific file or role directory:
  ```sh
  ./check_ansible_playbooks.sh path/to/playbook.yml
  ```
  or
  ```sh
  ./check_ansible_playbooks.sh path/to/role/
  ```

## Configuration

- **ansible-lint** reads its rules and configuration from a file named `.ansible-lint.yaml` in this folder.

For more details on the tool’s configuration options, see:

- ansible-lint: [https://docs.ansible.com/projects/lint/configuring/](https://docs.ansible.com/projects/lint/configuring/)

---