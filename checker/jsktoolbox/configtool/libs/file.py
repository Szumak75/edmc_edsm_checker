# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose: Class for creating and processes config files.
"""

from inspect import currentframe
from typing import List, Optional

from ...attribtool import NoDynamicAttributes, ReadOnlyClass
from ...raisetool import Raise
from ...basetool.data import BData
from ...systemtool import PathChecker


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    FILE: str = "__file__"


class FileProcessor(BData, NoDynamicAttributes):
    """Handle filesystem interactions for configuration files.

    ### Purpose:
    Offers helpers to validate paths, read, and persist config data.
    """

    def __init__(self) -> None:
        """Initialise FileProcessor instance.

        The constructor does not perform extra work but keeps parity with other mixins.
        """

    @property
    def file(self) -> Optional[str]:
        """Return config file path.

        ### Returns:
        [Optional[str]] - Absolute path or None when not set.
        """
        out: Optional[PathChecker] = self._get_data(
            key=_Keys.FILE,
        )
        if out:
            return out.path
        return None

    @file.setter
    def file(self, path: str) -> None:
        """Set file name.

        ### Arguments:
        * path: str - Path to configuration file.
        """
        self._set_data(
            key=_Keys.FILE,
            set_default_type=PathChecker,
            value=PathChecker(path),
        )

    @property
    def file_exists(self) -> bool:
        """Check if the file exists and is a file.

        ### Returns:
        [bool] - True when the file exists and is not a directory.

        ### Raises:
        * AttributeError: Path not configured prior to call.
        """
        obj: Optional[PathChecker] = self._get_data(key=_Keys.FILE)
        if obj:
            return obj.exists and (obj.is_file or obj.is_symlink) and not obj.is_dir
        raise Raise.error(
            f"{self._c_name}.file not set.",
            AttributeError,
            self._c_name,
            currentframe(),
        )

    def file_create(self) -> bool:
        """Try to create file.

        ### Returns:
        [bool] - True when file already exists or was created.

        ### Raises:
        * AttributeError: Path not configured.
        * OSError: Path points to an existing directory.
        """
        if self.file_exists:
            return True
        obj: Optional[PathChecker] = self._get_data(key=_Keys.FILE)
        if obj:
            if obj.exists and obj.is_dir:
                raise Raise.error(
                    f"Given path: {obj.path} exists and is a directory.",
                    OSError,
                    self._c_name,
                    currentframe(),
                )
            return obj.create()
        raise Raise.error(
            f"{self._c_name}.file not set.",
            AttributeError,
            self._c_name,
            currentframe(),
        )

    def read(self) -> str:
        """Try to read config file.

        ### Returns:
        [str] - Entire file contents as a string.
        """
        out: str = ""
        if self.file_exists:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "r") as file:
                    out = file.read()
        return out

    def readlines(self) -> List[str]:
        """Try to read config file and create list of strings.

        ### Returns:
        [List[str]] - List of lines stripped from end markers.
        """
        out: List[str] = []
        if self.file_exists:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "r") as file:
                    tmp = file.readlines()
                    for line in tmp:
                        stripped = line.strip()
                        if stripped.startswith("# -----<end of section"):
                            continue
                        out.append(stripped)
        return out

    def write(self, data: str) -> None:
        """Try to write data to config file.

        ### Arguments:
        * data: str - Serialized configuration payload.
        """
        test: bool = self.file_exists
        if not test:
            test = self.file_create()
        if test:
            filepath: Optional[str] = self.file
            if filepath is not None:
                with open(filepath, "w") as file:
                    file.write(data)


# #[EOF]#######################################################################
