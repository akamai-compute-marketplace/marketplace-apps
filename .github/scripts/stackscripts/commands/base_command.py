import argparse
import logging
from abc import ABC, abstractmethod
from typing import Self

from stackscripts.clients import SlackClient
from stackscripts.config import Config
from stackscripts.reporting import SlackMessageBuilder

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    """ Base class for CLI commands """

    name: str
    help: str

    def __init__(self, config: Config) -> None:
        self.config = config
        self.slack = SlackClient(config.slack_webhook_url)
        self.messages = SlackMessageBuilder(config.run_url)

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Add command-specific CLI arguments. Override when the command takes any."""

    @classmethod
    def from_args(cls, config: Config, args: argparse.Namespace) -> Self:
        return cls(config)

    def run(self) -> int:
        try:
            return self.execute()
        except Exception as error:
            logger.exception("StackScript %s failed", self.name)
            self.slack.send(self.messages.failure(self.name, error))
            return 1

    @abstractmethod
    def execute(self) -> int:
        """Do the work; return 0 on success, 1 on failure."""

    def set_github_output(self, name: str, value: str) -> None:
        if self.config.github_output_path is None:
            logger.info("Output %s=%s", name, value)
            return
        with self.config.github_output_path.open("a", encoding="utf-8") as file:
            file.write(f"{name}={value}\n")
