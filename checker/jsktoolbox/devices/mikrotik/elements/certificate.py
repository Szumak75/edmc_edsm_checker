# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.12.2023

Purpose: RB '/certificate/'
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

    CRL: str = "crl"
    OTP: str = "otp"
    RA: str = "ra"
    REQUESTS: str = "requests"
    ROOT: str = "certificate"
    SCEP_SERVER: str = "scep-server"
    SETTINGS: str = "settings"


class RBCertificate(BRouterOS):
    """Certificate class

    For command root: /certificate/
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
            _Elements.CRL: {},
            _Elements.SCEP_SERVER: {
                _Elements.OTP: {},
                _Elements.RA: {},
                _Elements.REQUESTS: {},
            },
            _Elements.SETTINGS: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
