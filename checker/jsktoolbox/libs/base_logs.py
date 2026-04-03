# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-09-04

Purpose: Retain backward compatibility for legacy logging imports.

This module re-exports logging helpers from the newer `jsktoolbox.basetool`
and `jsktoolbox.logstool` packages while warning about deprecation.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.base_logs is deprecated and will be removed in a future release,"
    "use import jsktoolbox.basetool.logs to access the contents of the module",
    DeprecationWarning,
)

from ..logstool.queue import LoggerQueue
from ..logstool.keys import LogKeys, LogsLevelKeys, SysLogKeys
from ..basetool.logs import (
    BLogFormatter,
    BLoggerEngine,
    BLoggerQueue,
)


# #[EOF]#######################################################################
