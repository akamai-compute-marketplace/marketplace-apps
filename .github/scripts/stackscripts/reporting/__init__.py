"""Turns results into human-readable output (log tables, Slack messages)."""

from stackscripts.reporting.result_table import ResultTable
from stackscripts.reporting.slack_message_builder import SlackMessageBuilder

__all__ = ["ResultTable", "SlackMessageBuilder"]
