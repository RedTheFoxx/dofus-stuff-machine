"""Optimiseur de combinaisons de stuff."""

from dofus_stuff.optimize.api import OptimizeResult, format_optimize_result, optimize_stuff
from dofus_stuff.optimize.profile_input import (
    COMPACT_HELP_LINES,
    OptimizeInputError,
    OptimizeRequest,
    parse_compact_line,
    parse_optimize_request,
)

__all__ = [
    "COMPACT_HELP_LINES",
    "OptimizeInputError",
    "OptimizeRequest",
    "OptimizeResult",
    "format_optimize_result",
    "optimize_stuff",
    "parse_compact_line",
    "parse_optimize_request",
]
