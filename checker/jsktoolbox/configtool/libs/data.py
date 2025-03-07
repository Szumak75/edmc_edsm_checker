# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 29.10.2023

Purpose: DataProcessor class for processing dataset operations.
"""

from inspect import currentframe
from typing import List, Tuple, Optional, Union, Any, TypeVar
from abc import ABC, abstractmethod
from copy import copy

from ...attribtool import NoDynamicAttributes, ReadOnlyClass
from ...raisetool import Raise
from ...basetool.data import BData

TVariableModel = TypeVar("TVariableModel", bound="VariableModel")


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    DATA: str = "__data__"
    DESC: str = "__desc__"
    DESCRIPTION: str = "__description__"
    MAIN: str = "__main__"
    NAME: str = "__name__"
    VALUE: str = "__value__"
    VARIABLES: str = "__variables__"


class IModel(ABC):
    """Model class interface."""

    @property
    @abstractmethod
    def dump(self) -> Union[List[str], TVariableModel]:
        """Dump data."""

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Get name property."""

    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        """Set name property."""

    @abstractmethod
    def parser(self, value: str) -> None:
        """Parser method."""

    @abstractmethod
    def search(self, name: str) -> bool:
        """Search method."""


class VariableModel(BData, IModel, NoDynamicAttributes):
    """VariableModel class."""

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[Union[str, int, float, bool, List]] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Constructor."""
        self._data[_Keys.NAME] = name
        self._data[_Keys.VALUE] = value
        self._data[_Keys.DESC] = desc

    def __repr__(self) -> str:
        """Return representation class string."""
        tmp: str = ""
        tmp += f"name='{self.name}', " if self.name is not None else ""
        if isinstance(self.value, (int, float, bool)):
            tmp += f"value={self.value}, " if self.value is not None else ""
        elif isinstance(self.value, List):
            tmp += f"value=[{self.value}], " if self.value is not None else ""
        else:
            tmp += f"value='{self.value}', " if self.value is not None else ""
        tmp += f"desc='{self.desc}'" if self.desc is not None else ""
        return f"{self._c_name}({tmp})"

    def __str__(self) -> str:
        """Return formatted string."""
        tmp: str = ""
        tmp += f"{self.name} = " if self.name is not None else ""
        if isinstance(self.value, (int, float, bool)):
            tmp += f"{self.value}" if self.value is not None else ""
        elif isinstance(self.value, List):
            tmp += f"{self.value}" if self.value is not None else ""
        else:
            tmp += (
                '"{}"'.format(self.value.strip("\"'")) if self.value is not None else ""
            )
        if tmp:
            tmp += f" # {self.desc}" if self.desc is not None else ""
        else:
            tmp += f"# {self.desc}" if self.desc is not None else "#"
        return tmp

    @property
    def desc(self) -> Optional[str]:
        """Get description property."""
        return self._get_data(key=_Keys.DESC, set_default_type=Optional[str])

    @desc.setter
    def desc(self, desc: Optional[str]) -> None:
        """Set description property."""
        self._set_data(key=_Keys.DESC, value=desc, set_default_type=Optional[str])

    @property
    def dump(self) -> TVariableModel:
        """Dump data."""
        return self  # type: ignore

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._get_data(key=_Keys.NAME, set_default_type=Optional[str])

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set name property."""
        if name is None:
            self._set_data(key=_Keys.NAME, value=None, set_default_type=Optional[str])
        else:
            self._set_data(
                key=_Keys.NAME, value=name.strip(), set_default_type=Optional[str]
            )

    def parser(self, value: str) -> None:
        """Parser method."""

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def value(self) -> Optional[Union[str, int, float, bool, List]]:
        """Get value property."""
        return self._get_data(
            key=_Keys.VALUE,
            set_default_type=Optional[Union[str, int, float, bool, List]],
        )

    @value.setter
    def value(self, value: Optional[Union[str, int, float, bool, List]]) -> None:
        """Set value property."""
        self._set_data(
            key=_Keys.VALUE,
            value=value,
            set_default_type=Optional[Union[str, int, float, bool, List]],
        )


