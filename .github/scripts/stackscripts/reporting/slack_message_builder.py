from stackscripts.models import Result, Status
from stackscripts.reporting.result_table import ResultTable


class SlackMessageBuilder:
    """Builds Slack Block Kit messages for each stage of the job."""

    MAX_TABLE_LENGTH = 2900

    def __init__(self, run_url: str) -> None:
        self._run_url = run_url

    def validation(self, results: list[Result]) -> dict:
        mismatches = [result for result in results if result.status is Status.MISMATCH]
        errors = [result for result in results if result.status.needs_attention and result.status is not Status.MISMATCH]

        if not mismatches and not errors:
            return self._message(f"✅ All {len(results)} StackScripts are in sync")

        blocks = []
        if errors:
            blocks.append(self._section("*Manual fix required:*"))
            blocks.append(self._table(errors))
        if mismatches:
            blocks.append(self._section("*Can be fixed by the job:*"))
            blocks.append(self._table(mismatches))
            blocks.append(self._section("*Do you want to fix mismatched StackScripts?*"))
            blocks.append(self._button("Review & Approve"))
        return self._message(f"⚠️ StackScripts: {len(mismatches)} mismatches, {len(errors)} errors", blocks)

    def update(self, results: list[Result]) -> dict:
        updated = [result for result in results if result.status is Status.UPDATED]
        failed = [result for result in results if result.status.needs_attention]

        icon = "❌" if failed else "✅"
        title = f"{icon} StackScript update: {len(updated)} updated, {len(failed)} failed"
        return self._message(title, [self._table(results)])

    def failure(self, command: str, error: Exception) -> dict:
        return self._message(f"❌ StackScript {command} crashed", [self._section(f"```\n{error}\n```")])

    def _message(self, title: str, blocks: list[dict] | None = None) -> dict:
        header = {"type": "header", "text": {"type": "plain_text", "text": title}}
        run_link = {"type": "context", "elements": [{"type": "mrkdwn", "text": f"<{self._run_url}|View workflow run>"}]}
        return {"text": title, "blocks": [header, *(blocks or []), run_link]}

    def _table(self, results: list[Result]) -> dict:
        table = ResultTable(results).render(max_length=self.MAX_TABLE_LENGTH)
        return self._section(f"```\n{table}\n```")

    def _button(self, text: str) -> dict:
        button = {"type": "button", "text": {"type": "plain_text", "text": text}, "style": "primary", "url": self._run_url}
        return {"type": "actions", "elements": [button]}

    @staticmethod
    def _section(text: str) -> dict:
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}
