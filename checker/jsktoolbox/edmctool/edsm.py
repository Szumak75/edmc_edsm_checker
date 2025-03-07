# -*- coding: utf-8 -*-
"""
edsm.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 8.10.2024, 12:15:38

Purpose:
"""

import requests  # type: ignore
import json
import json

from typing import Dict, List, Optional, Any, Union
from requests.utils import requote_uri  # type: ignore
from inspect import currentframe

from .edsm_keys import EdsmKeys


from ..basetool.data import BData
from ..attribtool import ReadOnlyClass
from ..raisetool import Raise
from ..edmctool.stars import StarsSystem


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal  keys container class."""

    OPTIONS: str = "__options__"
    SYSTEMS_URL: str = "__systems_url__"
    SYSTEM_URL: str = "__system_url__"


class Url(BData):
    """Url.

    Class for serving HTTP/HTTPS requests.
    """

    def __init__(self) -> None:
        """Create Url helper object."""
        self.__options = {
            EdsmKeys.SHOW_ID: 1,
            EdsmKeys.SHOW_PERMIT: 1,
            EdsmKeys.SHOW_COORDINATES: 1,
            EdsmKeys.SHOW_INFORMATION: 0,
            EdsmKeys.SHOW_PRIMARY_STAR: 0,
            EdsmKeys.INCLUDE_HIDDEN: 0,
        }
        self._set_data(
            key=_Keys.SYSTEMS_URL,
            value="https://www.edsm.net/api-v1/",
            set_default_type=str,
        )
        self._set_data(
            key=_Keys.SYSTEM_URL,
            value="https://www.edsm.net/api-system-v1/",
            set_default_type=str,
        )

    @property
    def __options(self) -> Dict:
        return self._get_data(key=_Keys.OPTIONS)  # type: ignore

    @__options.setter
    def __options(self, value: Optional[Dict]) -> None:
        if value is None:
            self._set_data(key=_Keys.OPTIONS, value={}, set_default_type=Dict)
        else:
            self._set_data(key=_Keys.OPTIONS, value=value, set_default_type=Dict)

    @property
    def __system_url(self) -> str:
        return self._get_data(key=_Keys.SYSTEM_URL)  # type: ignore

    @property
    def __systems_url(self) -> str:
        return self._get_data(key=_Keys.SYSTEMS_URL)  # type: ignore

    @property
    def options(self) -> str:
        """Get url options string."""
        out: str = ""
        for key, value in self.__options.items():
            out += f"&{key}={value}"
        return out

    def bodies_url(self, s_system: StarsSystem) -> str:
        """Returns proper API url for getting bodies information data."""
        if not isinstance(s_system, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(s_system)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )

        if s_system.name:
            return requote_uri(f"{self.__system_url}bodies?systemName={s_system.name}")
        if s_system.address:
            return requote_uri(f"{self.__system_url}bodies?systemId={s_system.address}")
        return ""

    def system_url(self, s_system: StarsSystem) -> str:
        """Returns proper API url for getting system data."""
        if not isinstance(s_system, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(s_system)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )

        if s_system.name:
            return requote_uri(
                f"{self.__systems_url}system?systemName={s_system.name}{self.options}"
            )
        return ""

    def radius_url(self, s_system: StarsSystem, radius: int) -> str:
        """Returns proper API url for getting systems data in radius."""
        if not isinstance(s_system, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(s_system)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(radius, int):
            radius = 50
        else:
            if radius < 5:
                radius = 5
            elif radius > 100:
                radius = 100

        if s_system.name:
            return requote_uri(
                f"{self.__systems_url}sphere-systems?systemName={s_system.name}&radius={radius}{self.options}"
            )
        return ""

    def cube_url(self, s_system: StarsSystem, size: int) -> str:
        """Returns proper API url for getting systems data in radius."""
        if not isinstance(s_system, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(s_system)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(size, int):
            size = 100
        else:
            if size < 10:
                size = 10
            elif size > 200:
                size = 200

        if s_system.name:
            return requote_uri(
                f"{self.__systems_url}cube-systems?systemName={s_system.name}&size={size}{self.options}"
            )
        return ""

    def system_query(self, s_system: StarsSystem) -> Optional[Dict]:
        """Returns result of query for system data."""
        if not isinstance(s_system, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(s_system)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        url: str = self.system_url(s_system)
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

    def url_query(self, url: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Returns result of query for url."""
        out = []
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


# #[EOF]#######################################################################
