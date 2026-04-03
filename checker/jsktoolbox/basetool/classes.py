# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Deliver lightweight base classes with runtime metadata helpers.

Provides mixins that expose convenience properties for class and method names,
supporting logging contexts and debugging aids in derived classes.
"""

from inspect import currentframe
from typing import Optional
from types import FrameType

from ..attribtool import NoDynamicAttributes


class BClasses(NoDynamicAttributes):
    """Common base class exposing class and frame metadata helpers."""

    @property
    def _c_name(self) -> str:
        """Return the name of the current class.

        ### Returns:
        [str] - Qualified name without module prefix.
        """
        return self.__class__.__name__

    @property
    def _f_name(self) -> str:
        """Return the caller method name using the current frame.

        ### Returns:
        [str] - Name of the calling method or empty string if unavailable.
        """
        tmp: Optional[FrameType] = currentframe()
        if tmp is not None:
            frame: Optional[FrameType] = tmp.f_back
            if frame is not None:
                method_name: str = frame.f_code.co_name
                return method_name
        return ""


# #[EOF]#######################################################################
