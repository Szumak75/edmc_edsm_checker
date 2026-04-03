# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-10-05

Purpose: Provide multi-platform clipboard helpers that wrap GUI-specific APIs.

The module exposes per-platform tool adapters that normalise clipboard access,
allowing the higher-level tool to select an available backend at runtime.
"""

import ctypes
import os
import platform
import tkinter as tk
import time

from abc import ABC, abstractmethod
from inspect import currentframe
from typing import Callable, Optional, Union
from types import MethodType

from ..basetool.data import BData
from ..attribtool import ReadOnlyClass
from ..raisetool import Raise
from .base import TkBase


class _IClip(ABC):
    """Abstract clipboard interface.

    Defines the contract for platform-specific clipboard helpers that provide
    consistent get and set operations across environments.
    """

    @abstractmethod
    def get_clipboard(self) -> str:
        """Retrieve the current clipboard text.

        Implementations must return Unicode text or an empty string when the
        clipboard is empty or inaccessible.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Text currently stored on the clipboard.

        ### Raises:
        * RuntimeError: Raised when clipboard access fails in a concrete backend.
        """

    @abstractmethod
    def set_clipboard(self, value: str) -> None:
        """Store text data in the clipboard.

        ### Arguments:
        * value: str - Text payload that should be placed on the clipboard.

        ### Returns:
        None - This method performs side effects only.

        ### Raises:
        * RuntimeError: Raised when clipboard access fails in a concrete backend.
        """

    @property
    @abstractmethod
    def is_tool(self) -> bool:
        """Report whether the clipboard backend is available.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        bool - True when the backend is operational.

        ### Raises:
        * None: Availability checks do not raise exceptions.
        """


class _Keys(object, metaclass=ReadOnlyClass):
    """Immutable key container.

    Stores keyword constants and platform identifiers used by clipboard helpers.
    """

    COPY: str = "_copy_"
    DARWIN: str = "Darwin"
    LINUX: str = "Linux"
    MAC: str = "mac"
    NT: str = "nt"
    PASTE: str = "_paste_"
    POSIX: str = "posix"
    TOOL: str = "_tool_"
    WINDOWS: str = "Windows"


class _BClip(BData, _IClip):
    """Base clipboard storage helper.

    Provides default get/set implementations that dispatch to backend handlers
    collected by subclasses.
    """

    def get_clipboard(self) -> str:
        """Get clipboard content.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard text or an empty string when no backend is available.

        ### Raises:
        * None: Backend availability is verified before access.
        """
        if self.is_tool:
            return self._get_data(key=_Keys.PASTE)()  # type: ignore
        return ""

    def set_clipboard(self, value: str) -> None:
        """Set clipboard content.

        ### Arguments:
        * value: str - Text payload to push onto the clipboard.

        ### Returns:
        None - This method performs side effects only.

        ### Raises:
        * None: Backend availability is verified before access.
        """
        if self.is_tool:
            self._get_data(key=_Keys.COPY)(value)  # type: ignore

    @property
    def is_tool(self) -> bool:
        """Return True if the tool is available.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        bool - True when both copy and paste callbacks are registered.

        ### Raises:
        * None: Availability checks do not raise exceptions.
        """
        return (
            self._get_data(key=_Keys.COPY) is not None
            and self._get_data(key=_Keys.PASTE) is not None
        )


class _WinClip(_BClip):
    """Windows clipboard class.

    Provides ctypes-based access to the native Windows clipboard APIs.
    """

    _CF_UNICODETEXT: int = 13
    _GMEM_MOVEABLE: int = 0x0002
    _UNICODE_NULL: int = 2  # two bytes for UTF-16LE terminator

    def __init__(self) -> None:
        """Initialise clipboard helpers for the Windows platform.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Failures are handled by skipping backend registration.
        """
        # https://stackoverflow.com/questions/101128/how-do-i-read-text-from-the-windows-clipboard-in-python

        if os.name == _Keys.NT or platform.system() == _Keys.WINDOWS:
            get_cb = self.__win_get_clipboard
            set_cb = self.__win_set_clipboard
            self._set_data(
                key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
            )
            self._set_data(
                key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
            )

    def __win_get_clipboard(self) -> str:
        """Return Unicode clipboard contents from the Windows clipboard.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard content decoded from UTF-16LE memory blocks.

        ### Raises:
        * RuntimeError: Raised when Windows clipboard APIs fail.
        """
        if not ctypes.windll.user32.OpenClipboard(0):  # type: ignore
            raise Raise.error(
                "Unable to open Windows clipboard.",
                RuntimeError,
                self._c_name,
                currentframe(),
            )
        try:
            handle = ctypes.windll.user32.GetClipboardData(self._CF_UNICODETEXT)  # type: ignore
            if not handle:
                return ""
            pointer = ctypes.windll.kernel32.GlobalLock(handle)  # type: ignore
            if not pointer:
                return ""
            try:
                text = ctypes.wstring_at(pointer)
                return text or ""
            finally:
                ctypes.windll.kernel32.GlobalUnlock(handle)  # type: ignore
        finally:
            ctypes.windll.user32.CloseClipboard()  # type: ignore

    def __win_set_clipboard(self, text: str) -> None:
        """Store Unicode clipboard data on Windows.

        ### Arguments:
        * text: str - Text payload encoded as UTF-16LE before storing.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * MemoryError: Raised when global memory allocation fails.
        * RuntimeError: Raised when Windows clipboard APIs fail.
        """
        value = str(text)
        encoded = value.encode("utf-16-le")
        size = len(encoded) + self._UNICODE_NULL
        if not ctypes.windll.user32.OpenClipboard(0):  # type: ignore
            raise Raise.error(
                "Unable to open Windows clipboard.",
                RuntimeError,
                self._c_name,
                currentframe(),
            )
        try:
            ctypes.windll.user32.EmptyClipboard()  # type: ignore
            handle = ctypes.windll.kernel32.GlobalAlloc(self._GMEM_MOVEABLE, size)  # type: ignore
            if not handle:
                raise Raise.error(
                    "Unable to allocate global memory for clipboard.",
                    MemoryError,
                    self._c_name,
                    currentframe(),
                )
            pointer = ctypes.windll.kernel32.GlobalLock(handle)  # type: ignore
            if not pointer:
                ctypes.windll.kernel32.GlobalFree(handle)  # type: ignore
                raise Raise.error(
                    "Unable to lock global memory for clipboard.",
                    RuntimeError,
                    self._c_name,
                    currentframe(),
                )
            try:
                ctypes.memmove(pointer, encoded, len(encoded))  # type: ignore
                ctypes.memset(pointer + len(encoded), 0, self._UNICODE_NULL)  # type: ignore
            finally:
                ctypes.windll.kernel32.GlobalUnlock(handle)  # type: ignore
            ctypes.windll.user32.SetClipboardData(self._CF_UNICODETEXT, handle)  # type: ignore
        finally:
            ctypes.windll.user32.CloseClipboard()  # type: ignore


class _MacClip(_BClip):
    """macOS clipboard class.

    Wraps the pbcopy/pbpaste utilities to interoperate with the system clipboard.
    """

    def __init__(self) -> None:
        """Initialise the macOS clipboard backend.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable if initialisation fails.
        """
        if os.name == _Keys.MAC or platform.system() == _Keys.DARWIN:
            get_cb = self.__mac_get_clipboard
            set_cb = self.__mac_set_clipboard
            self._set_data(
                key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
            )
            self._set_data(
                key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
            )

    def __mac_set_clipboard(self, text: str) -> None:
        """Set macOS clipboard data.

        ### Arguments:
        * text: str - Text payload forwarded to the `pbcopy` command.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        text = str(text)
        out_f: os._wrap_close = os.popen("pbcopy", "w")
        out_f.write(text)
        out_f.close()

    def __mac_get_clipboard(self) -> str:
        """Get macOS clipboard data.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard content produced by the `pbpaste` command.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        out_f: os._wrap_close = os.popen("pbpaste", "r")
        content: str = out_f.read()
        out_f.close()
        return content


class _XClip(_BClip):
    """X11 clipboard class.

    Integrates with the `xclip` command-line tool when it is available.
    """

    def __init__(self) -> None:
        """Initialise the xclip backend.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable when the command is missing.
        """
        if os.name == _Keys.POSIX or platform.system() == _Keys.LINUX:
            if os.system("which xclip > /dev/null") == 0:
                get_cb = self.__xclip_get_clipboard
                set_cb = self.__xclip_set_clipboard
                self._set_data(
                    key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
                )
                self._set_data(
                    key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
                )

    def __xclip_set_clipboard(self, text: str) -> None:
        """Set xclip clipboard data.

        ### Arguments:
        * text: str - Text payload forwarded to the `xclip` command.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        text = str(text)
        out_f: os._wrap_close = os.popen("xclip -selection c", "w")
        out_f.write(text)
        out_f.close()

    def __xclip_get_clipboard(self) -> str:
        """Get xclip clipboard data.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard content produced by the `xclip` command.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        out_f: os._wrap_close = os.popen("xclip -selection c -o", "r")
        content: str = out_f.read()
        out_f.close()
        return content


class _XSel(_BClip):
    """X11 clipboard class.

    Integrates with the `xsel` command-line tool when it is available.
    """

    def __init__(self) -> None:
        """Initialise the xsel backend.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable when the command is missing.
        """
        if os.name == _Keys.POSIX or platform.system() == _Keys.LINUX:
            if os.system("which xsel > /dev/null") == 0:
                get_cb = self.__xsel_get_clipboard
                set_cb = self.__xsel_set_clipboard
                self._set_data(
                    key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
                )
                self._set_data(
                    key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
                )

    def __xsel_set_clipboard(self, text: str) -> None:
        """Set xsel clipboard data.

        ### Arguments:
        * text: str - Text payload forwarded to the `xsel` command.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        text = str(text)
        out_f: os._wrap_close = os.popen("xsel -b -i", "w")
        out_f.write(text)
        out_f.close()

    def __xsel_get_clipboard(self) -> str:
        """Get xsel clipboard data.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard content produced by the `xsel` command.

        ### Raises:
        * None: Errors surface via the underlying shell command.
        """
        out_f: os._wrap_close = os.popen("xsel -b -o", "r")
        content: str = out_f.read()
        out_f.close()
        return content


