import json
import logging

from stackscripts.clients import LinodeClient
from stackscripts.commands.base_command import BaseCommand
from stackscripts.reporting import ResultTable
from stackscripts.services import DeployScriptReader, StackScriptValidator

logger = logging.getLogger(__name__)


class ValidateCommand(BaseCommand):
    """Compares all deploy scripts with their StackScripts and reports the result."""

    name = "validate"
    help = "Compare deploy scripts with StackScripts and report to Slack"

    def execute(self) -> int:
        scripts = DeployScriptReader(self.config.deployment_dir).read()
        results = StackScriptValidator(LinodeClient()).validate(scripts)
        logger.info("Validation results:\n%s", ResultTable(results).render())
        self.set_github_output("results", json.dumps([result.to_dict() for result in results]))
        self.slack.send(self.messages.validation(results))
        return 0
