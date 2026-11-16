import time

WEBAPPS = "/opt/tomcat/webapps"


class ApacheTomcatService:
    """
    Tomcat actions: systemd/process checks and WAR deployment over SSH, page fetches over public HTTPS.
    """

    def __init__(self, remote_exec, http_session=None, base_url=None):
        self._run = remote_exec
        self._http = http_session
        self._base_url = base_url

    def unit_active(self):
        out, _, _ = self._run("systemctl is-active tomcat")
        return out

    def process_user(self):
        out, _, _ = self._run("ps -o user:32= -C java")
        return out

    def get(self, path, timeout=30):
        return self._http.get(f"{self._base_url}{path}", timeout=timeout)

    def deploy_war(self, source_war, name):
        return self._run(f"install -o tomcat -g tomcat -m 0640 {WEBAPPS}/{source_war} {WEBAPPS}/{name}.war")

    def wait_until_served(self, path, timeout=60, interval=3):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.get(path).status_code == 200:
                return True
            time.sleep(interval)
        return False