class _GtkClip(_BClip):
    """Gtk clipboard class.

    Uses the Gtk clipboard API when the bindings are available.
    """

    def __init__(self) -> None:
        """Initialise the Gtk backend.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable when Gtk cannot be imported.
        """
        try:
            import gtk  # type: ignore

            get_cb = self.__gtk_get_clipboard
            set_cb = self.__gtk_set_clipboard
            self._set_data(
                key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
            )
            self._set_data(
                key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
            )
        except Exception:
            pass

    def __gtk_get_clipboard(self) -> str:
        """Get GTK clipboard data.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard text retrieved via the Gtk clipboard.

        ### Raises:
        * RuntimeError: Raised when Gtk fails to supply clipboard text.
        """
        return gtk.Clipboard().wait_for_text()  # type: ignore

    def __gtk_set_clipboard(self, text: str) -> None:
        """Set GTK clipboard data.

        ### Arguments:
        * text: str - Text payload to store via the Gtk clipboard.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * RuntimeError: Raised when Gtk fails to update clipboard text.
        """
        global cb
        text = str(text)
        cb = gtk.Clipboard()  # type: ignore
        cb.set_text(text)
        cb.store()


class _QtClip(_BClip):
    """Qt clipboard class.

    Creates or reuses a QApplication and routes clipboard operations through Qt APIs.
    """

    __app = None
    __cb = None

    def __init__(self) -> None:
        """Initialise the Qt clipboard backend.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable when Qt bindings cannot be imported.
        """
        try:
            # TODO: PyQt5
            # example: https://pythonprogramminglanguage.com/pyqt-clipboard/
            from PyQt5.QtCore import QCoreApplication
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtGui import QClipboard

            # QApplication is a singleton
            if not QApplication.instance():
                self.__app: Optional[Union[QApplication, QCoreApplication]] = (
                    QApplication([])
                )
            else:
                self.__app = QApplication.instance()

            self.__cb: Optional[QClipboard] = QApplication.clipboard()
            get_cb = self.__qt_get_clipboard
            set_cb = self.__qt_set_clipboard
            self._set_data(
                key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
            )
            self._set_data(
                key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
            )
        except Exception:
            try:
                from PyQt6.QtCore import QCoreApplication
                from PyQt6.QtWidgets import QApplication
                from PyQt6.QtGui import QClipboard

                # QApplication is a singleton
                if not QApplication.instance():
                    self.__app: Optional[Union[QApplication, QCoreApplication]] = (
                        QApplication([])
                    )
                else:
                    self.__app = QApplication.instance()

                self.__cb: Optional[QClipboard] = QApplication.clipboard()
                get_cb = self.__qt_get_clipboard
                set_cb = self.__qt_set_clipboard
                self._set_data(
                    key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
                )
                self._set_data(
                    key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
                )
            except Exception:
                pass

    def __qt_get_clipboard(self) -> str:
        """Get Qt clipboard data.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard text retrieved from the Qt clipboard instance.

        ### Raises:
        * None: Errors propagate from Qt when they occur.
        """
        if self.__cb:
            return str(self.__cb.text())
        return ""

    def __qt_set_clipboard(self, text: str) -> None:
        """Set Qt clipboard data.

        ### Arguments:
        * text: str - Text payload to store on the Qt clipboard.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * None: Errors propagate from Qt when they occur.
        """
        if self.__cb:
            text = str(text)
            self.__cb.setText(text)


