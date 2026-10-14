
class StackScriptJobError(Exception):
    """Base class for all job errors."""


class ConfigError(StackScriptJobError):
    """Required configuration is missing."""


class LinodeApiError(StackScriptJobError):
    """The Linode API request failed."""


class StackScriptNotFoundError(LinodeApiError):
    """The StackScript ID does not exist."""
