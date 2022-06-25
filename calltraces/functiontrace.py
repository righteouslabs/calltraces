# Original: https://stackoverflow.com/a/63644860/9168936

from datetime import datetime
from functools import update_wrapper
import logging

from colorama import Back, Fore, Style
import commonTraceSettings
from linetrace import isDebuggerAttached, traceInfo


def __functionDecorator__(func: any, debug: bool = False):

    funcFullName = f"{func.__module__}.{func.__name__}"

    if (
        not commonTraceSettings.enabled
        or funcFullName in commonTraceSettings.ignoreSymbols
        or func.__name__.startswith("_")
    ):
        return func

    logLevel = logging.DEBUG if debug else logging.INFO

    # we define a wrapper function. This will execute all additional code
    # before and after the "real" function.

    def __traceWrapper__(*args, **kwargs):

        output = None
        try:
            traceInfo(f"{funcFullName} Started Function", logLevel=logLevel)
            if commonTraceSettings.printArguments:
                traceInfo(f"{funcFullName} args: {args}", logLevel=logLevel)
                traceInfo(f"{funcFullName} kwargs: {kwargs}", logLevel=logLevel)

            # Function call
            commonTraceSettings.traceStackDepth = (
                commonTraceSettings.traceStackDepth + 1
            )
            output = func(*args, **kwargs)
            return output
        finally:
            commonTraceSettings.traceStackDepth = (
                commonTraceSettings.traceStackDepth - 1
            )
            traceInfo(f"{funcFullName} Ended Function", logLevel=logLevel)
            if commonTraceSettings.printArguments:
                traceInfo(f"{funcFullName} args: {args}", logLevel=logLevel)
                traceInfo(f"{funcFullName} kwargs: {kwargs}", logLevel=logLevel)
            if commonTraceSettings.printOutputs:
                traceInfo(f"{funcFullName} output: {output}", logLevel=logLevel)

    # Use "update_wrapper" to keep docstrings and other function metadata
    # intact
    update_wrapper(__traceWrapper__, func)

    commonTraceSettings.ignoreSymbols.append(funcFullName)

    # We can now return the wrapped function
    return __traceWrapper__


def functiontrace(debugOnly: bool = False, **kwargs):
    """
    Trace function calls including input and output
    """

    debug = debugOnly and isDebuggerAttached()

    return lambda func: __functionDecorator__(func=func, debug=debug)
