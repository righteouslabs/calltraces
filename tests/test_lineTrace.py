import logging
from calltraces.linetrace import traceInfo, traceWarning, traceError
from calltraces.traceSettings import traceSettings
from calltraces import replaceLoggingFunctions


def test_line_trace(caplog) -> None:
    with caplog.at_level(logging.INFO):
        traceInfo("Test log")
    assert 'Test losg' in caplog.text
