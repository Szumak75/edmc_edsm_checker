# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: Class for creating and processes config files.
"""

from inspect import currentframe
from typing import List, Optional
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import PathChecker


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    FILE = "__file__"


class FileProcessor(BData, NoDynamicAttributes):
    """FileProcessor class."""

    def __init__(self) -> None:
        """Constructor."""

    @property
    def file(self) -> Optional[str]:
        """Return config file path."""
        if _Keys.FILE not in self._data:
            self._data[_Keys.FILE] = None
        if isinstance(self._data[_Keys.FILE], PathChecker):
            return self._data[_Keys.FILE].path
        return self._data[_Keys.FILE]

    @file.setter
    def file(self, path: str) -> None:
        """Set file name."""
        self._data[_Keys.FILE] = PathChecker(path)

    @property
    def file_exists(self) -> bool:
        """Check if the file exists and is a file."""
        obj: PathChecker = self._data[_Keys.FILE]
        return obj.exists and (obj.is_file or obj.is_symlink) and not obj.is_dir

    def file_create(self) -> bool:
        """Try to create file."""
        if self.file_exists:
            return True
        obj: PathChecker = self._data[_Keys.FILE]
        if obj.exists and obj.is_dir:
            raise Raise.error(
                f"Given path: {obj.path} exists and is a directory.",
                OSError,
                self._c_name,
                currentframe(),
            )
        return obj.create()

    def read(self) -> str:
        """Try to read config file."""
        out: str = ""
        if self.file_exists:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "r") as file:
                    out = file.read()
        return out

    def readlines(self) -> List[str]:
        """Try to read config file and create list of strings."""
        out: List[str] = []
        if self.file_exists:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "r") as file:
                    tmp = file.readlines()
                    for line in tmp:
                        if line.find("<end of section") > 0:
                            continue
                        out.append(line.strip())
        return out

    def write(self, data: str) -> None:
        """Try to write data to config file."""
        test: bool = self.file_exists
        if not test:
            test = self.file_create()
        if test:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "w") as file:
                    file.write(data)


# #[EOF]#######################################################################
