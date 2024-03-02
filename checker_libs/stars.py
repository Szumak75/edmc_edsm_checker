# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose:
"""

from inspect import currentframe
from typing import Optional, List, Dict, Union, Any

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise


class StarsSystem(NoDynamicAttributes):
    """StarsSystem container class."""

    __name: Optional[str] = None
    __address: Optional[int] = None
    __pos_x: Optional[float] = None
    __pos_y: Optional[float] = None
    __pos_z: Optional[float] = None
    __data: Optional[Dict[str, Any]] = None

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
            f"{self.__class__.__name__}(name='{self.name}', "
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
        return self.__address

    @address.setter
    def address(self, arg: Optional[Union[int, str]]) -> None:
        if arg is None or isinstance(arg, int):
            self.__address = arg
        elif isinstance(arg, str) and arg.isdigit():
            self.__address = int(arg)
        else:
            raise Raise.error(
                f"Int type expected, '{type(arg)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def name(self) -> Optional[str]:
        """Give me name of system."""
        return self.__name

    @name.setter
    def name(self, arg: Optional[str]) -> None:
        if arg is None or isinstance(arg, str):
            self.__name = arg
            if arg is None:
                self.address = None
                self.star_pos = None
        else:
            raise Raise.error(
                f"String type expected, '{type(arg)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def pos_x(self) -> Optional[float]:
        """Give me pos_x of system."""
        return self.__pos_x

    @pos_x.setter
    def pos_x(self, arg: Optional[float]) -> None:
        if arg is None:
            self.__pos_x = arg
        elif isinstance(arg, (int, float)):
            self.__pos_x = float(arg)
        else:
            raise Raise.error(
                f"String type expected, '{type(arg)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def pos_y(self) -> Optional[float]:
        """Give me pos_y of system."""
        return self.__pos_y

    @pos_y.setter
    def pos_y(self, arg: Optional[float]) -> None:
        if arg is None:
            self.__pos_y = arg
        elif isinstance(arg, (int, float)):
            self.__pos_y = float(arg)
        else:
            raise Raise.error(
                f"String type expected, '{type(arg)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def pos_z(self) -> Optional[float]:
        """Give me pos_z of system."""
        return self.__pos_z

    @pos_z.setter
    def pos_z(self, arg: Optional[float]) -> None:
        if arg is None:
            self.__pos_z = arg
        elif isinstance(arg, (int, float)):
            self.__pos_z = float(arg)
        else:
            raise Raise.error(
                f"String type expected, '{type(arg)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
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
        if self.__data is None:
            self.__data = {}
        return self.__data

    @data.setter
    def data(self, value: Optional[Dict]) -> None:
        if value is None:
            self.__data = {}
        if not isinstance(value, Dict):
            raise Raise.error(
                f"Type of data container is dict, '{type(value)}' received, cannot proceed.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        self.__data = value


# #[EOF]#######################################################################
