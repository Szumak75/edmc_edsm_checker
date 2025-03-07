# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.12.2023

Purpose: RB '/mpls/'
"""

from typing import Dict, Optional, Any

from ....logstool.queue import LoggerQueue

from ....attribtool import ReadOnlyClass
from ....logstool.logs import LoggerClient
from ..base import BRouterOS, BDev
from ...network.connectors import IConnector


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ACCEPT_FILTER: str = "accept-filter"
    ADVERTISE_FILTER: str = "advertise-filter"
    FLOW: str = "flow"
    FORWARDING_TABLE: str = "forwarding-table"
    INTERFACE: str = "interface"
    LDP: str = "ldp"
    LOCAL_MAPPING: str = "local-mapping"
    NEIGHBOR: str = "neighbor"
    PATH: str = "path"
    REMOTE_MAPPING: str = "remote-mapping"
    ROOT: str = "mpls"
    SETTINGS: str = "settings"
    TRAFFIC_ENG: str = "traffic-eng"
    TUNNEL: str = "tunnel"


class RBMpls(BRouterOS):
    """MPLS class

    For command root: /mpls/
    """

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        super().__init__(
            parent,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.root = f"{_Elements.ROOT}/"

        # add elements
        elements: Dict[str, Any] = {
            _Elements.FORWARDING_TABLE: {},
            _Elements.INTERFACE: {},
            _Elements.LDP: {
                _Elements.ACCEPT_FILTER: {},
                _Elements.ADVERTISE_FILTER: {},
                _Elements.INTERFACE: {},
                _Elements.LOCAL_MAPPING: {},
                _Elements.NEIGHBOR: {},
                _Elements.REMOTE_MAPPING: {},
            },
            _Elements.SETTINGS: {},
            _Elements.TRAFFIC_ENG: {
                _Elements.FLOW: {},
                _Elements.INTERFACE: {},
                _Elements.PATH: {},
                _Elements.TUNNEL: {},
            },
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
