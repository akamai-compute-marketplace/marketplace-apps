from stackscripts.models import Result


class ResultTable:
    """Renders results as a plain-text table with aligned columns."""

    HEADERS = ("App", "StackScript ID", "Status", "Detail")
    MAX_DETAIL_LENGTH = 60

    def __init__(self, results: list[Result]) -> None:
        self._results = results

    def render(self, max_length: int | None = None) -> str:
        rows = [self.HEADERS, *(self._to_row(result) for result in self._results)]
        widths = [max(len(row[column]) for row in rows) for column in range(len(self.HEADERS))]

        lines = [self._render_row(row, widths) for row in rows]
        lines.insert(1, "-+-".join("-" * width for width in widths))
        table = "\n".join(lines)

        if max_length and len(table) > max_length:
            table = table[:max_length].rsplit("\n", 1)[0] + "\n... (truncated, see the workflow run log)"
        return table

    def _to_row(self, result: Result) -> tuple[str, ...]:
        stackscript_id = str(result.stackscript_id) if result.stackscript_id else "-"
        return result.app, stackscript_id, result.status, result.detail[: self.MAX_DETAIL_LENGTH]

    @staticmethod
    def _render_row(row: tuple[str, ...], widths: list[int]) -> str:
        return " | ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip()
