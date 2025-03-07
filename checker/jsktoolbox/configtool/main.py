# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose: Main class for creating and processes config files.
"""

import re
from inspect import currentframe
from typing import List, Dict, Optional, Any

from ..attribtool import NoDynamicAttributes, ReadOnlyClass
from ..raisetool import Raise
from ..basetool.data import BData
from .libs.file import FileProcessor
from .libs.data import DataProcessor
from .libs.data import SectionModel


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    DESC: str = "__desc__"
    DP: str = "__data_processor__"
    FP: str = "__file_processor__"
    RE_BOOL: str = "__re_bool__"
    RE_DESC: str = "__re_description__"
    RE_FALSE: str = "__re_false__"
    RE_FLOAT: str = "__re_float__"
    RE_INT: str = "__re_integer__"
    RE_LIST: str = "__re_list__"
    RE_SECTION: str = "__re_section__"
    RE_TRUE: str = "__re_true__"
    RE_VAR: str = "__re_variable__"
    VALUE: str = "__value__"
    VARNAME: str = "__varname__"


class Config(BData, NoDynamicAttributes):
    """Config main class."""

    def __init__(
        self,
        filename: str,
        main_section_name: str,
        auto_create: bool = False,
    ) -> None:
        """Constructor."""
        self._set_data(
            key=_Keys.FP, value=FileProcessor(), set_default_type=FileProcessor
        )
        self._set_data(
            key=_Keys.DP, value=DataProcessor(), set_default_type=DataProcessor
        )
        self.__fp.file = filename
        self.__dp.main_section = main_section_name
        if auto_create:
            if not self.__fp.file_exists:
                self.__fp.file_create()
        # compile regex
        self._data[_Keys.RE_SECTION] = re.compile(r"\s{0,}\[.*\]\s{0,}")
        self._data[_Keys.RE_DESC] = re.compile(r"\s{0,}#")
        self._data[_Keys.RE_VAR] = re.compile(r"\s{0,}\S{1,}\s{0,}=")
        self._data[_Keys.RE_INT] = re.compile(r"^\d{1,}$")
        self._data[_Keys.RE_FLOAT] = re.compile(r"^\d{1,}\.\d{1,}$")
        self._data[_Keys.RE_BOOL] = re.compile(r"^true|false|yes|no$", re.IGNORECASE)
        self._data[_Keys.RE_TRUE] = re.compile(r"^true|yes$", re.IGNORECASE)
        self._data[_Keys.RE_FALSE] = re.compile(r"^false|no$", re.IGNORECASE)
        self._data[_Keys.RE_LIST] = re.compile(r"^\[.*\]$")

    @property
    def __fp(self) -> FileProcessor:
        """Return FileProcessor object."""
        return self._get_data(key=_Keys.FP)  # type: ignore

    @property
    def __dp(self) -> DataProcessor:
        """Return DataProcessor object."""
        return self._get_data(key=_Keys.DP)  # type: ignore

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__fp.file_exists

    def __value_parser(self, item: str) -> Any:
        """Return proper type of value."""
        if self._data[_Keys.RE_BOOL].match(item):
            return True if self._data[_Keys.RE_TRUE].match(item) else False
        elif self._data[_Keys.RE_INT].match(item):
            return int(item)
        elif self._data[_Keys.RE_FLOAT].match(item):
            return float(item)
        elif self._data[_Keys.RE_LIST].match(item):
            out = []
            tmp: list[str] = [x.strip() for x in item.strip("[]").split(",")]
            for item in tmp:
                out.append(self.__value_parser(item))
            return out
        return str(item.strip("\"'"))

    def __var_parser(self, line: str) -> Dict:
        """Return Dict[varname, value, desc]."""
        out: dict[str, Any] = {
            _Keys.VARNAME: None,
            _Keys.VALUE: None,
            _Keys.DESC: None,
        }
        tmp: list[str] = line.split("=", 1)
        if len(tmp) != 2:
            raise Raise.error(
                f"Unexpected config line format: '{line}'",
                ValueError,
                self._c_name,
                currentframe(),
            )
        out[_Keys.VARNAME] = tmp[0].strip()
        if len(tmp[1]) > 0:
            tmp = tmp[1].split("#", 1)
            # desc
            if len(tmp) == 2 and len(tmp[1]) > 0:
                out[_Keys.DESC] = tmp[1].strip()
            # value
            out[_Keys.VALUE] = self.__value_parser(tmp[0].strip())

        return out

    def load(self) -> bool:
        """Load config file to DataProcessor."""
        test = False
        # 1. load file into list
        file: List[str] = self.__fp.readlines()
        section_name: str = ""
        if self.__dp.main_section is not None:
            section_name = self.__dp.main_section
        for line in file:
            # check section
            if self._data[_Keys.RE_SECTION].match(line):
                section_name = self.__dp.add_section(line)
            # check description
            elif self._data[_Keys.RE_DESC].match(line):
                self.__dp.set(section_name, desc=line.strip("# "))
            # check var
            elif self._data[_Keys.RE_VAR].match(line):
                out = self.__var_parser(line)
                self.__dp.set(
                    section=section_name,
                    varname=out[_Keys.VARNAME],
                    value=out[_Keys.VALUE],
                    desc=out[_Keys.DESC],
                )
            else:
                self.__dp.set(section_name, desc=line)
            test = True
        return test

    def save(self) -> bool:
        """Save config file from DataProcessor."""
        test = False
        self.__fp.write(self.__dp.dump)
        test = True
        return test

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Any:
        """Get and return data."""
        return self.__dp.get(section, varname, desc)

    def set(
        self,
        section: str,
        varname: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Set data."""
        self.__dp.set(section, varname, value, desc)

    def has_section(self, section: str) -> bool:
        """Check section name in config file."""
        if not isinstance(section, str):
            raise Raise.error(
                f"Expected String type, received: '{type(section)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        return self.__dp.get_section(section) is not None

    def has_varname(self, section_name: str, varname: str) -> bool:
        """Check varname in section."""
        if not isinstance(varname, str):
            raise Raise.error(
                f"Expected String type, received: '{type(varname)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if self.has_section(section_name):
            tmp: Optional[SectionModel] = self.__dp.get_section(section_name)
            if tmp is not None:
                found_section: SectionModel = tmp
                return found_section.get_variable(varname) is not None
        return False

    @property
    def main_section_name(self) -> Optional[str]:
        """Return main section name string."""
        return self.__dp.main_section


# #[EOF]#######################################################################
