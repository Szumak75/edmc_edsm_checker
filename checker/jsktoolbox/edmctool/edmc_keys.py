# -*- coding: utf-8 -*-
"""
  edmc_keys.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 8.10.2024, 17:22:21
  
  Purpose: 
"""


from ..attribtool import ReadOnlyClass


class EdmcKeys(object, metaclass=ReadOnlyClass):
    """EDMC Keys container class."""

    EVENT: str = "event"
    FSD_JUMP: str = "FSDJump"
    FSD_TARGET: str = "FSDTarget"
    NAME: str = "Name"
    STAR_CLASS: str = "StarClass"
    STAR_SYSTEM: str = "StarSystem"
    SYSTEM_ADDRESS: str = "SystemAddress"
    SYSTEM_BODY: str = "SystemBody"
    SYSTEM_BODY_COUNT: str = "SystemBodyCount"
    SYSTEM_COORDS: str = "SystemCoords"
    SYSTEM_COORDS_LOCKED: str = "SystemCoordsLocked"
    SYSTEM_DISTANCE: str = "SystemDistance"
    SYSTEM_NAME: str = "SystemName"


# #[EOF]#######################################################################
