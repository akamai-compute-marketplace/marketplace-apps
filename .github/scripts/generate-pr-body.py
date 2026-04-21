import json
import os
from pathlib import Path


def generate_markdown_table(updates: list[dict], dependency_label: str) -> str:
    lines = [
        f'| App | {dependency_label} | Current | Latest |',
        '|---|---|---|---|'
    ]
    for u in updates:
        lines.append(f"| `{u['app']}` | `{u['name']}` | `{u['old']}` | `{u['new']}` |")
    return '\n'.join(lines)


def main():
    print("Gathering update reports...")
    py_file = Path('/tmp/python_updates.json')
    ansible_file = Path('/tmp/ansible_updates.json')

    pr_intro = (
        "🤖 **Automated Dependency Updates**\n\n"
        "This Pull Request was generated automatically by Dependency Updates workflow "
        "It checks for the latest available versions of our Python packages and Ansible collections, "
        "and safely bumps the pinned versions in our configuration files.\n\n"
        "Please review the version changes below and run deployment before merging.\n\n"
        "---"
    )

    body_parts = [pr_intro]

    if py_file.exists():
        py_updates = json.loads(py_file.read_text())
        body_parts.append('### 🐍 Python Updates\n\n' + generate_markdown_table(py_updates, 'Package'))

    if ansible_file.exists():
        ansible_updates = json.loads(ansible_file.read_text())
        body_parts.append('### ⚙️ Ansible Updates\n\n' + generate_markdown_table(ansible_updates, 'Collection'))

    output_file = os.environ.get('GITHUB_OUTPUT', '/dev/null')

    if len(body_parts) > 1:
        print("Writing /tmp/pr_body.md...")
        Path('/tmp/pr_body.md').write_text('\n\n'.join(body_parts))

        with open(output_file, 'a') as f:
            f.write('any_updates=true\n')
    else:
        print("No updates across any ecosystem.")
        with open(output_file, 'a') as f:
            f.write('any_updates=false\n')


if __name__ == '__main__':
    main()