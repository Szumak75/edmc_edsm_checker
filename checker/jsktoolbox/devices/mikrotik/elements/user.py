# -*- coding: UTF-8 -*-
"""
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 22.12.2023, 12:41:06

Purpose: RB: /user/
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
    GROUP: str = "group"
    PRIVATE: str = "private"
    ROOT: str = "user"
    SETTINGS: str = "settings"
    SSH_KEYS: str = "ssh-keys"


class RBUser(BRouterOS):
    """User class

    For command root: /user/
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
            _Elements.GROUP: {},
            _Elements.SETTINGS: {},  # v7
            _Elements.SSH_KEYS: {_Elements.PRIVATE: {}},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
