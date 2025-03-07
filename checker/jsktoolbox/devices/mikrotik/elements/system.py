# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: RB '/system/'
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

    ACTION: str = "action"
    BACKUP: str = "backup"
    CLIENT: str = "client"
    CLOCK: str = "clock"
    CLOUD: str = "cloud"
    CONSOLE: str = "console"
    CPU: str = "cpu"
    DEVICE_MODE: str = "device-mode"
    ENVIRONMENT: str = "environment"
    GAUGES: str = "gauges"
    HEALTH: str = "health"
    HISTORY: str = "history"
    IDENTITY: str = "identity"
    IRQ: str = "irq"
    JOB: str = "job"
    KEY: str = "key"
    LEDS: str = "leds"
    LICENSE: str = "license"
    LOGGING: str = "logging"
    MANUAL: str = "manual"
    NOTE: str = "note"
    NTP: str = "ntp"
    PACKAGE: str = "package"
    PCI: str = "pci"
    RESOURCE: str = "resource"
    ROOT: str = "system"
    ROUTERBOARD: str = "routerboard"
    SCHEDULER: str = "scheduler"
    SCRIPT: str = "script"
    SERVER: str = "server"
    SERVERS: str = "servers"
    SETTINGS: str = "settings"
    UPDATE: str = "update"
    UPGRADE: str = "upgrade"
    USB: str = "usb"
    WATCHDOG: str = "watchdog"


class RBSystem(BRouterOS):
    """System class

    For command root: /system/
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
            _Elements.BACKUP: {
                _Elements.CLOUD: {},
            },
            _Elements.CLOCK: {
                _Elements.MANUAL: {},
            },
            _Elements.CONSOLE: {},
            _Elements.DEVICE_MODE: {},
            _Elements.HEALTH: {
                _Elements.SETTINGS: {},
                _Elements.GAUGES: {},
            },
            _Elements.HISTORY: {},
            _Elements.IDENTITY: {},
            _Elements.LEDS: {
                _Elements.SETTINGS: {},
            },
            _Elements.LICENSE: {},
            _Elements.LOGGING: {
                _Elements.ACTION: {},
            },
            _Elements.NOTE: {},
            _Elements.NTP: {
                _Elements.CLIENT: {
                    _Elements.SERVERS: {},
                },
                _Elements.KEY: {},
                _Elements.SERVER: {},
            },
            _Elements.PACKAGE: {
                _Elements.UPDATE: {},
            },
            _Elements.RESOURCE: {
                _Elements.CPU: {},
                _Elements.IRQ: {},
                _Elements.PCI: {},
                _Elements.USB: {
                    _Elements.SETTINGS: {},
                },
            },
            _Elements.ROUTERBOARD: {
                _Elements.SETTINGS: {},
            },
            _Elements.SCHEDULER: {},
            _Elements.SCRIPT: {
                _Elements.ENVIRONMENT: {},
                _Elements.JOB: {},
            },
            _Elements.UPGRADE: {},
            _Elements.WATCHDOG: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