class SectionModel(BData, IModel, NoDynamicAttributes):
    """SectionModel class."""

    def __init__(self, name: Optional[str] = None) -> None:
        """Constructor."""
        self._data[_Keys.NAME] = None
        self._data[_Keys.VARIABLES] = []
        self.parser(name)

    def __repr__(self) -> str:
        """Return representation class string."""
        return f"{self._c_name}(name='{self.name}')"

    def __str__(self) -> str:
        """Return formatted string."""
        return f"[{self.name}]"

    @property
    def dump(self) -> List[Any]:
        """Dump data."""
        tmp: List = []
        tmp.append(self)
        for item in self._data[_Keys.VARIABLES]:
            tmp.append(item.dump())
        return copy(tmp)

    def parser(self, value: Optional[str]) -> None:
        """Parser method."""
        if value is None:
            return
        tmp: str = f"{value}".strip("[] \n")
        if tmp:
            self._data[_Keys.NAME] = tmp
        else:
            raise Raise.error(
                f"Expected String name, received: '{tmp}'.",
                ValueError,
                self._c_name,
                currentframe(),
            )

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data[_Keys.NAME]

    @name.setter
    def name(self, name: str) -> None:
        """Set name property."""
        self.parser(name)

    def get_variable(self, name: str) -> Optional[VariableModel]:
        """Search and return VariableModel if exists."""
        name = str(name)
        for item in self._data[_Keys.VARIABLES]:
            if item.name == name:
                return item
        return None

    def set_variable(
        self,
        name: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Add or update VariableModel."""
        if name is not None:
            tmp: Optional[VariableModel] = self.get_variable(name)
            if tmp is not None:
                item: VariableModel = tmp
                if value is not None or (value is None and desc is None):
                    item.value = value
                if desc is not None or (desc is None and value is None):
                    item.desc = desc
                return
        # add new VariableModel
        if name is None and value is not None:
            return
        self._data[_Keys.VARIABLES].append(VariableModel(name, value, desc))

    @property
    def variables(self) -> List[VariableModel]:
        """Return list of VariableModel."""
        return self._data[_Keys.VARIABLES]


class DataProcessor(BData, NoDynamicAttributes):
    """DataProcessor class."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[_Keys.DATA] = []

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name."""
        return self._get_data(key=_Keys.MAIN, set_default_type=Optional[str])

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name."""
        if not isinstance(name, str):
            name = str(name)
        self._set_data(key=_Keys.MAIN, value=name, set_default_type=Optional[str])
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple."""
        out = []
        for item in self._data[_Keys.DATA]:
            out.append(item.name)
        return tuple(sorted(out))

    def add_section(self, name: str) -> str:
        """Add section object to dataset.

        Return: extracted section name.
        """
        sm = SectionModel(str(name))
        if sm.name not in self.sections:
            self._data[_Keys.DATA].append(sm)
        return f"{sm.name}"

    def get_section(self, name: str) -> Optional[SectionModel]:
        """Get section object if exists."""
        sm = SectionModel(name)
        for item in self._data[_Keys.DATA]:
            if item.name == sm.name:
                return item
        return None

    def set(
        self,
        section: str,
        varname: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Set data to [SectionModel]->[VariableModel]."""
        section_name: str = self.add_section(section)
        tmp: Optional[SectionModel] = self.get_section(section_name)
        if tmp is not None:
            found_section: SectionModel = tmp
            found_section.set_variable(varname, value, desc)

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Optional[Any]:
        """Return value."""
        sm = SectionModel(section)
        if sm.name in self.sections:
            tmp: Optional[SectionModel] = self.get_section(section)
            if tmp is not None:
                found_section: SectionModel = tmp
                if varname is not None:
                    found_var: Optional[VariableModel] = found_section.get_variable(
                        varname
                    )
                    if found_var is not None:
                        if desc:
                            # Return description for varname
                            return found_var.desc
                        else:
                            # Return value for varname
                            return found_var.value
                    else:
                        return None
                else:
                    # Return list od description for section
                    out: List[str] = []
                    for item in found_section.variables:
                        if item.name is None and item.desc is not None:
                            out.append(item.desc)
                    return out
        else:
            raise Raise.error(
                f"Given section name: '{section}' not found.",
                KeyError,
                self._c_name,
                currentframe(),
            )

    def __dump(self, section: str) -> str:
        """Return formatted configuration data for section name."""
        out: str = ""
        if section in self.sections:
            tmp: Optional[SectionModel] = self.get_section(section)
            if tmp is not None:
                found_section: SectionModel = tmp
                out += f"{found_section}\n"
                for item in found_section.variables:
                    out += f"{item}\n"
                out += f"# -----<end of section: '{found_section.name}'>-----\n"
        else:
            raise Raise.error(
                f"Section name: '{section}' not found.",
                KeyError,
                self._c_name,
                currentframe(),
            )
        return out

    @property
    def dump(self) -> str:
        """Return formatted configuration data string."""
        out: str = ""

        # first section is a main section
        if self.main_section is None:
            raise Raise.error(
                "Main section is not set.",
                KeyError,
                self._c_name,
                currentframe(),
            )
        out = self.__dump(self.main_section)

        # other sections
        for section in sorted(tuple(set(self.sections) ^ set([self.main_section]))):
            out += self.__dump(section)

        return out


# #[EOF]#######################################################################
