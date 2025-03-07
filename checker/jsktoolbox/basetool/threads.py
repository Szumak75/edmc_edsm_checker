# -*- coding: utf-8 -*-
"""
threads.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 10:23:51

Purpose: Base class for classes derived from threading.Thread
"""

from io import TextIOWrapper
from time import sleep
from types import FunctionType
from typing import Any, Callable, Optional, Tuple, Dict
from threading import Event
from _thread import LockType

from .data import BData
from ..attribtool import ReadOnlyClass


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS: str = "_args"
    DAEMONIC: str = "_daemonic"
    DEBUG: str = "_debug"
    IDENT: str = "_ident"
    INVOKE_EXCEPTHOOK: str = "_invoke_excepthook"
    IS_STOPPED: str = "_is_stopped"
    KWARGS: str = "_kwargs"
    NAME: str = "_name"
    NATIVE_ID: str = "_native_id"
    SLEEP_PERIOD: str = "_sleep_period"
    STARTED: str = "_started"
    STDERR: str = "_stderr"
    STOP_EVENT: str = "_stop_event"
    TARGET: str = "_target"
    TSTATE_LOCK: str = "_tstate_lock"


class ThBaseObject(BData):
    """Base class for classes derived from threading.Thread.

    Definition of properties used in the threading library.
    """

    @property
    def _target(self) -> Optional[Callable]:
        return self._get_data(key=_Keys.TARGET, default_value=None)

    @_target.setter
    def _target(self, value: Optional[Callable]) -> None:
        self._set_data(
            key=_Keys.TARGET, value=value, set_default_type=Optional[Callable]
        )

    @property
    def _name(self) -> Optional[str]:
        return self._get_data(key=_Keys.NAME, default_value=None)

    @_name.setter
    def _name(self, value: Optional[str]) -> None:
        self._set_data(key=_Keys.NAME, value=value, set_default_type=Optional[str])

    @property
    def _args(self) -> Optional[Tuple]:
        return self._get_data(key=_Keys.ARGS, default_value=None)

    @_args.setter
    def _args(self, value: Tuple) -> None:
        self._set_data(key=_Keys.ARGS, value=value, set_default_type=Tuple)

    @property
    def _kwargs(self) -> Optional[Dict]:
        return self._get_data(key=_Keys.KWARGS, default_value=None)

    @_kwargs.setter
    def _kwargs(self, value: Dict) -> None:
        self._set_data(key=_Keys.KWARGS, value=value, set_default_type=Dict)

    @property
    def _daemonic(self) -> Optional[bool]:
        return self._get_data(key=_Keys.DAEMONIC, default_value=None)

    @_daemonic.setter
    def _daemonic(self, value: bool) -> None:
        self._set_data(key=_Keys.DAEMONIC, value=value, set_default_type=bool)

    @property
    def _debug(self) -> Optional[bool]:
        return self._get_data(key=_Keys.DEBUG, default_value=None)

    @_debug.setter
    def _debug(self, value: bool) -> None:
        self._set_data(key=_Keys.DEBUG, value=value, set_default_type=bool)

    @property
    def _ident(self) -> Optional[int]:
        return self._get_data(key=_Keys.IDENT, default_value=None)

    @_ident.setter
    def _ident(self, value: Optional[int]) -> None:
        self._set_data(key=_Keys.IDENT, value=value, set_default_type=Optional[int])

    @property
    def _native_id(self) -> Optional[int]:
        return self._get_data(key=_Keys.NATIVE_ID, default_value=None)

    @_native_id.setter
    def _native_id(self, value: Optional[int]) -> None:
        self._set_data(key=_Keys.NATIVE_ID, value=value, set_default_type=Optional[int])

    @property
    def _tstate_lock(self) -> Optional[LockType]:
        return self._get_data(key=_Keys.TSTATE_LOCK, default_value=None)

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        self._set_data(
            key=_Keys.TSTATE_LOCK, value=value, set_default_type=Optional[LockType]
        )

    @property
    def _started(self) -> Optional[Event]:
        return self._get_data(key=_Keys.STARTED, default_value=None)

    @_started.setter
    def _started(self, value: Event) -> None:
        self._set_data(key=_Keys.STARTED, value=value, set_default_type=Event)

    @property
    def _is_stopped(self) -> Optional[bool]:
        return self._get_data(key=_Keys.IS_STOPPED, default_value=None)

    @_is_stopped.setter
    def _is_stopped(self, value: bool) -> None:
        self._set_data(key=_Keys.IS_STOPPED, value=value, set_default_type=bool)

    @property
    def _stderr(self) -> Optional[TextIOWrapper]:
        return self._get_data(
            key=_Keys.STDERR,
            default_value=None,
        )

    @_stderr.setter
    def _stderr(self, value: Optional[TextIOWrapper]) -> None:
        self._set_data(key=_Keys.STDERR, value=value, set_default_type=TextIOWrapper)

    @property
    def _invoke_excepthook(self) -> Optional[FunctionType]:
        return self._get_data(
            key=_Keys.INVOKE_EXCEPTHOOK,
            default_value=None,
        )

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Optional[FunctionType]) -> None:
        self._set_data(
            key=_Keys.INVOKE_EXCEPTHOOK,
            value=value,
            set_default_type=FunctionType,
        )

    @property
    def _stop_event(self) -> Optional[Event]:
        """Return the stop event object, if set."""
        return self._get_data(key=_Keys.STOP_EVENT, default_value=None)

    @_stop_event.setter
    def _stop_event(self, obj: Event) -> None:
        """Set the stop event object."""
        self._set_data(key=_Keys.STOP_EVENT, value=obj, set_default_type=Event)

    @property
    def started(self) -> bool:
        """Whether the process has started."""
        if self._started is not None:
            return self._started.is_set()
        return False

    @property
    def stopped(self) -> bool:
        """Return stop event flag."""
        if self._stop_event:
            return self._stop_event.is_set()
        return True

    @property
    def sleep_period(self) -> float:
        """Return sleep period value."""
        return self._get_data(key=_Keys.SLEEP_PERIOD, default_value=1.0)  # type: ignore

    @sleep_period.setter
    def sleep_period(self, value: float) -> None:
        """Set sleep period value."""
        self._set_data(
            key=_Keys.SLEEP_PERIOD, value=float(value), set_default_type=float
        )

    def _sleep(self, sleep_period: Optional[float] = None) -> None:
        """Sleep the thread."""
        if sleep_period is None:
            sleep_period = self.sleep_period
        sleep(sleep_period)

    def stop(self) -> None:
        """Finish the thread."""
        if self._stop_event:
            self._stop_event.set()


# #[EOF]#######################################################################
