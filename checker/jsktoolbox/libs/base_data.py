# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 01.09.2023

Purpose: For compatibility reasons only.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.base_data is deprecated and will be removed in a future release,"
    "use import jsktoolbox.basetool.data to access the contents of the module",
    DeprecationWarning,
)

from ..basetool.classes import BClasses
from ..basetool.data import BData


# #[EOF]#######################################################################
