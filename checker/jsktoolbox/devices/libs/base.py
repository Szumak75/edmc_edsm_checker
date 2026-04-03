# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2023-12-04

Purpose: Provide foundational mixins for device abstractions, including shared
flags and connector plumbing.

These helpers keep higher-level device classes lightweight by centralising
parent management, logging integration, and RouterOS command prefix
composition.
"""

from typing import Optional, TypeVar
from inspect import currentframe


from ...attribtool import ReadOnlyClass
from ...raisetool import Raise
from ...logstool.logs import LoggerClient
from ...basetool.data import BData


from ..network.connectors import IConnector

TDev = TypeVar("TDev", bound="BDev")


class _Keys(object, metaclass=ReadOnlyClass):
    """Immutable container for data keys used by device helpers."""

    CH: str = "__connector_handler__"
    DEBUG: str = "__debug__"
    LC: str = "__logs_client__"
    PARENT: str = "__parent__"
    ROOT: str = "__root__"
    VERBOSE: str = "__verbose__"


class BDebug(BData):
    """Expose debug and verbose flags for device components."""

    @property
    def debug(self) -> bool:
        """Return debug flag.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        bool - True when debug logging is enabled for the device.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        return self._get_data(
            key=_Keys.DEBUG, set_default_type=bool, default_value=False
        )  # type: ignore

    @debug.setter
    def debug(self, debug: bool) -> None:
        """Set debug flag.

        ### Arguments:
        * debug: bool - New debug flag value.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * None: Setter does not raise exceptions.
        """
        self._set_data(key=_Keys.DEBUG, set_default_type=bool, value=debug)

    @property
    def verbose(self) -> bool:
        """Return verbose flag.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        bool - True when verbose logging is enabled.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        return self._get_data(
            key=_Keys.VERBOSE, set_default_type=bool, default_value=False
        )  # type: ignore

    @verbose.setter
    def verbose(self, verbose: bool) -> None:
        """Set verbose flag.

        ### Arguments:
        * verbose: bool - New verbose flag value.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * None: Setter does not raise exceptions.
        """
        self._set_data(key=_Keys.VERBOSE, set_default_type=bool, value=verbose)


class BDev(BDebug):
    """Coordinate connectors, logging, and parent relationships for devices."""

    @property
    def _ch(self) -> Optional[IConnector]:
        """Return the connector associated with this device.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Optional[IConnector] - Current connector or None when detached.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        return self._get_data(
            key=_Keys.CH,
            set_default_type=Optional[IConnector],
        )

    @_ch.setter
    def _ch(self, value: IConnector) -> None:
        """Attach a connector to the device.

        ### Arguments:
        * value: IConnector - Connector that should be used for communication.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * None: Setter does not perform validation beyond typing.
        """
        self._set_data(
            key=_Keys.CH,
            value=value,
            set_default_type=Optional[IConnector],
        )

    @property
    def logs(self) -> Optional[LoggerClient]:
        """Return the logger client registered for the device.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Optional[LoggerClient] - Configured logger client or None.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        return self._get_data(
            key=_Keys.LC,
            set_default_type=Optional[LoggerClient],
        )

    @logs.setter
    def logs(self, value: LoggerClient) -> None:
        """Assign a logger client to the device.

        ### Arguments:
        * value: LoggerClient - Logger client used for device diagnostics.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * None: Setter does not perform validation beyond typing.
        """
        self._set_data(
            key=_Keys.LC,
            value=value,
            set_default_type=Optional[LoggerClient],
        )

    @property
    def root(self) -> str:
        """Return the accumulated RouterOS command root for the device.

        The property aggregates the root path from all parents in the device
        hierarchy.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Command prefix for RouterOS requests.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        tmp: str = self._get_data(
            key=_Keys.ROOT, set_default_type=str, default_value=""
        )  # type: ignore

        if self.parent is not None:
            item: BDev = self.parent
            tmp = f"{item.root}{tmp}"
        return tmp

    @root.setter
    def root(self, value: str) -> None:
        """Set the RouterOS command root for the device.

        ### Arguments:
        * value: str - Command prefix specific to the device.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * TypeError: Raised when the provided value is not a string.
        """
        self._set_data(key=_Keys.ROOT, set_default_type=str, value=value)

    @property
    def parent(self) -> Optional[TDev]:
        """Return the parent device instance if assigned.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Optional[TDev] - Parent device or `None` for top-level elements.

        ### Raises:
        * None: Accessors do not raise exceptions.
        """
        return self._get_data(
            key=_Keys.PARENT,
            set_default_type=Optional[BDev],
            default_value=None,
        )

    @parent.setter
    def parent(self, value: Optional[TDev]) -> None:
        """Assign the parent device for the current instance.

        ### Arguments:
        * value: Optional[TDev] - Parent device or None.

        ### Returns:
        None - Updates internal state only.

        ### Raises:
        * TypeError: Raised when the provided value is not a BDev instance.
        """
        self._set_data(
            key=_Keys.PARENT,
            set_default_type=Optional[BDev],
            value=value,
        )


# #[EOF]#######################################################################
