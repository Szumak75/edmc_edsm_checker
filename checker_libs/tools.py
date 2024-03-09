# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: tools classes.
"""

from inspect import currentframe
import json
from typing import Dict, Optional, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

import requests
from requests.utils import requote_uri
from checker_libs.stars import StarsSystem


class Url(NoDynamicAttributes):
    """Url.

    Class for serving HTTP/HTTPS requests.
    """

    __options: Dict[str, int] = None  # type: ignore
    __systems_url: str = None  # type: ignore
    __system_url: str = None  # type: ignore

    def __init__(self) -> None:
        """Create Url helper object."""
        self.__options = {
            "showId": 1,
            "showPermit": 1,
            "showCoordinates": 1,
            "showInformation": 0,
            "showPrimaryStar": 0,
            "includeHidden": 0,
        }
        self.__systems_url = "https://www.edsm.net/api-v1/"
        self.__system_url = "https://www.edsm.net/api-system-v1/"

    @property
    def options(self) -> str:
        """Get url options string."""
        out: str = ""
        for key, value in self.__options.items():
            out += f"&{key}={value}"
        return out

    def bodies_url(self, ssystem: StarsSystem) -> str:
        """Return proper API url for getting bodies information data."""
        if not isinstance(ssystem, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(ssystem)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

        if ssystem.name:
            return requote_uri(f"{self.__system_url}bodies?systemName={ssystem.name}")
        if ssystem.address:
            return requote_uri(f"{self.__system_url}bodies?systemId={ssystem.address}")
        return ""

    def system_url(self, ssystem: StarsSystem) -> str:
        """Return proper API url for getting system data."""
        if not isinstance(ssystem, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(ssystem)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )

        if ssystem.name:
            return requote_uri(
                f"{self.__systems_url}system?systemName={ssystem.name}{self.options}"
            )
        return ""

    def radius_url(self, ssystem: StarsSystem, radius: int) -> str:
        """Return proper API url for getting systems data in radius."""
        if not isinstance(ssystem, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(ssystem)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if not isinstance(radius, int):
            radius = 50
        else:
            if radius < 5:
                radius = 5
            elif radius > 100:
                radius = 100

        if ssystem.name:
            return requote_uri(
                f"{self.__systems_url}sphere-systems?systemName={ssystem.name}&radius={radius}{self.options}"
            )
        return ""

    def cube_url(self, ssystem: StarsSystem, size: int) -> str:
        """Return proper API url for getting systems data in radius."""
        if not isinstance(ssystem, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(ssystem)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if not isinstance(size, int):
            size = 100
        else:
            if size < 10:
                size = 10
            elif size > 200:
                size = 200

        if ssystem.name:
            return requote_uri(
                f"{self.__systems_url}cube-systems?systemName={ssystem.name}&size={size}{self.options}"
            )
        return ""

    def system_query(self, ssystem: StarsSystem) -> Optional[Dict]:
        """Return result of query for system data."""
        if not isinstance(ssystem, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(ssystem)}' received",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        url: str = self.system_url(ssystem)
        if not url:
            return None

        try:
            response: requests.Response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print(f"Error calling API for system data: {response.status_code}")
                return None
            return json.loads(response.text)
        except Exception as ex:
            print(ex)
        return None

    def url_query(self, url: str) -> Dict[str, Any]:
        """Return result of query for url."""
        out = {}
        if not url:
            return out

        try:
            response: requests.Response = requests.get(url, timeout=60)
            if response.status_code != 200:
                print(f"Error calling API for EDSM data: {response.status_code}")
            else:
                out = json.loads(response.text)
        except Exception as ex:
            print(ex)
        return out


class Numbers(NoDynamicAttributes):
    """Numbers tool."""

    def is_float(self, element: Any) -> bool:
        """Check, if element is proper float variable."""
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False


# #[EOF]#######################################################################
