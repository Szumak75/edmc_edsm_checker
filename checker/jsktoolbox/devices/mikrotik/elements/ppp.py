# -*- coding: UTF-8 -*-
"""
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 22.12.2023, 12:37:30

Purpose: RB: /ppp/
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

    AAA: str = "aaa"
    ACTIVE: str = "active"
    L2TP_SECRET: str = "l2tp-secret"
    PROFILE: str = "profile"
    ROOT: str = "ppp"
    SECRET: str = "secret"


class RBPpp(BRouterOS):
    """Ppp class

    For command root: /ppp/
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
            _Elements.AAA: {},
            _Elements.ACTIVE: {},
            _Elements.L2TP_SECRET: {},
            _Elements.PROFILE: {},
            _Elements.SECRET: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
