# -*- coding: UTF-8 -*-
"""
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 22.12.2023, 12:35:53

Purpose: RB: /ipv6/
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

    ADDRESS: str = "address"
    ADDRESS_LIST: str = "address-list"
    BINDING: str = "binding"
    CONNECTION: str = "connection"
    DEFAULT: str = "default"
    DHCP_CLIENT: str = "dhcp-client"
    DHCP_RELAY: str = "dhcp-relay"
    DHCP_SERVER: str = "dhcp-server"
    FILTER: str = "filter"
    FIREWALL: str = "firewall"
    MANGLE: str = "mangle"
    NAT: str = "nat"
    ND: str = "nd"
    NEIGHBOR: str = "neighbor"
    OPTION: str = "option"
    POOL: str = "pool"
    PREFIX: str = "prefix"
    RAW: str = "raw"
    ROOT: str = "ipv6"
    ROUTE: str = "route"
    SETS: str = "sets"
    SETTINGS: str = "settings"
    USED: str = "used"


class RBIpv6(BRouterOS):
    """IPv6 class

    For command root: /ipv6/
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
            _Elements.ADDRESS: {},
            _Elements.DHCP_CLIENT: {_Elements.OPTION: {}},
            _Elements.DHCP_RELAY: {},
            _Elements.DHCP_SERVER: {
                _Elements.BINDING: {},
                _Elements.OPTION: {_Elements.SETS: {}},
            },
            _Elements.FIREWALL: {
                _Elements.ADDRESS_LIST: {},
                _Elements.CONNECTION: {},
                _Elements.FILTER: {},
                _Elements.MANGLE: {},
                _Elements.NAT: {},
                _Elements.RAW: {},
            },
            _Elements.ND: {_Elements.PREFIX: {_Elements.DEFAULT: {}}},
            _Elements.NEIGHBOR: {},
            _Elements.POOL: {_Elements.USED: {}},
            _Elements.ROUTE: {},
            _Elements.SETTINGS: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
