import logging
from datetime import datetime
from .traceSettings import traceSettings

commonTraceSettings = traceSettings()

from .linetrace import traceInfo, traceWarning, traceError

from . import _version

__version__ = _version.get_versions()["version"]


def replaceLoggingFunctions():
    logging.info = traceInfo
    logging.warning = traceWarning
    logging.error = traceError
    logging.exception = traceError

    logging.root.info = traceInfo
    logging.root.warning = traceWarning
    logging.root.error = traceError
    logging.root.exception = traceError
