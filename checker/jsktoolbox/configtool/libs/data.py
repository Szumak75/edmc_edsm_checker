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
    """Representation of a configuration variable entry.

    ### Purpose:
    Stores name, value, and description for a single configuration variable.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[Union[str, int, float, bool, List]] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Initialise a variable record.

        ### Arguments:
        * name: Optional[str] - Variable identifier.
        * value: Optional[Union[str, int, float, bool, List]] - Payload to store.
        * desc: Optional[str] - Optional human-friendly description.
        """
        self._data[_Keys.NAME] = name
        self._data[_Keys.VALUE] = value
        self._data[_Keys.DESC] = desc

    def __repr__(self) -> str:
        """Return representation class string.

        ### Returns:
        [str] - Debug-friendly section representation.
        """
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
        """Return formatted section header.

        ### Returns:
        [str] - String in INI-style header format.
        """
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
        """Get description property.

        ### Returns:
        [Optional[str]] - Description string or None.
        """
        return self._get_data(key=_Keys.DESC, set_default_type=Optional[str])

    @desc.setter
    def desc(self, desc: Optional[str]) -> None:
        """Set description property.

        ### Arguments:
        * desc: Optional[str] - Description text.
        """
        self._set_data(key=_Keys.DESC, value=desc, set_default_type=Optional[str])

    @property
    def dump(self) -> TVariableModel:
        """Dump data.

        ### Returns:
        [List[Any]] - Shallow copy of section with variables.
        """
        return self  # type: ignore

    @property
    def name(self) -> Optional[str]:
        """Get name property.

        ### Returns:
        [Optional[str]] - Section name.
        """
        return self._get_data(key=_Keys.NAME, set_default_type=Optional[str])

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set name property.

        ### Arguments:
        * name: Optional[str] - New variable name.

        ### Raises:
        * ValueError: Raised when the trimmed name becomes empty.
        """
        if name is None:
            self._set_data(key=_Keys.NAME, value=None, set_default_type=Optional[str])
        else:
            cleaned = name.strip()
            if not cleaned:
                raise Raise.error(
                    "Variable name cannot be empty.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
            self._set_data(
                key=_Keys.NAME, value=cleaned, set_default_type=Optional[str]
            )

    def parser(self, value: str) -> None:
        """Parse raw string input ensuring valid state.

        ### Arguments:
        * value: str - Raw value string.

        ### Raises:
        * ValueError: Raised when the parsed value is empty after trimming.
        """

        if not value.strip():
            raise Raise.error(
                "Variable value cannot be empty.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        self.value = value

    def search(self, name: str) -> bool:
        """Search method.

        ### Arguments:
        * name: str - Section name to match.

        ### Returns:
        [bool] - True when names coincide.
        """
        return self.name == name

    @property
    def value(self) -> Optional[Union[str, int, float, bool, List]]:
        """Get value property.

        ### Returns:
        [Optional[Union[str, int, float, bool, List]]] - Stored value.
        """
        return self._get_data(
            key=_Keys.VALUE,
            set_default_type=Optional[Union[str, int, float, bool, List]],
        )

    @value.setter
    def value(self, value: Optional[Union[str, int, float, bool, List]]) -> None:
        """Set value property.

        ### Arguments:
        * value: Optional[Union[str, int, float, bool, List]] - Payload.
        """
        self._set_data(
            key=_Keys.VALUE,
            value=value,
            set_default_type=Optional[Union[str, int, float, bool, List]],
        )


class SectionModel(BData, IModel, NoDynamicAttributes):
    """Representation of a configuration section.

    ### Purpose:
    Aggregates variables and descriptions under a named section.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        """Initialise section state.

        ### Arguments:
        * name: Optional[str] - Optional section header value.
        """
        self._data[_Keys.NAME] = None
        self._data[_Keys.VARIABLES] = []
        self.parser(name)

    def __repr__(self) -> str:
        """Return representation class string.

        ### Returns:
        [str] - Debug-friendly section representation.
        """
        return f"{self._c_name}(name='{self.name}')"

    def __str__(self) -> str:
        """Return formatted section header.

        ### Returns:
        [str] - String in INI-style header format.
        """
        return f"[{self.name}]"

    @property
    def dump(self) -> List[Any]:
        """Dump data.

        ### Returns:
        [List[Any]] - Shallow copy of section with variables.
        """
        tmp: List = []
        tmp.append(self)
        for item in self._data[_Keys.VARIABLES]:
            tmp.append(item.dump())
        return copy(tmp)

    def parser(self, value: Optional[str]) -> None:
        """Parse and validate section name.

        ### Arguments:
        * value: Optional[str] - Raw header text.

        ### Raises:
        * ValueError: Raised when the name resolves to an empty string.
        """
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
        """Search method.

        ### Arguments:
        * name: str - Section name to match.

        ### Returns:
        [bool] - True when names coincide.
        """
        return self.name == name

    @property
    def name(self) -> Optional[str]:
        """Get name property.

        ### Returns:
        [Optional[str]] - Section name.
        """
        return self._data[_Keys.NAME]

    @name.setter
    def name(self, name: str) -> None:
        """Set name property.

        ### Arguments:
        * name: str - New section name.
        """
        self.parser(name)

    def get_variable(self, name: str) -> Optional[VariableModel]:
        """Search and return VariableModel if exists.

        ### Arguments:
        * name: str - Variable name to locate.

        ### Returns:
        [Optional[VariableModel]] - Matching variable instance or None.
        """
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
        """Add or update VariableModel.

        ### Arguments:
        * name: Optional[str] - Variable name to set or update.
        * value: Optional[Any] - Value payload.
        * desc: Optional[str] - Description text.

        ### Raises:
        * ValueError: Raised when both name and value are None.
        """
        if name is not None:
            key = name.strip() if isinstance(name, str) else name
            tmp: Optional[VariableModel] = (
                self.get_variable(key) if key is not None else None
            )
            if tmp is not None:
                item: VariableModel = tmp
                if value is not None or (value is None and desc is None):
                    item.value = value
                if desc is not None or (desc is None and value is None):
                    item.desc = desc
                return
        # add new VariableModel
        if name is None and value is not None:
            raise Raise.error(
                "Variable name is required when providing a value.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.VARIABLES].append(VariableModel(name, value, desc))

    @property
    def variables(self) -> List[VariableModel]:
        """Return list of VariableModel.

        ### Returns:
        [List[VariableModel]] - Mutable list of section variables.
        """
        return self._data[_Keys.VARIABLES]


class DataProcessor(BData, NoDynamicAttributes):
    """Manage configuration data composed of sections and variables.

    ### Purpose:
    Provides helpers for reading, setting, and dumping configuration structures.
    """

    def __init__(self) -> None:
        """Initialise DataProcessor state.

        ### Purpose:
        Ensures the internal container for sections exists.
        """
        self._data[_Keys.DATA] = []

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name.

        ### Returns:
        [Optional[str]] - Name of the primary section.
        """
        return self._get_data(key=_Keys.MAIN, set_default_type=Optional[str])

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name.

        ### Arguments:
        * name: str - Target section name.
        """
        if not isinstance(name, str):
            name = str(name)
        self._set_data(key=_Keys.MAIN, value=name, set_default_type=Optional[str])
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple.

        ### Returns:
        [Tuple] - Tuple containing names of tracked sections.
        """
        out = []
        for item in self._data[_Keys.DATA]:
            out.append(item.name)
        return tuple(sorted(out))

    def add_section(self, name: str) -> str:
        """Add section object to dataset.

        ### Arguments:
        * name: str - Raw section name.

        ### Returns:
        [str] - Sanitised section name actually stored.
        """
        sm = SectionModel(str(name))
        if sm.name not in self.sections:
            self._data[_Keys.DATA].append(sm)
        return f"{sm.name}"

    def get_section(self, name: str) -> Optional[SectionModel]:
        """Get section object if exists.

        ### Arguments:
        * name: str - Section name.

        ### Returns:
        [Optional[SectionModel]] - Matching section or None.
        """
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
        """Set data to [SectionModel]->[VariableModel].

        ### Arguments:
        * section: str - Section name.
        * varname: Optional[str] - Variable name.
        * value: Optional[Any] - Value payload.
        * desc: Optional[str] - Description text.
        """
        section_name: str = self.add_section(section)
        tmp: Optional[SectionModel] = self.get_section(section_name)
        if tmp is not None:
            found_section: SectionModel = tmp
            found_section.set_variable(varname, value, desc)

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Optional[Any]:
        """Return value.

        ### Arguments:
        * section: str - Section name.
        * varname: Optional[str] - Variable name to fetch.
        * desc: bool - When True returns description.

        ### Returns:
        [Optional[Any]] - Value or description based on `desc`.

        ### Raises:
        * KeyError: Section not present.
        """
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
        """Return formatted configuration data for section name.

        ### Arguments:
        * section: str - Section name to dump.

        ### Returns:
        [str] - Section content formatted for output.

        ### Raises:
        * KeyError: Section not present.
        """
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
        """Return formatted configuration data string.

        ### Returns:
        [str] - Full configuration payload.

        ### Raises:
        * KeyError: Main section not set.
        """
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
