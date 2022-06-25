from functools import update_wrapper, wraps

import commonTraceSettings
from functiontrace import __functionDecorator__
from linetrace import isDebuggerAttached


def __classDecorator__(cls: any, debug: bool = False):

    if not commonTraceSettings.enabled:
        return cls

    for funcname in dir(cls):
        # Skip private members
        if funcname.startswith("_"):
            continue

        # Get class attributes and check if it is a function
        func = getattr(cls, funcname)
        if not callable(func):
            continue

        # wrap function with calltraces decorator
        wrapped = __functionDecorator__(func=func, debug=debug)

        # Attach the new calltraces function in place of the old function
        setattr(cls, funcname, wrapped)
    return cls


def calltraces(debugOnly: bool = False, **kwargs):
    """
    Trace all object function calls including input and output
    """

    debug = debugOnly and isDebuggerAttached()

    return lambda cls: __classDecorator__(cls=cls, debug=debug)
