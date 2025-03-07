# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 05.09.2023

Purpose: For compatibility reasons only.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.system is deprecated and will be removed in a future release,"
    "use import jsktoolbox.systemtool to access the contents of the module",
    DeprecationWarning,
)

from jsktoolbox.systemtool import Env, CommandLineParser, PathChecker

# #[EOF]#######################################################################
