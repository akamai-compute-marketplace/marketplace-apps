import logging

from stackscripts.clients import LinodeClient
from stackscripts.exceptions import LinodeApiError, StackScriptNotFoundError
from stackscripts.models import DeployScript, Result, Status

logger = logging.getLogger(__name__)


class StackScriptValidator:
    """Compares deploy scripts with the content of their StackScripts."""

    def __init__(self, linode_client: LinodeClient) -> None:
        self._linode = linode_client

    def validate(self, scripts: list[DeployScript]) -> list[Result]:
        logger.info("Validating %d deploy scripts", len(scripts))
        return [self.check(script) for script in scripts]

    def check(self, script: DeployScript) -> Result:
        if script.stackscript_id is None:
            return Result(script.app, None, Status.MISSING_ID, "No '# STACKSCRIPT_ID:' header")

        try:
            remote_script = self._linode.get_script(script.stackscript_id)
        except StackScriptNotFoundError as error:
            return Result(script.app, script.stackscript_id, Status.NOT_FOUND, str(error))
        except LinodeApiError as error:
            return Result(script.app, script.stackscript_id, Status.ERROR, str(error))

        status = Status.MATCH if remote_script == script.content else Status.MISMATCH
        return Result(script.app, script.stackscript_id, status)
