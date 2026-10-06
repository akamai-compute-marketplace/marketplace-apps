class NewrelicService:
    """
    Actions for the newrelic add-on over SSH.
    The add-on only installs the CLI and a first-login script; the agent is installed once a user logs in and enters keys.
    """

    CLI = "/usr/local/bin/newrelic"
    LOGIN_SCRIPT = "/etc/profile.d/newrelic.sh"
    ADDONS_LOG = "/var/log/marketplace_addons.log"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def file_mode_owner(self, path):
        out, _, _ = self._run(f"stat -c '%a %U:%G' {path}")
        return out

    def cli_version(self):
        out, err, code = self._run(f"{self.CLI} version")
        return code, out or err

    def login_script_syntax_error(self):
        _, err, code = self._run(f"bash -n {self.LOGIN_SCRIPT}")
        return err if code != 0 else None

    def login_script_completed(self):
        _, _, code = self._run(f"grep -q 'New Relic installation completed' {self.ADDONS_LOG}")
        return code == 0
