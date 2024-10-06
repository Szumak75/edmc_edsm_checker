# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose:
"""

from inspect import currentframe
from typing import Optional, List, Dict, Union, Any

from checker.jsktoolbox.attribtool import NoDynamicAttributes
from checker.jsktoolbox.raisetool import Raise
from checker.jsktoolbox.basetool.data import BData
from checker.keys import CheckerKeys


class StarsSystem(BData):
    """StarsSystem container class."""

    def __init__(
        self,
        name: Optional[str] = None,
        address: Optional[int] = None,
        star_pos: Optional[List] = None,
    ) -> None:
        """Create Star System object."""
        self.name = name
        self.address = address
        self.star_pos = star_pos

    def __repr__(self) -> str:
        """Give me class dump."""
        return (
            f"{self._c_name}(name='{self.name}', "
            f"address={self.address}, "
            f"starpos={self.star_pos}, "
            f"data={self.data})"
        )

    def update_from_edsm(self, data: Dict) -> None:
        """Update records from given EDSM Api dict."""
        if data is None or not isinstance(data, Dict):
            return

        self.name = data.get("name", self.name)
        self.address = data.get("id64", self.address)
        if "coords" in data and "x" in data["coords"]:
            self.pos_x = data["coords"].get("x", self.pos_x)
            self.pos_y = data["coords"].get("y", self.pos_y)
            self.pos_z = data["coords"].get("z", self.pos_z)
        if "bodyCount" in data:
            self.data["bodycount"] = data["bodyCount"]
        if "coordsLocked" in data:
            self.data["coordslocked"] = data["coordsLocked"]
        if "requirePermit" in data:
            self.data["requirepermit"] = data["requirePermit"]
        if "distance" in data:
            self.data["distance"] = data["distance"]
        if "bodies" in data:
            self.data["bodies"] = len(data["bodies"])

    @property
    def address(self) -> Optional[int]:
        """Give me address of system."""
        return self._get_data(key=CheckerKeys.SS_ADDRESS, default_value=None)

    @address.setter
    def address(self, arg: Optional[Union[int, str]]) -> None:
        if isinstance(arg, str):
            self._set_data(
                key=CheckerKeys.SS_ADDRESS,
                value=int(arg),
                set_default_type=Optional[int],
            )
        else:
            self._set_data(
                key=CheckerKeys.SS_ADDRESS, value=arg, set_default_type=Optional[int]
            )

    @property
    def name(self) -> Optional[str]:
        """Give me name of system."""
        return self._get_data(key=CheckerKeys.SS_NAME, default_value=None)

    @name.setter
    def name(self, arg: Optional[str]) -> None:
        self._set_data(
            key=CheckerKeys.SS_NAME, value=arg, set_default_type=Optional[str]
        )

    @property
    def pos_x(self) -> Optional[float]:
        """Give me pos_x of system."""
        return self._get_data(key=CheckerKeys.SS_POS_X, default_value=None)

    @pos_x.setter
    def pos_x(self, arg: Optional[float]) -> None:
        self._set_data(
            key=CheckerKeys.SS_POS_X, value=arg, set_default_type=Optional[float]
        )

    @property
    def pos_y(self) -> Optional[float]:
        """Give me pos_y of system."""
        return self._get_data(key=CheckerKeys.SS_POS_Y, default_value=None)

    @pos_y.setter
    def pos_y(self, arg: Optional[float]) -> None:
        self._set_data(
            key=CheckerKeys.SS_POS_Y, value=arg, set_default_type=Optional[float]
        )

    @property
    def pos_z(self) -> Optional[float]:
        """Give me pos_z of system."""
        return self._get_data(key=CheckerKeys.SS_POS_Z, default_value=None)

    @pos_z.setter
    def pos_z(self, arg: Optional[float]) -> None:
        self._set_data(
            key=CheckerKeys.SS_POS_Z, value=arg, set_default_type=Optional[float]
        )

    @property
    def star_pos(self) -> List:
        """Give me star position list."""
        return [self.pos_x, self.pos_y, self.pos_z]

    @star_pos.setter
    def star_pos(self, arg: Optional[List] = None) -> None:
        if arg is None:
            (self.pos_x, self.pos_y, self.pos_z) = (None, None, None)
        elif isinstance(arg, List) and len(arg) == 3:
            (self.pos_x, self.pos_y, self.pos_z) = arg
        else:
            raise Raise.error(
                f"List type expected, '{type(arg)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def star_class(self) -> str:
        """Give me star class string."""
        if "StarClass" in self.data:
            return self.data["StarClass"]
        return ""

    @star_class.setter
    def star_class(self, value: str) -> None:
        """Set StarClass string."""
        self.data["StarClass"] = value

    @property
    def data(self) -> Dict:
        """Return data container.

        This is dictionary object for storing various elements.
        """
        if self._get_data(key=CheckerKeys.SS_DATA, default_value=None) is None:
            self._set_data(key=CheckerKeys.SS_DATA, value={}, set_default_type=Dict)
        return self._get_data(key=CheckerKeys.SS_DATA)  # type: ignore

    @data.setter
    def data(self, value: Optional[Dict]) -> None:
        if value is None:
            self._set_data(key=CheckerKeys.SS_DATA, value={}, set_default_type=Dict)
        else:
            self._set_data(key=CheckerKeys.SS_DATA, value=value, set_default_type=Dict)


# #[EOF]#######################################################################