class _TkClip(_BClip, TkBase):
    """Tkinter-based clipboard helper with hidden root management.

    Owns a hidden Tk root window to synchronise clipboard operations without exposing UI elements.
    """

    __tw: Optional[tk.Tk] = None
    __owns_root: bool = False

    def __init__(self) -> None:
        """Initialise Tk clipboard access or mark as unavailable.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend registration side effects.

        ### Raises:
        * None: Backend remains unavailable when Tk cannot initialise.
        """
        try:
            self.__tw = tk.Tk()
            self.__tw.withdraw()
            self.__owns_root = True
        except tk.TclError:
            self.__tw = None
            return

        if self.__tw:
            get_cb = self.__tkinter_get_clipboard
            set_cb = self.__tkinter_set_clipboard
            self._set_data(
                key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
            )
            self._set_data(
                key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
            )

    def __del__(self) -> None:  # pragma: no cover - destructor depends on GC
        if self.__owns_root and self.__tw is not None:
            try:
                self.__tw.destroy()
            except tk.TclError:
                pass
            self.__tw = None

    def __tkinter_get_clipboard(self) -> str:
        """Return clipboard text via Tkinter APIs.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        str - Clipboard text retrieved from the Tkinter root or an empty string when unavailable.

        ### Raises:
        * None: Tkinter exceptions are handled internally.
        """
        if self.__tw is None:
            return ""
        try:
            return self.__tw.clipboard_get()  # type: ignore[no-any-return]
        except tk.TclError:
            return ""

    def __tkinter_set_clipboard(self, text: str) -> None:
        """Store clipboard text via Tkinter APIs.

        ### Arguments:
        * text: str - Text payload to place on the clipboard.

        ### Returns:
        None - Performs clipboard update side effects.

        ### Raises:
        * RuntimeError: Raised when Tkinter cannot set the clipboard content.
        """
        if self.__tw is None:
            return
        value = str(text)
        try:
            self.__tw.clipboard_clear()
            self.__tw.clipboard_append(value)
            self.__tw.update_idletasks()
            self.__tw.update()
            for _ in range(5):
                time.sleep(0.1)
                self.__tw.update()
                try:
                    if self.__tw.clipboard_get() == value:
                        break
                except tk.TclError:
                    continue
        except tk.TclError as exc:  # pragma: no cover - rare runtime failure
            raise Raise.error(
                f"Unable to set Tk clipboard content: {exc}",
                RuntimeError,
                self._c_name,
                currentframe(),
            )


