# Regression Tests

End-to-end regression tests for Linode Marketplace apps, built with [pytest](https://pytest.org) and [Playwright](https://playwright.dev/python/).

---

## Project Structure

```
regression_tests/
├── apps/                        # Test suites
│   ├── linode-marketplace-antmedia/
│   │   ├── conftest.py          # App-specific fixtures
│   │   └── test_scenarios.py    # Test scenarios
│   └── linode-marketplace-antmedia-community/
│       ├── conftest.py
│       └── test_scenarios.py
├── pages/                       # Page Object Model classes
│   ├── base_page.py             # Shared BasePage
│   ├── antmedia/
│   │   ├── login_page.py
│   │   ├── dashboard_page.py
│   │   └── stream_page.py
│   └── antmedia_community/
├── utils/
│   ├── ssh.py                   # SSH helpers
├── conftest.py                  # Session-wide fixtures
├── pytest.ini                   # pytest configuration
└── requirements.txt             # Python dependencies
```

---

## Requirements

- Python 3.10+
- A deployed Linode instance running the target Marketplace app

Install dependencies:

```bash
pip install -r tests/regression_tests/requirements.txt
playwright install chromium
```

---

## Environment Variables

| Variable           | Description                                |
|--------------------|--------------------------------------------|
| `LINODE_IPV4`      | Public IPv4 address of the deployed Linode |
| `LINODE_ROOT_PASS` | Root password for SSH access               |
| `LINODE_ROOT_USER` | SSH username (defaults to `root`)          |

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests for a specific app:

```bash
pytest apps/linode-marketplace-antmedia/
```

Run a single test:

```bash
pytest apps/linode-marketplace-antmedia/test_scenarios.py::test_antmedia_start_stream
```

Generate an HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```

Set a custom reports directory:

```bash
REGRESSION_REPORTS_DIR=my_reports pytest --html=my_reports/report.html --self-contained-html
```

---

### Page Object Model

Each app has a dedicated set of page classes under `pages/`. Pages extend `BasePage` and expose locators and actions as methods, keeping test scenarios free of raw selectors.

### Screenshot on Failure

The `pytest_runtest_makereport` hook in the root `conftest.py` automatically captures a full-page screenshot on test failure and embeds it as a Base64 image in the HTML report.

