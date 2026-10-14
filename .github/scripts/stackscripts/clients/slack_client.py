import logging

import requests

logger = logging.getLogger(__name__)


class SlackClient:
    """ Posts messages to a Slack incoming webhook """

    TIMEOUT_SECONDS = 30

    def __init__(self, webhook_url: str) -> None:
        self._webhook_url = webhook_url

    def send(self, message: dict) -> None:
        response = requests.post(self._webhook_url, json=message, timeout=self.TIMEOUT_SECONDS)
        response.raise_for_status()
        logger.info("Slack message sent: %s", message["text"])
