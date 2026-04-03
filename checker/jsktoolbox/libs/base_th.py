# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-11-03

Purpose: Retain backward compatibility for legacy threading imports.

The module simply re-exports items from `jsktoolbox.basetool.threads` and emits
an informative deprecation warning.
"""

import warnings


warnings.warn(
    "import jsktoolbox.libs.base_th is deprecated and will be removed in a future release,"
    "use import jsktoolbox.basetool.threads to access the contents of the module",
    DeprecationWarning,
)

from ..basetool.threads import ThBaseObject

# #[EOF]#######################################################################
