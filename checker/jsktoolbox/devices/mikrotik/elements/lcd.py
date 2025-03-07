# -*- coding: UTF-8 -*-
"""
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 22.12.2023, 12:39:52

Purpose: RB: /lcd/
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

    INTERFACE: str = "interface"
    PAGES: str = "pages"
    PIN: str = "pin"
    ROOT: str = "lcd"
    SCREEN: str = "screen"


class RBLcd(BRouterOS):
    """Lcd class

    For command root: /lcd/
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
            _Elements.INTERFACE: {_Elements.PAGES: {}},
            _Elements.PIN: {},
            _Elements.SCREEN: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
