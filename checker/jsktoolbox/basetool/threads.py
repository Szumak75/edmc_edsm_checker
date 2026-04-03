# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Offer foundational helpers for thread-based utilities.

Provides attribute containers mirroring `threading.Thread` internals so custom
thread implementations can share consistent state management behaviour.
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
    """Immutable constants describing thread attribute names."""

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
    """Base mixin mirroring attributes of `threading.Thread`."""

    @property
    def _target(self) -> Optional[Callable]:
        """Return the thread target callable.

        ### Returns:
        [Optional[Callable]] - Function executed by the thread.
        """
        return self._get_data(key=_Keys.TARGET, default_value=None)

    @_target.setter
    def _target(self, value: Optional[Callable]) -> None:
        """Assign the thread target callable.

        ### Arguments:
        * value: Optional[Callable] - Callable to execute or None.
        """
        self._set_data(
            key=_Keys.TARGET, value=value, set_default_type=Optional[Callable]
        )

    @property
    def _name(self) -> Optional[str]:
        """Return the thread name.

        ### Returns:
        [Optional[str]] - Name string or None.
        """
        return self._get_data(key=_Keys.NAME, default_value=None)

    @_name.setter
    def _name(self, value: Optional[str]) -> None:
        """Assign the thread name.

        ### Arguments:
        * value: Optional[str] - Thread name value.
        """
        self._set_data(key=_Keys.NAME, value=value, set_default_type=Optional[str])

    @property
    def _args(self) -> Optional[Tuple]:
        """Return positional arguments supplied to the target.

        ### Returns:
        [Optional[Tuple]] - Tuple with positional arguments.
        """
        return self._get_data(key=_Keys.ARGS, default_value=None)

    @_args.setter
    def _args(self, value: Tuple) -> None:
        """Assign positional arguments for the target callable.

        ### Arguments:
        * value: Tuple - Positional argument tuple.
        """
        self._set_data(key=_Keys.ARGS, value=value, set_default_type=Tuple)

    @property
    def _kwargs(self) -> Optional[Dict]:
        """Return keyword arguments for the target callable.

        ### Returns:
        [Optional[Dict]] - Keyword argument mapping.
        """
        return self._get_data(key=_Keys.KWARGS, default_value=None)

    @_kwargs.setter
    def _kwargs(self, value: Dict) -> None:
        """Assign keyword arguments for the target callable.

        ### Arguments:
        * value: Dict - Keyword argument dictionary.
        """
        self._set_data(key=_Keys.KWARGS, value=value, set_default_type=Dict)

    @property
    def _daemonic(self) -> Optional[bool]:
        """Return whether the thread runs as a daemon.

        ### Returns:
        [Optional[bool]] - Daemon flag or None.
        """
        return self._get_data(key=_Keys.DAEMONIC, default_value=None)

    @_daemonic.setter
    def _daemonic(self, value: bool) -> None:
        """Assign the daemon flag.

        ### Arguments:
        * value: bool - Daemon state.
        """
        self._set_data(key=_Keys.DAEMONIC, value=value, set_default_type=bool)

    @property
    def _debug(self) -> Optional[bool]:
        """Return the debug flag.

        ### Returns:
        [Optional[bool]] - Debug flag or None.
        """
        return self._get_data(key=_Keys.DEBUG, default_value=None)

    @_debug.setter
    def _debug(self, value: bool) -> None:
        """Assign the debug flag.

        ### Arguments:
        * value: bool - Debug state.
        """
        self._set_data(key=_Keys.DEBUG, value=value, set_default_type=bool)

    @property
    def _ident(self) -> Optional[int]:
        """Return the Python thread identifier.

        ### Returns:
        [Optional[int]] - Thread identifier or None when inactive.
        """
        return self._get_data(key=_Keys.IDENT, default_value=None)

    @_ident.setter
    def _ident(self, value: Optional[int]) -> None:
        """Assign the Python thread identifier.

        ### Arguments:
        * value: Optional[int] - Identifier value.
        """
        self._set_data(key=_Keys.IDENT, value=value, set_default_type=Optional[int])

    @property
    def _native_id(self) -> Optional[int]:
        """Return the native thread identifier where available.

        ### Returns:
        [Optional[int]] - Native identifier or None.
        """
        return self._get_data(key=_Keys.NATIVE_ID, default_value=None)

    @_native_id.setter
    def _native_id(self, value: Optional[int]) -> None:
        """Assign the native thread identifier.

        ### Arguments:
        * value: Optional[int] - Native thread ID.
        """
        self._set_data(key=_Keys.NATIVE_ID, value=value, set_default_type=Optional[int])

    @property
    def _tstate_lock(self) -> Optional[LockType]:
        """Return the thread state lock object.

        ### Returns:
        [Optional[LockType]] - Thread state lock or None.
        """
        return self._get_data(key=_Keys.TSTATE_LOCK, default_value=None)

    @_tstate_lock.setter
    def _tstate_lock(self, value: Any) -> None:
        """Assign the thread state lock object.

        ### Arguments:
        * value: Any - Lock-like object.
        """
        self._set_data(
            key=_Keys.TSTATE_LOCK, value=value, set_default_type=Optional[LockType]
        )

    @property
    def _started(self) -> Optional[Event]:
        """Return the event tracking thread start status.

        ### Returns:
        [Optional[Event]] - Event instance or None.
        """
        return self._get_data(key=_Keys.STARTED, default_value=None)

    @_started.setter
    def _started(self, value: Event) -> None:
        """Assign the start event value.

        ### Arguments:
        * value: Event - Event indicating thread start.
        """
        self._set_data(key=_Keys.STARTED, value=value, set_default_type=Event)

    @property
    def _is_stopped(self) -> Optional[bool]:
        """Return the cached stopped state flag.

        ### Returns:
        [Optional[bool]] - Boolean state or None.
        """
        return self._get_data(key=_Keys.IS_STOPPED, default_value=None)

    @_is_stopped.setter
    def _is_stopped(self, value: bool) -> None:
        """Assign the cached stopped state flag.

        ### Arguments:
        * value: bool - Stopped state.
        """
        self._set_data(key=_Keys.IS_STOPPED, value=value, set_default_type=bool)

    @property
    def _stderr(self) -> Optional[TextIOWrapper]:
        """Return the thread-specific stderr stream.

        ### Returns:
        [Optional[TextIOWrapper]] - Text IO wrapper or None.
        """
        return self._get_data(
            key=_Keys.STDERR,
            default_value=None,
        )

    @_stderr.setter
    def _stderr(self, value: Optional[TextIOWrapper]) -> None:
        """Assign the stderr stream.

        ### Arguments:
        * value: Optional[TextIOWrapper] - Stream or None.
        """
        self._set_data(key=_Keys.STDERR, value=value, set_default_type=TextIOWrapper)

    @property
    def _invoke_excepthook(self) -> Optional[FunctionType]:
        """Return the custom exception hook callable.

        ### Returns:
        [Optional[FunctionType]] - Callable or None.
        """
        return self._get_data(
            key=_Keys.INVOKE_EXCEPTHOOK,
            default_value=None,
        )

    @_invoke_excepthook.setter
    def _invoke_excepthook(self, value: Optional[FunctionType]) -> None:
        """Assign the custom exception hook.

        ### Arguments:
        * value: Optional[FunctionType] - Callable or None.
        """
        self._set_data(
            key=_Keys.INVOKE_EXCEPTHOOK,
            value=value,
            set_default_type=FunctionType,
        )

    @property
    def _stop_event(self) -> Optional[Event]:
        """Return the stop event object, if set.

        ### Returns:
        [Optional[Event]] - Stop event instance or None.
        """
        return self._get_data(key=_Keys.STOP_EVENT, default_value=None)

    @_stop_event.setter
    def _stop_event(self, obj: Event) -> None:
        """Set the stop event object.

        ### Arguments:
        * obj: Event - Event signaling stop requests.
        """
        self._set_data(key=_Keys.STOP_EVENT, value=obj, set_default_type=Event)

    @property
    def started(self) -> bool:
        """Return whether the thread has started.

        ### Returns:
        [bool] - True when the thread start event is set.
        """
        if self._started is not None:
            return self._started.is_set()
        return False

    @property
    def stopped(self) -> bool:
        """Return whether the stop event flag is set.

        ### Returns:
        [bool] - True when stop event exists and is set, otherwise False.
        """
        if self._stop_event:
            return self._stop_event.is_set()
        return True

    @property
    def sleep_period(self) -> float:
        """Return configured sleep period in seconds.

        ### Returns:
        [float] - Sleep interval value.
        """
        return self._get_data(key=_Keys.SLEEP_PERIOD, default_value=1.0)  # type: ignore

    @sleep_period.setter
    def sleep_period(self, value: float) -> None:
        """Set configured sleep period in seconds.

        ### Arguments:
        * value: float - Sleep interval value.
        """
        self._set_data(
            key=_Keys.SLEEP_PERIOD, value=float(value), set_default_type=float
        )

    def _sleep(self, sleep_period: Optional[float] = None) -> None:
        """Pause execution for the configured period.

        ### Arguments:
        * sleep_period: Optional[float] - Custom sleep duration override.
        """
        if sleep_period is None:
            sleep_period = self.sleep_period
        sleep(sleep_period)

    def stop(self) -> None:
        """Signal the stop event for the thread."""
        if self._stop_event:
            self._stop_event.set()


# #[EOF]#######################################################################
