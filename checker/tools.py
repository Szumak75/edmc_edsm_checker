# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: tools classes.
"""

from typing import Any

from checker.jsktoolbox.attribtool import NoDynamicAttributes



class Numbers(NoDynamicAttributes):
    """Numbers tool."""

    def is_float(self, element: Any) -> bool:
        """Check, if element is proper float variable."""
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False


# #[EOF]#######################################################################