class ClipBoard(BData):
    """System clipboard tool.

    Selects the first available platform backend and exposes copy/paste callables for clients.
    """

    __error: str = (
        "ClipBoard requires the xclip or the xsel command or gtk or PyQt4 module installed."
    )

    def __init__(self) -> None:
        """Initialise the aggregated clipboard tool.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs backend detection side effects.

        ### Raises:
        * None: Backend discovery failures are reported via messages.
        """
        for tool in (_XClip(), _XSel(), _GtkClip(), _QtClip(), _WinClip(), _MacClip()):
            if tool.is_tool:
                self._set_data(key=_Keys.TOOL, value=tool)
                break
        if not self.is_tool:
            print(
                Raise.message(
                    self.__error,
                    self._c_name,
                    currentframe(),
                )
            )

    @property
    def is_tool(self) -> bool:
        """Return True if the tool is available.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        bool - True when at least one backend is registered.

        ### Raises:
        * None: Availability checks do not raise exceptions.
        """
        if self._get_data(key=_Keys.TOOL, default_value=None):
            tool: _IClip = self._get_data(key=_Keys.TOOL)  # type: ignore
            return tool.is_tool
        return False

    @property
    def copy(self) -> Callable:
        """Return copy handler.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Callable - Function that copies text to the system clipboard.

        ### Raises:
        * None: Missing backends fall back to a no-op lambda.
        """
        if self.is_tool:
            return self._get_data(key=_Keys.TOOL).set_clipboard  # type: ignore
        print(
            Raise.message(
                self.__error,
                self._c_name,
                currentframe(),
            )
        )
        return lambda: ""

    @property
    def paste(self) -> Callable:
        """Return paste handler.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Callable - Function that retrieves text from the system clipboard.

        ### Raises:
        * None: Missing backends fall back to a no-op lambda.
        """
        if self.is_tool:
            return self._get_data(key=_Keys.TOOL).get_clipboard  # type: ignore
        print(
            Raise.message(
                self.__error,
                self._c_name,
                currentframe(),
            )
        )
        return lambda: ""


# #[EOF]#######################################################################
