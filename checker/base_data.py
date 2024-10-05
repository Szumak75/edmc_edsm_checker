# -*- coding: utf-8 -*-
"""
  base_data.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 20.01.2024, 23:29:14
  
  Purpose: 
"""

import tkinter as tk

from inspect import currentframe
from typing import Optional

from checker.keys import CheckerKeys
from checker.jsktoolbox.libs.base_data import BData
from checker.jsktoolbox.raisetool import Raise

from checker.stars import StarsSystem
from checker.th import ThSearchSystem


class BCheckerData(BData):
    """docstring for BData."""

    @property
    def jump_system(self) -> StarsSystem:
        """jump_system property

        Returns:
            StarsSystem
        """
        if self._get_data(key=CheckerKeys.JUMP_SYSTEM, default_value=None) is None:
            self._set_data(
                key=CheckerKeys.JUMP_SYSTEM,
                value=StarsSystem(),
                set_default_type=StarsSystem,
            )
        return self._get_data(key=CheckerKeys.JUMP_SYSTEM)  # type: ignore

    @jump_system.setter
    def jump_system(self, value: Optional[StarsSystem]) -> None:
        """jump_system setter

        Arguments:
            value -- Optional[StarsSystem]
        """
        if value is None:
            self._set_data(
                key=CheckerKeys.JUMP_SYSTEM,
                value=StarsSystem(),
                set_default_type=StarsSystem,
            )
            return
        self._set_data(
            key=CheckerKeys.JUMP_SYSTEM, value=value, set_default_type=StarsSystem
        )

    @property
    def plugin_name(self) -> str:
        """plugin_name property

        Returns:
            [str] -- name of the plugin
        """
        return self._get_data(key=CheckerKeys.PLUGIN_NAME, default_value="")  # type: ignore

    @plugin_name.setter
    def plugin_name(self, value: str) -> None:
        """plugin_name setter

        Arguments:
            value -- [str] name of the plugin
        """
        self._set_data(key=CheckerKeys.PLUGIN_NAME, value=value, set_default_type=str)

    @property
    def _search(self) -> Optional[ThSearchSystem]:
        return self._get_data(key=CheckerKeys.TH_SEARCH, default_value=None)

    @_search.setter
    def _search(self, value: ThSearchSystem) -> None:
        self._set_data(
            key=CheckerKeys.TH_SEARCH, value=value, set_default_type=ThSearchSystem
        )

    @property
    def shutting_down(self) -> bool:
        return self._get_data(key=CheckerKeys.SHUTTING_DOWN, default_value=False)  # type: ignore

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        self._set_data(
            key=CheckerKeys.SHUTTING_DOWN, value=value, set_default_type=bool
        )

    @property
    def status(self) -> tk.StringVar:
        return self._get_data(key=CheckerKeys.STATUS, default_value=None)  # type: ignore

    @status.setter
    def status(self, value: tk.StringVar) -> None:
        self._set_data(
            key=CheckerKeys.STATUS, value=value, set_default_type=tk.StringVar
        )

    @property
    def version(self) -> str:
        return self._get_data(key=CheckerKeys.VERSION, default_value="")  # type: ignore

    @version.setter
    def version(self, value: str) -> None:
        self._set_data(key=CheckerKeys.VERSION, value=value, set_default_type=str)


# #[EOF]#######################################################################
