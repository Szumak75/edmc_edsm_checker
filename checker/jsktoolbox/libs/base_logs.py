# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 04.09.2023

Purpose: For compatibility reasons only.
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
