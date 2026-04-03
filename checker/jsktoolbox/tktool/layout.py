# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide named accessors for Tk geometry manager constants (pack, grid, place).

This module centralises the most common anchor, side, fill, and sticky options so that GUI code can
refer to Tk enumerations through read-only wrappers instead of raw tkinter symbols.
"""

import tkinter as tk

from ..attribtool import ReadOnlyClass


class Pack(object, metaclass=ReadOnlyClass):
    """Pack geometry manager constants.

    Groups anchors, sides, and fill modes exposed by ``tk.pack`` for consistent, read-only access.
    """

    class Anchor(object, metaclass=ReadOnlyClass):
        """Anchor values for pack placement.

        Mirrors the ``anchor`` parameter accepted by the pack geometry manager.
        """

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
        """Side values for pack placement.

        Indicates which edge of the container a widget should hug when packed.
        """

        BOTTOM = tk.BOTTOM
        LEFT = tk.LEFT
        RIGHT = tk.RIGHT
        TOP = tk.TOP

    class Fill(object, metaclass=ReadOnlyClass):
        """Fill modes for pack placement.

        Controls how a widget expands along the horizontal and vertical axes.
        """

        BOTH = tk.BOTH
        NONE = tk.NONE
        X = tk.X
        Y = tk.Y


class Grid(object, metaclass=ReadOnlyClass):
    """Grid geometry manager constants.

    Aggregates sticky options from ``tk.grid`` to keep UI layout code expressive.
    """

    class Sticky(object, metaclass=ReadOnlyClass):
        """Sticky values for grid placement.

        Specifies which cell edges a widget should adhere to when the cell grows.
        """

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
    """Place geometry manager constants.

    Wraps commonly used ``tk.place`` anchor options inside a read-only namespace.
    """

    class Anchor(object, metaclass=ReadOnlyClass):
        """Anchor values for absolute placement.

        Describes which widget point maps to the x/y coordinates supplied to ``place``.
        """

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
