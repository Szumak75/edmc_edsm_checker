# -*- coding: utf-8 -*-
"""
classes.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 10:23:31

Purpose:
"""

from inspect import currentframe
from typing import Optional
from types import FrameType

from ..attribtool import NoDynamicAttributes


class BClasses(NoDynamicAttributes):
    """Base class for projects."""

    @property
    def _c_name(self) -> str:
        """Return class name."""
        return self.__class__.__name__

    @property
    def _f_name(self) -> str:
        """Return current method name."""
        tmp: Optional[FrameType] = currentframe()
        if tmp is not None:
            frame: Optional[FrameType] = tmp.f_back
            if frame is not None:
                method_name: str = frame.f_code.co_name
                return method_name
        return ""


# #[EOF]#######################################################################
