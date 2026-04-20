import json
import re
import urllib.request
from pathlib import Path


def get_latest_version(namespace: str, name: str) -> str | None:
    url = f'https://galaxy.ansible.com/api/v3/collections/{namespace}/{name}/'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'quick-deploy-dependency-update-bot'})
        with urllib.request.urlopen(req, timeout=10) as r:
            response = json.load(r)
            highest = response.get('highest_version', {})
            return highest.get('version')
    except Exception as e:
        print(f"Error fetching latest version for {namespace}.{name}: {e}")
        return None


def get_current_versions(yaml_file: Path) -> dict[str, str]:
    current_versions = {}
    content = yaml_file.read_text().splitlines()
    current_name = None
    for line in content:
        name_match = re.search(r'-\s+name:\s+([a-zA-Z0-9_.]+)', line)
        if name_match:
            current_name = name_match.group(1)
            continue
        if current_name:
            version_match = re.search(r'version:\s+[\'"]?([0-9a-zA-Z.-]+)[\'"]?', line)
            if version_match:
                current_versions[current_name] = version_match.group(1)
                current_name = None
    return current_versions


def main():
    print('Getting list of apps collections files...')
    repo_root = Path(__file__).resolve().parent.parent.parent
    collections_files = sorted((repo_root / 'apps').rglob('collections.yml'))

    print('Getting unique list of collections...')
    all_collections: set[str] = set()
    for file in collections_files:
        for collection_name in get_current_versions(file).keys():
            all_collections.add(collection_name)

    print('Getting latest collection versions from Ansible Galaxy...')
    latest_versions: dict[str, str] = {}
    for col_name in all_collections:
        if '.' in col_name:
            namespace, name = col_name.split('.', 1)
            version = get_latest_version(namespace, name)
            if version:
                latest_versions[col_name] = version

    print('Checking and updating collection versions...')
    report = []

    for f in collections_files:
        app = f.parent.name
        pinned = get_current_versions(f)
        content = f.read_text()
        changed = False
        for col_name, col_version in pinned.items():
            new_version = latest_versions.get(col_name)
            if not new_version or new_version == col_version:
                continue
            pattern = rf"(name:\s+{re.escape(col_name)}\s*\n\s*version:\s+[\"']?){re.escape(col_version)}([\"']?)"
            content, count = re.subn(pattern, rf"\g<1>{new_version}\g<2>", content)
            if count > 0:
                report.append({"app": app, "name": col_name, "old": col_version, "new": new_version})
                changed = True
        if changed:
            f.write_text(content)

    if report:
        print('Updates found. Saving to /tmp/ansible_updates.json...')
        with open('/tmp/ansible_updates.json', 'w') as f:
            json.dump(report, f)
    else:
        print('No Ansible updates found.')


if __name__ == '__main__':
    main()
