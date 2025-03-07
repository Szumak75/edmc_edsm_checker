# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.12.2023

Purpose: RB '/port/'
"""


from typing import Optional, Dict, Any

from ....logstool.queue import LoggerQueue

from ....attribtool import ReadOnlyClass
from ....logstool.logs import LoggerClient
from ..base import BRouterOS, BDev
from ...network.connectors import IConnector


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    FIRMWARE: str = "firmware"
    REMOTE_ACCESS: str = "remote-access"
    ROOT: str = "port"


class RBPort(BRouterOS):
    """Port class

    For command root: /port/
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
        elements: Dict[str, Any] = {_Elements.FIRMWARE: {}, _Elements.REMOTE_ACCESS: {}}

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
