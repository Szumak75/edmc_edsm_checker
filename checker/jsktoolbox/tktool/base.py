# -*- coding: utf-8 -*-
"""
base.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 13:41:50

Purpose: Base classes for tkinter.
"""

from ..attribtool import NoDynamicAttributes


class TkBase(NoDynamicAttributes):
    """Base class for classes derived from Tk."""

    _name = None
    _tkloaded = None
    _w = None
    _windowingsystem_cached = None
    child = None
    children = None
    master = None
    tk = None
    widgetName = None


# #[EOF]#######################################################################
