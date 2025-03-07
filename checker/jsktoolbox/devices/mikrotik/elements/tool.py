# -*- coding: UTF-8 -*-
"""
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 22.12.2023, 12:40:33

Purpose: RB: /tool/
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

    BANDWIDTH_SERVER: str = "bandwidth-server"
    CONNECTION: str = "connection"
    E_MAIL: str = "e-mail"
    GRAPHING: str = "graphing"
    HOST: str = "host"
    INBOX: str = "inbox"
    INTERFACE: str = "interface"
    LATENCY_DISTRIBUTION: str = "latency-distribution"
    MAC_SERVER: str = "mac-server"
    MAC_WINBOX: str = "mac-winbox"
    NETWATCH: str = "netwatch"
    PACKET: str = "packet"
    PACKET_TEMPLATE: str = "packet-template"
    PING: str = "ping"
    PORT: str = "port"
    PROTOCOL: str = "protocol"
    QUEUE: str = "queue"
    RAW: str = "raw"
    RAW_PACKET_TEMPLATE: str = "raw-packet-template"
    RESOURCE: str = "resource"
    ROMON: str = "romon"
    ROOT: str = "tool"
    SESSION: str = "session"
    SESSIONS: str = "sessions"
    SMS: str = "sms"
    SNIFFER: str = "sniffer"
    STATS: str = "stats"
    STREAM: str = "stream"
    TRAFFIC_GENERATOR: str = "traffic-generator"
    TRAFFIC_MONITOR: str = "traffic-monitor"


class RBTool(BRouterOS):
    """Tool class

    For command root: /tool/
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
            _Elements.BANDWIDTH_SERVER: {_Elements.SESSION: {}},
            _Elements.E_MAIL: {},
            _Elements.GRAPHING: {
                _Elements.INTERFACE: {},
                _Elements.QUEUE: {},
                _Elements.RESOURCE: {},
            },
            _Elements.MAC_SERVER: {
                _Elements.MAC_WINBOX: {},
                _Elements.PING: {},
                _Elements.SESSIONS: {},
            },
            _Elements.NETWATCH: {},
            _Elements.ROMON: {_Elements.PORT: {}},
            _Elements.SMS: {_Elements.INBOX: {}},
            _Elements.SNIFFER: {
                _Elements.CONNECTION: {},
                _Elements.HOST: {},
                _Elements.PACKET: {},
                _Elements.PROTOCOL: {},
            },
            _Elements.TRAFFIC_GENERATOR: {
                _Elements.PACKET_TEMPLATE: {},
                _Elements.PORT: {},
                _Elements.RAW_PACKET_TEMPLATE: {},
                _Elements.STATS: {
                    _Elements.LATENCY_DISTRIBUTION: {},
                    _Elements.PORT: {},
                    _Elements.RAW: {},
                    _Elements.STREAM: {},
                },
                _Elements.STREAM: {},
            },
            _Elements.TRAFFIC_MONITOR: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
