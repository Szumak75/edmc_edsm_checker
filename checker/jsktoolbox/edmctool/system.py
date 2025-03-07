# -*- coding: utf-8 -*-
"""
system.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 7.10.2024, 14:25:00

Purpose: EDMC plugins system classes.
"""

import os

from ..basetool.data import BData
from ..systemtool import Env
from ..attribtool import ReadOnlyClass


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    DIR: str = "__dir__"


class Directory(BData):
    """Container class to store the directory path."""

    def is_directory(self, path_string: str) -> bool:
        """Check if the given string is a directory.

        path_string: str        path string to check
        return:      bool       True, if exists and is directory,
                                False in the other case.
        """
        return os.path.exists(path_string) and os.path.isdir(path_string)

    @property
    def dir(self) -> str:
        """Property that returns directory string."""
        return self._get_data(key=_Keys.DIR, default_value="")  # type: ignore

    @dir.setter
    def dir(self, arg: str) -> None:
        """Setter for directory string.

        given path must exists.
        """
        if self.is_directory(arg):
            self._set_data(key=_Keys.DIR, value=arg, set_default_type=str)


class EnvLocal(Env):
    """Environmental class."""

    def __init__(self) -> None:
        """Initialize Env class."""
        super().__init__()

    def check_dir(self, directory: str) -> str:
        """Check if dir exists, return dir or else HOME."""
        if not Directory().is_directory(directory):
            return self.home
        return directory

    @property
    def plugin_dir(self) -> str:
        """Return plugin dir path."""
        return f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))}"


# #[EOF]#######################################################################
