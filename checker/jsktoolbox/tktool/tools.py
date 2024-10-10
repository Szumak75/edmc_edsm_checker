# -*- coding: UTF-8 -*-
"""
  tools.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 5.10.2024, 14:26:16
  
  Purpose: 
"""

import ctypes
import os, platform

from inspect import currentframe
from typing import Any, Callable, Optional
from types import MethodType

from ..basetool.data import BData
from ..attribtool import ReadOnlyClass
from ..raisetool import Raise


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    COPY: str = "_copy_"
    DARWIN: str = "Darwin"
    LINUX: str = "Linux"
    MAC: str = "mac"
    NT: str = "nt"
    PASTE: str = "_paste_"
    POSIX: str = "posix"
    WINDOWS: str = "Windows"


class ClipBoard(BData):
    """System clipboard tool."""

    def __init__(self) -> None:
        """Create instance of class."""
        set_cb: Optional[Callable] = None
        get_cb: Optional[Callable] = None
        if os.name == _Keys.NT or platform.system() == _Keys.WINDOWS:
            get_cb = self.__win_get_clipboard
            set_cb = self.__win_set_clipboard
        elif os.name == _Keys.MAC or platform.system() == _Keys.DARWIN:
            get_cb = self.__mac_get_clipboard
            set_cb = self.__mac_set_clipboard
        elif os.name == _Keys.POSIX or platform.system() == _Keys.LINUX:
            xclipExists: bool = os.system("which xclip > /dev/null") == 0
            if xclipExists:
                get_cb = self.__xclip_get_clipboard
                set_cb = self.__xclip_set_clipboard
            else:
                xselExists: bool = os.system("which xsel > /dev/null") == 0
                if xselExists:
                    get_cb = self.__xsel_get_clipboard
                    set_cb = self.__xsel_set_clipboard
                try:
                    import gtk  # type: ignore

                    get_cb = self.__gtk_get_clipboard
                    set_cb = self.__gtk_set_clipboard
                except Exception:
                    try:
                        import PyQt4.QtCore  # type: ignore
                        import PyQt4.QtGui  # type: ignore

                        app = PyQt4.QApplication([])
                        cb = PyQt4.QtGui.QApplication.clipboard()
                        get_cb = self.__qt_get_clipboard
                        set_cb = self.__qt_set_clipboard
                    except:
                        print(
                            Raise.message(
                                "ClipBoard requires the gtk or PyQt4 module installed, or the xclip command.",
                                self._c_name,
                                currentframe(),
                            )
                        )
        self._set_data(
            key=_Keys.COPY, value=set_cb, set_default_type=Optional[MethodType]
        )
        self._set_data(
            key=_Keys.PASTE, value=get_cb, set_default_type=Optional[MethodType]
        )

    @property
    def is_tool(self) -> bool:
        """Return True if the tool is available."""
        return (
            self._get_data(key=_Keys.COPY, default_value=None) is not None
            and self._get_data(key=_Keys.PASTE, default_value=None) is not None
        )

    @property
    def copy(self) -> Callable:
        """Return copy handler."""
        return self._get_data(key=_Keys.COPY)  # type: ignore

    @property
    def paste(self) -> Callable:
        """Return paste handler."""
        return self._get_data(key=_Keys.PASTE)  # type: ignore

    def __win_get_clipboard(self) -> str:
        """Get windows clipboard data."""
        ctypes.windll.user32.OpenClipboard(0)  # type: ignore
        p_contents = ctypes.windll.user32.GetClipboardData(1)  # type: ignore # 1 is CF_TEXT
        data = ctypes.c_char_p(p_contents).value
        # ctypes.windll.kernel32.GlobalUnlock(p_contents)
        ctypes.windll.user32.CloseClipboard()  # type: ignore
        return data  # type: ignore

    def __win_set_clipboard(self, text: str) -> None:
        """Set windows clipboard data."""
        text = str(text)
        G_MEM_DDE_SHARE = 0x2000
        ctypes.windll.user32.OpenClipboard(0)  # type: ignore
        ctypes.windll.user32.EmptyClipboard()  # type: ignore
        try:
            # works on Python 2 (bytes() only takes one argument)
            hCd = ctypes.windll.kernel32.GlobalAlloc(  # type: ignore
                G_MEM_DDE_SHARE, len(bytes(text)) + 1  # type: ignore
            )
        except TypeError:
            # works on Python 3 (bytes() requires an encoding)
            hCd = ctypes.windll.kernel32.GlobalAlloc(  # type: ignore
                G_MEM_DDE_SHARE, len(bytes(text, "ascii")) + 1
            )
        pchData = ctypes.windll.kernel32.GlobalLock(hCd)  # type: ignore
        try:
            # works on Python 2 (bytes() only takes one argument)
            ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))  # type: ignore
        except TypeError:
            # works on Python 3 (bytes() requires an encoding)
            ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, "ascii"))
        ctypes.windll.kernel32.GlobalUnlock(hCd)  # type: ignore
        ctypes.windll.user32.SetClipboardData(1, hCd)  # type: ignore
        ctypes.windll.user32.CloseClipboard()  # type: ignore

    def __mac_set_clipboard(self, text: str) -> None:
        """Set MacOS clipboard data."""
        text = str(text)
        out_f: os._wrap_close = os.popen("pbcopy", "w")
        out_f.write(text)
        out_f.close()

    def __mac_get_clipboard(self) -> str:
        """Get MacOS clipboard data."""
        out_f: os._wrap_close = os.popen("pbpaste", "r")
        content: str = out_f.read()
        out_f.close()
        return content

    def __gtk_get_clipboard(self) -> str:
        """Get GTK clipboard data."""
        return gtk.Clipboard().wait_for_text()  # type: ignore

    def __gtk_set_clipboard(self, text: str) -> None:
        """Set GTK clipboard data."""
        global cb
        text = str(text)
        cb = gtk.Clipboard()  # type: ignore
        cb.set_text(text)
        cb.store()

    def __qt_get_clipboard(self) -> str:
        """Get QT clipboard data."""
        return str(cb.text())

    def __qt_set_clipboard(self, text: str) -> None:
        """Set QT clipboard data."""
        text = str(text)
        cb.setText(text)

    def __xclip_set_clipboard(self, text: str) -> None:
        """Set xclip clipboard data."""
        text = str(text)
        out_f: os._wrap_close = os.popen("xclip -selection c", "w")
        out_f.write(text)
        out_f.close()

    def __xclip_get_clipboard(self) -> str:
        """Get xclip clipboard data."""
        out_f: os._wrap_close = os.popen("xclip -selection c -o", "r")
        content: str = out_f.read()
        out_f.close()
        return content

    def __xsel_set_clipboard(self, text: str) -> None:
        """Set xsel clipboard data."""
        text = str(text)
        out_f: os._wrap_close = os.popen("xsel -i", "w")
        out_f.write(text)
        out_f.close()

    def __xsel_get_clipboard(self) -> str:
        """Get xsel clipboard data."""
        out_f: os._wrap_close = os.popen("xsel -o", "r")
        content: str = out_f.read()
        out_f.close()
        return content


# #[EOF]#######################################################################
