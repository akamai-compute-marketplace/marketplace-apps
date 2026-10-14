import argparse
import json
import logging
from typing import Self

from stackscripts.clients import LinodeClient
from stackscripts.commands.base_command import BaseCommand
from stackscripts.config import Config
from stackscripts.exceptions import ConfigError
from stackscripts.models import Result, Status
from stackscripts.reporting import ResultTable
from stackscripts.services import DeployScriptReader, StackScriptUpdater, StackScriptValidator

logger = logging.getLogger(__name__)


class UpdateCommand(BaseCommand):
    """Updates the StackScripts of the given apps from their deploy scripts. Runs after approval."""

    name = "update"
    help = "Update StackScripts from deploy scripts"

    def __init__(self, config: Config, validation_results: list[Result]) -> None:
        super().__init__(config)
        self.validation_results = validation_results

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--results", required=True, help="Validation results (JSON) from the validate command")

    @classmethod
    def from_args(cls, config: Config, args: argparse.Namespace) -> Self:
        results = [Result.from_dict(item) for item in json.loads(args.results)]
        return cls(config, results)

    def execute(self) -> int:
        mismatched_apps = [result.app for result in self.validation_results if result.status is Status.MISMATCH]
        logger.info("Mismatched apps to update: %s", ", ".join(mismatched_apps))

        linode = LinodeClient(self.config.stackscript_api_token)
        updater = StackScriptUpdater(linode, StackScriptValidator(linode))

        scripts = DeployScriptReader(self.config.deployment_dir).read(mismatched_apps)
        results = updater.update(scripts)
        logger.info("Update results:\n%s", ResultTable(results).render())

        self.slack.send(self.messages.update(results))
        return 1 if any(result.status.needs_attention for result in results) else 0
