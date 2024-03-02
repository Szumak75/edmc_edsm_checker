# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 03.11.2023

  Purpose: Base class for classess derived from threading.Thread
"""

from inspect import currentframe
from typing import Any, Optional, Tuple, Dict
from threading import Event
from jsktoolbox.libs.base_data import BData
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS = "_args"
    DAEMONIC = "_daemonic"
    DEBUG = "_debug"
    IDENT = "_ident"
    INVOKE_EXCEPTHOOK = "_invoke_excepthook"
    IS_STOPPED = "_is_stopped"
    KWARGS = "_kwargs"
    NAME = "_name"
    NATIVE_ID = "_native_id"
    SLEEP_PERIOD = "_sleep_period"
    STARTED = "_started"
    STDERR = "_stderr"
    STOP_EVENT = "_stop_event"
    TARGET = "_target"
    TSTATE_LOCK = "_tstate_lock"


class ThBaseObject(BData, NoDynamicAttributes):
    """Base class for classes derived from threading.Thread.

    Definition of properties used in the threading library.
    """

    @property
    def _target(self) -> Optional[Any]:
        if _Keys.TARGET not in self._data:
            self._data[_Keys.TARGET] = None
        return self._data[_Keys.TARGET]

    @_target.setter
    def _target(self, value: Any) -> None:
        self._data[_Keys.TARGET] = value

    @property
    def _name(self) -> Optional[str]:
        if _Keys.NAME not in self._data:
            self._data[_Keys.NAME] = None
        return self._data[_Keys.NAME]

    @_name.setter
    def _name(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise Raise.error(
                f"Expected String type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.NAME] = value

    @property
    def _args(self) -> Optional[Tuple]:
        if _Keys.ARGS not in self._data:
            self._data[_Keys.ARGS] = None
        return self._data[_Keys.ARGS]

    @_args.setter
    def _args(self, value: Tuple) -> None:
        self._data[_Keys.ARGS] = value

    @property
    def _kwargs(self) -> Optional[Dict]:
        if _Keys.KWARGS not in self._data:
            self._data[_Keys.KWARGS] = None
        return self._data[_Keys.KWARGS]

    @_kwargs.setter
    def _kwargs(self, value: Dict) -> None:
        if value is not None and not isinstance(value, Dict):
            raise Raise.error(
                f"Expected Dict type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.KWARGS] = value

    @property
    def _daemonic(self) -> Optional[bool]:
        if _Keys.DAEMONIC not in self._data:
            self._data[_Keys.DAEMONIC] = None
        return self._data[_Keys.DAEMONIC]

    @_daemonic.setter
    def _daemonic(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Expected Boolean type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.DAEMONIC] = value

    @property
    def _debug(self) -> Optional[bool]:
        if _Keys.DEBUG not in self._data:
            self._data[_Keys.DEBUG] = None
        return self._data[_Keys.DEBUG]

    @_debug.setter
    def _debug(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Expected Boolean type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.DEBUG] = value

    @property
    def _ident(self) -> Optional[int]:
        if _Keys.IDENT not in self._data:
            self._data[_Keys.IDENT] = None
        return self._data[_Keys.IDENT]

    @_ident.setter
    def _ident(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise Raise.error(
                f"Expected Integer type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.IDENT] = value

    @property
    def _native_id(self) -> Optional[int]:
        if _Keys.NATIVE_ID not in self._data:
            self._data[_Keys.NATIVE_ID] = None
        return self._data[_Keys.NATIVE_ID]

    @_native_id.setter
    def _native_id(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise Raise.error(
                f"Expected Integer type, received '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.NATIVE_ID] = value

    @property
    def _tstate_lock(self) -> Optional[Any]:
        if _Keys.TSTATE_LOCK not in self._data:
            self._data[_Keys.TSTATE_LOCK] = None
        return self._data[_Keys.TSTATE_LOCK]

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        self._data[_Keys.TSTATE_LOCK] = value

    @property
    def _started(self) -> Optional[Event]:
        if _Keys.STARTED not in self._data:
            self._data[_Keys.STARTED] = None
        return self._data[_Keys.STARTED]

    @_started.setter
    def _started(self, value: Event) -> None:
        if value is not None and not isinstance(value, Event):
            raise Raise.error(
                f"Expected threading.Event type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.STARTED] = value

    @property
    def _is_stopped(self) -> Optional[bool]:
        if _Keys.IS_STOPPED not in self._data:
            self._data[_Keys.IS_STOPPED] = None
        return self._data[_Keys.IS_STOPPED]

    @_is_stopped.setter
    def _is_stopped(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                f"Expected Boolean type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.IS_STOPPED] = value

    @property
    def _stderr(self) -> Optional[Any]:
        if _Keys.STDERR not in self._data:
            self._data[_Keys.STDERR] = None
        return self._data[_Keys.STDERR]

    @_stderr.setter
    def _stderr(self, value: Any) -> None:
        self._data[_Keys.STDERR] = value

    @property
    def _invoke_excepthook(self) -> Optional[Any]:
        if _Keys.INVOKE_EXCEPTHOOK not in self._data:
            self._data[_Keys.INVOKE_EXCEPTHOOK] = None
        return self._data[_Keys.INVOKE_EXCEPTHOOK]

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Any) -> None:
        self._data[_Keys.INVOKE_EXCEPTHOOK] = value

    @property
    def _stop_event(self) -> Optional[Event]:
        if _Keys.STOP_EVENT not in self._data:
            self._data[_Keys.STOP_EVENT] = None
        return self._data[_Keys.STOP_EVENT]

    @_stop_event.setter
    def _stop_event(self, obj: Event) -> None:
        if obj is not None and not isinstance(obj, Event):
            raise Raise.error(
                f"Expected threading.Event type, received: '{type(obj)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.STOP_EVENT] = obj

    @property
    def is_stopped(self) -> Optional[bool]:
        return self._is_stopped

    @property
    def started(self) -> bool:
        if self._started is not None:
            return self._started.is_set()
        return False

    @property
    def sleep_period(self) -> float:
        """Return sleepperiod value."""
        if _Keys.SLEEP_PERIOD not in self._data:
            self._data[_Keys.SLEEP_PERIOD] = 1.0
        return self._data[_Keys.SLEEP_PERIOD]

    @sleep_period.setter
    def sleep_period(self, value: float) -> None:
        """Set sleepperiod value."""
        if not isinstance(value, float):
            raise Raise.error(
                f"Expected positive float type, received: '{value}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.SLEEP_PERIOD] = value


# #[EOF]#######################################################################
