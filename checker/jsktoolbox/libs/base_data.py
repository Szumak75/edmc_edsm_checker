# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-09-01

Purpose: Retain backward compatibility for legacy imports.

This module re-exports `BClasses` and `BData` while emitting a deprecation
warning that directs users to the modern `jsktoolbox.basetool` package.
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
