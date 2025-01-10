import pytest
import pytest_html
from pytest_metadata.plugin import metadata_key

# https://pytest-html.readthedocs.io/en/latest/user_guide.html#enhancing-reports

# Report Title
def pytest_html_report_title(report):
    report.title = "My very own title!"

# Environment
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    session.config.stash[metadata_key]["foo"] = "bar"

# Additional summary information
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend(["<p>foo: bar</p>"])

# Modifying the results table
def pytest_html_results_table_header(cells):
    cells.insert(2, '<th class="sortable" data-column-type="input">Input</th>')
    cells.insert(3, '<th class="sortable" data-column-type="expected">Expected</th>')
    cells.insert(4, '<th class="sortable" data-column-type="output">Output</th>')

def pytest_html_results_table_row(report, cells):
    user_properties = dict(report.user_properties)
    cells.insert(2, '<td class="col-input">{}</td>'.format(user_properties.get("input", "N/A")))
    cells.insert(3, '<td class="col-expected">{}</td>'.format(user_properties.get("expected", "N/A")))
    cells.insert(4, '<td class="col-output">{}</td>'.format(user_properties.get("output", "N/A")))

# Extra content
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url("http://www.example.com/"))
        # extras.append(pytest_html.extras.text("some string", name="Different title"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extras.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extras = extras
        # it is possible to include function doc, funcargs in report
        report.description = str(item.function.__doc__)