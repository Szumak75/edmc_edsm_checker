# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide lightweight base mixins shared by Tk widgets in the toolkit.

Tk modules rely on these helpers to align Tkinter widget attributes with the broader toolkit
conventions, reducing boilerplate for derived classes.
"""

from ..attribtool import NoDynamicAttributes


class TkBase(NoDynamicAttributes):
    """Common Tk widget mixin.

    Disables dynamic attribute assignment and documents the canonical Tkinter attributes expected on
    toolkit widgets.
    """

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
