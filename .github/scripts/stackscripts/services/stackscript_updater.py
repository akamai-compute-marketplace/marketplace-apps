import logging

from stackscripts.clients import LinodeClient
from stackscripts.exceptions import LinodeApiError
from stackscripts.models import DeployScript, Result, Status
from stackscripts.services.stackscript_validator import StackScriptValidator

logger = logging.getLogger(__name__)


class StackScriptUpdater:
    """ Pushes deploy scripts to StackScripts whose content differs """

    def __init__(self, linode_client: LinodeClient, validator: StackScriptValidator) -> None:
        self._linode = linode_client
        self._validator = validator

    def update(self, scripts: list[DeployScript]) -> list[Result]:
        logger.info("Updating %d StackScripts", len(scripts))
        return [self._update_one(script) for script in scripts]

    def _update_one(self, script: DeployScript) -> Result:
        result = self._validator.check(script)
        if result.status is not Status.MISMATCH:
            return result

        try:
            new_content = self._linode.update_script(script.stackscript_id, script.content)
        except LinodeApiError as error:
            return Result(script.app, script.stackscript_id, Status.FAILED, str(error))

        if new_content != script.content:
            return Result(script.app, script.stackscript_id, Status.FAILED, "Content still differs after update")
        return Result(script.app, script.stackscript_id, Status.UPDATED)
