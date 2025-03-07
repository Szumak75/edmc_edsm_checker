# -*- coding: utf-8 -*-
"""
layout.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 13:48:01

Purpose: Tkinter geometry managers keys helper classes.
"""

import tkinter as tk

from ..attribtool import ReadOnlyClass


class Pack(object, metaclass=ReadOnlyClass):
    """Pack geometry manager.

    https://www.pythontutorial.net/tkinter/tkinter-pack/
    """

    class Anchor(object, metaclass=ReadOnlyClass):
        """The anchor parameter allows you to anchor the widget to the edge of the allocated space."""

        CENTER = tk.CENTER
        E = tk.E
        N = tk.N
        NE = tk.NE
        NW = tk.NW
        S = tk.S
        SE = tk.SE
        SW = tk.SW
        W = tk.W

    class Side(object, metaclass=ReadOnlyClass):
        """The side parameter determines the direction of the widgets in the pack layout."""

        BOTTOM = tk.BOTTOM
        LEFT = tk.LEFT
        RIGHT = tk.RIGHT
        TOP = tk.TOP

    class Fill(object, metaclass=ReadOnlyClass):
        """The fill determines if a widget will occupy the available space."""

        BOTH = tk.BOTH
        NONE = tk.NONE
        X = tk.X
        Y = tk.Y


class Grid(object, metaclass=ReadOnlyClass):
    """Grid geometry manager.

    https://www.pythontutorial.net/tkinter/tkinter-grid/
    """

    class Sticky(object, metaclass=ReadOnlyClass):
        """The sticky option specifies which edge of the cell the widget should stick to."""

        CENTER = tk.CENTER
        E = tk.E
        N = tk.N
        NE = tk.NE
        NW = tk.NW
        S = tk.S
        SE = tk.SE
        SW = tk.SW
        W = tk.W


class Place(object, metaclass=ReadOnlyClass):
    """Place geometry manager.

    https://www.pythontutorial.net/tkinter/tkinter-place/
    """

    class Anchor(object, metaclass=ReadOnlyClass):
        """The anchor parameter determines which part of the widget is positioned at the given coordinates."""

        CENTER = tk.CENTER
        E = tk.E
        N = tk.N
        NE = tk.NE
        NW = tk.NW
        S = tk.S
        SE = tk.SE
        SW = tk.SW
        W = tk.W


# #[EOF]#######################################################################
