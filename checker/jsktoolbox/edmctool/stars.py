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


class EdmcKeys(object, metaclass=ReadOnlyClass):
    """EDMC Keys container class."""

    EDMC_EVENT: str = "event"
    EDMC_FSD_JUMP: str = "FSDJump"
    EDMC_FSD_TARGET: str = "FSDTarget"
    EDMC_NAME: str = "Name"
    EDMC_STAR_CLASS: str = "StarClass"
    EDMC_STAR_SYSTEM: str = "StarSystem"
    EDMC_SYSTEM_ADDRESS: str = "SystemAddress"
    EDMC_SYSTEM_BODY: str = "SystemBody"
    EDMC_SYSTEM_BODY_COUNT: str = "SystemBodyCount"
    EDMC_SYSTEM_COORDS: str = "SystemCoords"
    EDMC_SYSTEM_COORDS_LOCKED: str = "SystemCoordsLocked"
    EDMC_SYSTEM_DISTANCE: str = "SystemDistance"
    EDMC_SYSTEM_NAME: str = "SystemName"


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    # EDSM keys
    EDSM_ADDRESS: str = "id64"
    EDSM_BODIES: str = "bodies"
    EDSM_BODY_COUNT: str = "bodyCount"
    EDSM_COORDS: str = "coords"
    EDSM_COORDS_LOCKED: str = "coordsLocked"
    EDSM_DISTANCE: str = "distance"
    EDSM_NAME: str = "name"
    EDSM_REQUIRE_PERMIT: str = "requirePermit"
    EDSM_X: str = "x"
    EDSM_Y: str = "y"
    EDSM_Z: str = "z"

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
    def pos_x(self) -> Optional[float]:
        """Returns pos_x of the star system."""
        return self._get_data(key=_Keys.SS_POS_X, default_value=None)

    @pos_x.setter
    def pos_x(self, arg: Optional[float]) -> None:
        """Sets pos_x of the star system."""
        self._set_data(key=_Keys.SS_POS_X, value=arg, set_default_type=Optional[float])

    @property
    def pos_y(self) -> Optional[float]:
        """Returns pos_y of the star system."""
        return self._get_data(key=_Keys.SS_POS_Y, default_value=None)

    @pos_y.setter
    def pos_y(self, arg: Optional[float]) -> None:
        """Sets pos_y of the star system."""
        self._set_data(key=_Keys.SS_POS_Y, value=arg, set_default_type=Optional[float])

    @property
    def pos_z(self) -> Optional[float]:
        """Returns pos_z of the star system."""
        return self._get_data(key=_Keys.SS_POS_Z, default_value=None)

    @pos_z.setter
    def pos_z(self, arg: Optional[float]) -> None:
        """Sets pos_z of the star system."""
        self._set_data(key=_Keys.SS_POS_Z, value=arg, set_default_type=Optional[float])

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

        self.name = data.get(_Keys.EDSM_NAME, self.name)
        self.address = data.get(_Keys.EDSM_ADDRESS, self.address)
        if _Keys.EDSM_COORDS in data and _Keys.EDSM_X in data[_Keys.EDSM_COORDS]:
            self.pos_x = data[_Keys.EDSM_COORDS].get(_Keys.EDSM_X, self.pos_x)
            self.pos_y = data[_Keys.EDSM_COORDS].get(_Keys.EDSM_Y, self.pos_y)
            self.pos_z = data[_Keys.EDSM_COORDS].get(_Keys.EDSM_Z, self.pos_z)
        if _Keys.EDSM_BODY_COUNT in data:
            self.data[_Keys.EDSM_BODY_COUNT.lower()] = data[_Keys.EDSM_BODY_COUNT]
        if _Keys.EDSM_COORDS_LOCKED in data:
            self.data[_Keys.EDSM_COORDS_LOCKED.lower()] = data[_Keys.EDSM_COORDS_LOCKED]
        if _Keys.EDSM_REQUIRE_PERMIT in data:
            self.data[_Keys.EDSM_REQUIRE_PERMIT.lower()] = data[
                _Keys.EDSM_REQUIRE_PERMIT
            ]
        if _Keys.EDSM_DISTANCE in data:
            self.data[_Keys.EDSM_DISTANCE] = data[_Keys.EDSM_DISTANCE]
        if _Keys.EDSM_BODIES in data:
            self.data[_Keys.EDSM_BODIES] = len(data[_Keys.EDSM_BODIES])


# #[EOF]#######################################################################
