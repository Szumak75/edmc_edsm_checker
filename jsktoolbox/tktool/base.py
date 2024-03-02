# -*- coding: utf-8 -*-
"""
  base.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.01.2024, 13:41:50
  
  Purpose: Base classes for tkinter.
"""

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass


class TkBase(NoDynamicAttributes):
    """Base class for classess derived from Tk."""

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
