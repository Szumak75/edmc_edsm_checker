# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 03.11.2023

Purpose: For compatibility reasons only.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.base_th is deprecated and will be removed in a future release,"
    "use import jsktoolbox.basetool.threads to access the contents of the module",
    DeprecationWarning,
)

from ..basetool.threads import ThBaseObject

# #[EOF]#######################################################################
