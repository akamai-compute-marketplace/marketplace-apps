import requests

from stackscripts.exceptions import LinodeApiError, StackScriptNotFoundError


class LinodeClient:
    """ Reads and updates StackScripts through the Linode API """

    API_URL = "https://api.linode.com/v4/linode/stackscripts"
    TIMEOUT_SECONDS = 30

    def __init__(self, token: str | None = None) -> None:
        self._session = requests.Session()
        if token:
            self._session.headers["Authorization"] = f"Bearer {token}"

    def get_script(self, stackscript_id: int) -> str:
        return self._request("GET", stackscript_id)["script"]

    def update_script(self, stackscript_id: int, script: str) -> str:
        return self._request("PUT", stackscript_id, json={"script": script})["script"]

    def _request(self, method: str, stackscript_id: int, **kwargs) -> dict:
        url = f"{self.API_URL}/{stackscript_id}"
        try:
            response = self._session.request(method, url, timeout=self.TIMEOUT_SECONDS, **kwargs)
        except requests.RequestException as error:
            raise LinodeApiError(f"{method} {url} failed: {error}") from error

        if response.status_code == 404:
            raise StackScriptNotFoundError(f"StackScript {stackscript_id} does not exist")
        if not response.ok:
            raise LinodeApiError(f"{method} returned {response.status_code}: {response.text}")
        return response.json()
