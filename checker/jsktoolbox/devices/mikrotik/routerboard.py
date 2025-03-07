# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: MikroTik RouterOS main class.
"""

from typing import Dict, List, Optional, Union, Tuple, Any
from inspect import currentframe

from ...logstool.queue import LoggerQueue

from ...attribtool import NoDynamicAttributes, ReadOnlyClass
from ...raisetool import Raise
from ...logstool.logs import LoggerClient


from ...netaddresstool.ipv4 import (
    Address,
    Netmask,
    Network,
    SubNetwork,
)
from ...netaddresstool.ipv6 import (
    Address6,
    Network6,
    Prefix6,
    SubNetwork6,
)

from .base import BRouterOS, Element
from ..network.connectors import IConnector
from .elements.libs.interfaces import IElement
from .elements.certificate import RBCertificate
from .elements.disk import RBDisk
from .elements.file import RBFile
from .elements.interface import RBInterface
from .elements.ip import RBIp
from .elements.ipv6 import RBIpv6
from .elements.lcd import RBLcd
from .elements.log import RBLog
from .elements.mpls import RBMpls
from .elements.partitions import RBPartitions
from .elements.port import RBPort
from .elements.ppp import RBPpp
from .elements.queue import RBQueue
from .elements.radius import RBRadius
from .elements.routing import RBRouting
from .elements.snmp import RBSnmp
from .elements.system import RBSystem
from .elements.tool import RBTool
from .elements.user import RBUser


class _Elements(object, metaclass=ReadOnlyClass):
    """Internal keys class."""

    CERTIFICATE: str = "certificate"
    DISK: str = "disk"
    FILE: str = "file"
    INTERFACE: str = "interface"
    IP: str = "ip"
    IPV6: str = "ipv6"
    LCD: str = "lcd"
    LOG: str = "log"
    MPLS: str = "mpls"
    PARTITIONS: str = "partitions"
    PORT: str = "port"
    PPP: str = "ppp"
    QUEUE: str = "queue"
    RADIUS: str = "radius"
    ROUTING: str = "routing"
    SNMP: str = "snmp"
    SYSTEM: str = "system"
    TOOL: str = "tool"
    USER: str = "user"


class RouterBoard(BRouterOS):
    """MikroTik RouterBoard class."""

    system = None

    def __init__(
        self,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        super().__init__(
            None,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.root = "/"

        # add elements
        if self._ch is None:
            return None
        self.elements[_Elements.CERTIFICATE] = RBCertificate(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.DISK] = RBDisk(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.FILE] = RBFile(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.INTERFACE] = RBInterface(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IP] = RBIp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.IPV6] = RBIpv6(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LCD] = RBLcd(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.LOG] = RBLog(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.MPLS] = RBMpls(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PARTITIONS] = RBPartitions(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PORT] = RBPort(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.PPP] = RBPpp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.QUEUE] = RBQueue(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.RADIUS] = RBRadius(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.ROUTING] = RBRouting(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SNMP] = RBSnmp(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.SYSTEM] = RBSystem(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.TOOL] = RBTool(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )
        self.elements[_Elements.USER] = RBUser(
            parent=self,
            connector=self._ch,
            qlog=self.logs.logs_queue if self.logs is not None else None,
            debug=self.debug,
            verbose=self.verbose,
        )


# #[EOF]#######################################################################
