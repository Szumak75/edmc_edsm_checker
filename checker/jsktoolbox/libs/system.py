# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-09-05

Purpose: Retain backward compatibility for legacy system-tool imports.

The module re-exports objects from `jsktoolbox.systemtool` and notifies callers
about the preferred import path.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.system is deprecated and will be removed in a future release,"
    "use import jsktoolbox.systemtool to access the contents of the module",
    DeprecationWarning,
)

from jsktoolbox.systemtool import Env, CommandLineParser, PathChecker

# #[EOF]#######################################################################
