import logging
import os
import re
import tempfile

import pytest
from calltraces.linetrace import traceError, traceInfo, traceWarning
from calltraces import commonTraceSettings as traceSettings


@pytest.fixture
def tempLogFile() -> tempfile.NamedTemporaryFile:
    with tempfile.NamedTemporaryFile(
        suffix=".log", prefix=os.path.basename(__file__)
    ) as tf:
        tf_directory = os.path.dirname(tf.name)
        traceSettings.addOutputFileStream(tf.name)
        yield tf


def checkLog(
    regularExpression: str, tempLogFileToCheck: tempfile.NamedTemporaryFile
) -> None:

    tempLogFileToCheck.seek(0)

    logOutput = tempLogFileToCheck.read().decode(encoding="utf-8").strip()

    logRegex = re.compile(regularExpression)

    assert logRegex.match(logOutput)


def test_info_line_trace(tempLogFile) -> None:

    logContent = "A test log message for testing calltraces"

    traceInfo(logContent)

    checkLog(
        regularExpression=r"\[\d+:INFO:\d\d\] \d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d "
        + logContent,
        tempLogFileToCheck=tempLogFile,
    )


def test_warning_line_trace(tempLogFile) -> None:

    logContent = "A test log message for testing calltraces"

    traceWarning(logContent)

    checkLog(
        regularExpression=r"\[\d+:WARNING:\d\d\] \d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d "
        + logContent,
        tempLogFileToCheck=tempLogFile,
    )


def test_error_line_trace(tempLogFile) -> None:

    logContent = "A test log message for testing calltraces"

    traceError(logContent)

    checkLog(
        regularExpression=r"\[\d+:ERROR:\d\d\] \d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d "
        + logContent,
        tempLogFileToCheck=tempLogFile,
    )
