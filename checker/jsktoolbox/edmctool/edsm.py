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

from typing import Dict, List, Optional, Any
from requests.utils import requote_uri  # type: ignore
from inspect import currentframe


from ..basetool.data import BData
from ..attribtool import ReadOnlyClass
from ..raisetool import Raise
from ..edmctool.stars import StarsSystem


class EdsmKeys(object, metaclass=ReadOnlyClass):
    """EDSM API Keys container class."""

    ABSOLUTE_MAGNITUDE: str = "absoluteMagnitude"
    AGE: str = "age"
    ALLEGIANCE: str = "allegiance"
    API_KEY: str = "apiKey"
    ARG_OF_PERIAPSIS: str = "argOfPeriapsis"
    AXIAL_TILT: str = "axialTilt"
    BODIES: str = "bodies"
    BODY_COUNT: str = "bodyCount"
    BODY_ID: str = "bodyId"
    BODY_NAME: str = "bodyName"
    BREAKDOWN: str = "breakdown"
    CARGO: str = "cargo"
    COMMANDER_NAME: str = "commanderName"
    COMMENT: str = "comment"
    CONTROLLING_FACTION: str = "controllingFaction"
    COORDS: str = "coords"
    COORDS_LOCKED: str = "coordsLocked"
    CREDITS: str = "credits"
    DATA: str = "data"
    DATE: str = "date"
    DAY: str = "day"
    DEATHS: str = "deaths"
    DISTANCE: str = "distance"
    DISTANCE_TO_ARRIVAL: str = "distanceToArrival"
    DUPLICATES: str = "duplicates"
    ECONOMY: str = "economy"
    END_DATE_TIME: str = "endDateTime"
    ESTIMATED_VALUE: str = "estimatedValue"
    ESTIMATED_VALUE_MAPPED: str = "estimatedValueMapped"
    FACTION: str = "faction"
    FACTION_STATE: str = "factionState"
    FIRST_DISCOVER: str = "firstDiscover"
    FROM_GAME_BUILD: str = "fromGameBuild"
    FROM_GAME_VERSION: str = "fromGameVersion"
    FROM_SOFTWARE: str = "fromSoftware"
    FROM_SOFTWARE_VERSION: str = "fromSoftwareVersion"
    GOVERNMENT: str = "government"
    HAVE_MARKET: str = "haveMarket"
    HAVE_SHIPYARD: str = "haveShipyard"
    HIDDEN_AT: str = "hidden_at"
    ID: str = "id"
    ID64: str = "id64"
    INCLUDE_HIDDEN: str = "includeHidden"
    INFLUENCE: str = "influence"
    INFLUENCE_HISTORY: str = "influenceHistory"
    INFORMATION: str = "information"
    INNER_RADIUS: str = "innerRadius"
    IS_MAIN_STAR: str = "isMainStar"
    IS_PLAYER: str = "isPlayer"
    IS_SCOOPABLE: str = "isScoopable"
    LAST_UPDATE: str = "lastUpdate"
    LOGS: str = "logs"
    LUMINOSITY: str = "luminosity"
    MARKET_ID: str = "marketId"
    MATERIALS: str = "materials"
    MERGED_TO: str = "mergedTo"
    MESSAGE: str = "message"
    MIN_RADIUS: str = "minRadius"
    MSG: str = "msg"
    MSG_NUM: str = "msgnum"
    NAME: str = "name"
    ONLY_KNOWN_COORDINATES: str = "onlyKnownCoordinates"
    ONLY_UNKNOWN_COORDINATES: str = "onlyUnknownCoordinates"
    ORBITAL_ECCENTRICITY: str = "orbitalEccentricity"
    ORBITAL_INCLINATION: str = "orbitalInclination"
    ORBITAL_PERIOD: str = "orbitalPeriod"
    OUTER_RADIUS: str = "outerRadius"
    PENDING_STATES: str = "pendingStates"
    PERIOD: str = "period"
    PERMIT_NAME: str = "permitName"
    POPULATION: str = "population"
    PROGRESS: str = "progress"
    QTY: str = "qty"
    RADIUS: str = "radius"
    RANKS: str = "ranks"
    RANKS_VERBOSE: str = "ranksVerbose"
    RECOVERING_STATES: str = "recoveringStates"
    REQUIRE_PERMIT: str = "requirePermit"
    RINGS: str = "rings"
    ROTATIONAL_PERIOD: str = "rotationalPeriod"
    ROTATIONAL_PERIOD_TIDALLY_LOCKED: str = "rotationalPeriodTidallyLocked"
    SECURITY: str = "security"
    SEMI_MAJOR_AXIS: str = "semiMajorAxis"
    SHIP_ID: str = "shipId"
    SHOW_COORDINATES: str = "showCoordinates"
    SHOW_HISTORY: str = "showHistory"
    SHOW_ID: str = "showId"
    SHOW_INFORMATION: str = "showInformation"
    SHOW_PERMIT: str = "showPermit"
    SHOW_PRIMARY_STAR: str = "showPrimaryStar"
    SIZE: str = "size"
    SOLAR_MASSES: str = "solarMasses"
    SOLAR_RADIUS: str = "solarRadius"
    START_DATE_TIME: str = "startDateTime"
    STATE: str = "state"
    STATE_HISTORY: str = "stateHistory"
    STATIONS: str = "stations"
    STATION_NAME: str = "stationName"
    STATUS: str = "status"
    SUB_TYPE: str = "subType"
    SURFACE_TEMPERATURE: str = "surfaceTemperature"
    SYSTEM: str = "system"
    SYSTEM_ID: str = "systemId"
    SYSTEM_NAME: str = "systemName"
    TOTAL: str = "total"
    TRAFFIC: str = "traffic"
    TREND: str = "trend"
    TYPE: str = "type"
    URL: str = "url"
    VALUABLE_BODIES: str = "valuableBodies"
    VALUE_MAX: str = "valueMax"
    WEEK: str = "week"
    X: str = "x"
    Y: str = "y"
    Z: str = "z"
    _MARKET_ID: str = "_marketId"
    _SHIP_ID: str = "_shipId"
    _STATION_NAME: str = "_stationName"
    _SYSTEM_ADDRESS: str = "_systemAddress"
    _SYSTEM_COORDINATES: str = "_systemCoordinates"
    _SYSTEM_NAME: str = "_systemName"


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

        if s_system.address:
            return requote_uri(
                f"{self.__system_url}bodies?systemId={s_system.address}{self.options}"
            )
        if s_system.name:
            return requote_uri(
                f"{self.__system_url}bodies?systemName={s_system.name}{self.options}"
            )
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

    def url_query(self, url: str) -> List[Dict[str, Any]]:
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
