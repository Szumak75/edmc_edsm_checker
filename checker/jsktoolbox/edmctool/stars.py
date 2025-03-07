# -*- coding: utf-8 -*-
"""
stars.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 7.10.2024, 13:39:31

Purpose: StarsSystem container.
"""

from inspect import currentframe
from typing import Optional, List, Dict, Union, Any

from ..attribtool import ReadOnlyClass
from ..raisetool import Raise
from ..basetool.data import BData
from .edsm_keys import EdsmKeys


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    # StarsSystem
    SS_ADDRESS: str = "__ss_address__"
    SS_DATA: str = "__ss_data__"
    SS_NAME: str = "__ss_name__"
    SS_POS_X: str = "__ss_pos_x__"
    SS_POS_Y: str = "__ss_pos_y__"
    SS_POS_Z: str = "__ss_pos_z__"
    SS_STAR_CLASS: str = "__ss_star_class__"


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
            f"star_pos={self.star_pos}, "
            f"data={self.data})"
        )

    @property
    def address(self) -> Optional[int]:
        """Returns address of the star system."""
        return self._get_data(key=_Keys.SS_ADDRESS, default_value=None)

    @address.setter
    def address(self, arg: Optional[Union[int, str]]) -> None:
        """Sets  address of the star system."""
        if isinstance(arg, str):
            self._set_data(
                key=_Keys.SS_ADDRESS,
                value=int(arg),
                set_default_type=Optional[int],
            )
        else:
            self._set_data(
                key=_Keys.SS_ADDRESS, value=arg, set_default_type=Optional[int]
            )

    @property
    def data(self) -> Dict:
        """Returns data container.

        This is dictionary object for storing various elements.
        """
        if self._get_data(key=_Keys.SS_DATA, default_value=None) is None:
            self._set_data(key=_Keys.SS_DATA, value={}, set_default_type=Dict)
        return self._get_data(key=_Keys.SS_DATA)  # type: ignore

    @data.setter
    def data(self, value: Optional[Dict]) -> None:
        """Initialize or set data container."""
        if value is None:
            self._set_data(key=_Keys.SS_DATA, value={}, set_default_type=Dict)
        else:
            self._set_data(key=_Keys.SS_DATA, value=value, set_default_type=Dict)

    @property
    def name(self) -> Optional[str]:
        """Returns name of the  star system."""
        return self._get_data(key=_Keys.SS_NAME, default_value=None)

    @name.setter
    def name(self, arg: Optional[str]) -> None:
        """Sets name of the star system."""
        self._set_data(key=_Keys.SS_NAME, value=arg, set_default_type=Optional[str])

    @property
    def pos_x(self) -> Optional[Union[float, int]]:
        """Returns pos_x of the star system."""
        return self._get_data(key=_Keys.SS_POS_X, default_value=None)

    @pos_x.setter
    def pos_x(self, arg: Optional[Union[float, int]]) -> None:
        """Sets pos_x of the star system."""
        self._set_data(
            key=_Keys.SS_POS_X, value=arg, set_default_type=Optional[Union[float, int]]
        )

    @property
    def pos_y(self) -> Optional[Union[float, int]]:
        """Returns pos_y of the star system."""
        return self._get_data(key=_Keys.SS_POS_Y, default_value=None)

    @pos_y.setter
    def pos_y(self, arg: Optional[Union[float, int]]) -> None:
        """Sets pos_y of the star system."""
        self._set_data(
            key=_Keys.SS_POS_Y, value=arg, set_default_type=Optional[Union[float, int]]
        )

    @property
    def pos_z(self) -> Optional[Union[float, int]]:
        """Returns pos_z of the star system."""
        return self._get_data(key=_Keys.SS_POS_Z, default_value=None)

    @pos_z.setter
    def pos_z(self, arg: Optional[Union[float, int]]) -> None:
        """Sets pos_z of the star system."""
        self._set_data(
            key=_Keys.SS_POS_Z, value=arg, set_default_type=Optional[Union[float, int]]
        )

    @property
    def star_class(self) -> str:
        """Returns star class string."""
        return self._get_data(key=_Keys.SS_STAR_CLASS, default_value="")  # type: ignore

    @star_class.setter
    def star_class(self, value: str) -> None:
        """Sets star class string."""
        self._set_data(key=_Keys.SS_STAR_CLASS, value=value, set_default_type=str)

    @property
    def star_pos(self) -> List:
        """Returns the star position list."""
        return [self.pos_x, self.pos_y, self.pos_z]

    @star_pos.setter
    def star_pos(self, arg: Optional[List] = None) -> None:
        """Sets  the star position list."""
        if arg is None:
            (self.pos_x, self.pos_y, self.pos_z) = (None, None, None)
        elif isinstance(arg, List) and len(arg) == 3:
            (self.pos_x, self.pos_y, self.pos_z) = arg
        else:
            raise Raise.error(
                f"List type expected, '{type(arg)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )

    def update_from_edsm(self, data: Dict) -> None:
        """Update records from given EDSM Api dict."""
        if data is None or not isinstance(data, Dict):
            return

        self.name = data.get(EdsmKeys.NAME, self.name)
        self.address = data.get(EdsmKeys.ID64, self.address)
        if EdsmKeys.COORDS in data and EdsmKeys.X in data[EdsmKeys.COORDS]:
            self.pos_x = data[EdsmKeys.COORDS].get(EdsmKeys.X, self.pos_x)
            self.pos_y = data[EdsmKeys.COORDS].get(EdsmKeys.Y, self.pos_y)
            self.pos_z = data[EdsmKeys.COORDS].get(EdsmKeys.Z, self.pos_z)
        if EdsmKeys.BODY_COUNT in data:
            self.data[EdsmKeys.BODY_COUNT] = data[EdsmKeys.BODY_COUNT]
        if EdsmKeys.COORDS_LOCKED in data:
            self.data[EdsmKeys.COORDS_LOCKED] = data[EdsmKeys.COORDS_LOCKED]
        if EdsmKeys.REQUIRE_PERMIT in data:
            self.data[EdsmKeys.REQUIRE_PERMIT] = data[EdsmKeys.REQUIRE_PERMIT]
        if EdsmKeys.DISTANCE in data:
            self.data[EdsmKeys.DISTANCE] = data[EdsmKeys.DISTANCE]
        if EdsmKeys.BODIES in data:
            self.data[EdsmKeys.BODIES] = len(data[EdsmKeys.BODIES])


# #[EOF]#######################################################################
