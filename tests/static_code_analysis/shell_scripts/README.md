# Shell Script Formatting & Linting Utility

This folder contains a utility script for **formatting** and **linting** shell scripts (`.sh`).

- **shfmt** is an automatic _formatter_ for shell scripts. It enforces a consistent indentation and layout style, making scripts easier to read and maintain. It updates files to follow formatting conventions such as indentation size, alignment, and spacing.

- **ShellCheck** is a _linter_ and static analyzer for shell scripts. It detects syntax errors, common bugs, unsafe code, deprecated syntax, and provides suggestions for improving script reliability and portability. It reports problems before the scripts are run.

---

## Requirements

- [shfmt](https://github.com/mvdan/sh#shfmt) installed and available in your `PATH`
- [ShellCheck](https://github.com/koalaman/shellcheck#installing) installed and available in your `PATH`

---

## How to use

**Format and lint all shell scripts recursively:**
```sh
./check_shell_scripts.sh all
```

**Format and lint a specific shell script:**
```sh
./check_shell_scripts.sh path/to/script.sh
```

---

## Configuration

Edit the `SHELLCHECK_OPTS` variable at the top of the script to add or remove exclusions or change severity:

```bash
SHELLCHECK_OPTS="--exclude=SC1091,SC2154 --severity=warning"
```

- `--exclude` disables selected ShellCheck rules (e.g. SC1091, SC2154).
- `--severity` controls the minimum level of issues reported:
    - `error` – Only show errors, suppress warnings, info, and style.
    - `warning` – Show errors and warnings
    - `info` – Show errors, warnings, and info messages.
    - `style` – Show errors, warnings, info, and style suggestions.

---

## References

- [shfmt documentation](https://github.com/mvdan/sh#shfmt)
- [ShellCheck Wiki](https://github.com/koalaman/shellcheck/wiki)

---