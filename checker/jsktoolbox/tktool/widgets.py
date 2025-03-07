# -*- coding: utf-8 -*-
"""
widgets.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 10:42:01

Purpose: custom tkinter widgets.

VerticalScrolledFrame: https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
"""


import tkinter as tk
from tkinter import Toplevel, ttk
from typing import Any, Optional, List, Tuple, Union, Dict

from .base import TkBase


class StatusBarTkFrame(tk.Frame, TkBase):
    """Status bar widget."""

    __status: tk.StringVar = None  # type: ignore
    __status_label: tk.Label = None  # type: ignore
    __sizegrip: ttk.Sizegrip = None  # type: ignore

    def __init__(self, master: tk.Misc, *args, **kwargs) -> None:
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.__status = tk.StringVar()
        self.__status.set("Status Bar")
        self.__status_label = tk.Label(
            self, bd=1, relief=tk.FLAT, anchor=tk.W, textvariable=self.__status
        )
        self.__status_label.pack(
            side=tk.LEFT, fill=tk.X, expand=tk.TRUE, padx=5, pady=1
        )

        # size grip
        self.__sizegrip = ttk.Sizegrip(self)
        self.__sizegrip.pack(side=tk.RIGHT, anchor=tk.SE)

    def set(self, value: str) -> None:
        """Set status message."""
        self.__status.set(value)
        self.__status_label.update_idletasks()

    def clear(self) -> None:
        """Clear status message."""
        self.__status.set("")
        self.__status_label.update_idletasks()


class StatusBarTtkFrame(ttk.Frame, TkBase):
    """Status bar widget."""

    __status: tk.StringVar = None  # type: ignore
    __status_label: ttk.Label = None  # type: ignore
    __sizegrip: ttk.Sizegrip = None  # type: ignore

    def __init__(self, master: tk.Misc, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, master, *args, **kwargs)

        self.__status = tk.StringVar()
        self.__status.set("Status Bar")
        self.__status_label = ttk.Label(self, anchor=tk.W, textvariable=self.__status)
        self.__status_label.pack(
            side=tk.LEFT, fill=tk.X, expand=tk.TRUE, padx=5, pady=1
        )

        # size grip
        self.__sizegrip = ttk.Sizegrip(self)
        self.__sizegrip.pack(side=tk.RIGHT, anchor=tk.SE)

    def set(self, value: str) -> None:
        """Set status message."""
        self.__status.set(value)
        self.__status_label.update_idletasks()

    def clear(self) -> None:
        """Clear status message."""
        self.__status.set("")
        self.__status_label.update_idletasks()


class CreateToolTip(TkBase):
    """Create a tooltip for a given widget.

    Constructor:
    widget: tk.Misc -- Parent widget handler,
    text: Union[str, List[str], Tuple[str], tk.StringVar] -- text displayed in tooltip,
    wait_time: int -- delay of displaying tooltip [ms],
    wrap_length: int -- Limit the number of characters on each line to the specified value.
                    The default value of 0 means that lines will only be broken on newlines.
    """

    __id: Optional[str] = None
    __tw: Optional[tk.Toplevel] = None
    __wait_time: int = None  # type: ignore
    __widget: tk.Misc = None  # type: ignore
    __wrap_length: int = None  # type: ignore
    __text: Union[str, List[str], Tuple[str]] = None  # type: ignore
    __text_variable: tk.StringVar = None  # type: ignore
    __label_attr: Dict[str, Any] = None  # type: ignore

    def __init__(
        self,
        widget: tk.Misc,
        text: Union[str, List[str], Tuple[str], tk.StringVar] = "widget info",
        wait_time: int = 500,
        wrap_length: int = 0,
        **kwargs,
    ) -> None:
        """Create class object."""
        # set default attributes
        self.__label_attr = {
            "justify": tk.LEFT,
            "bg": "white",
            "relief": tk.SOLID,
            "borderwidth": 1,
        }
        # update attributes
        if kwargs:
            self.__label_attr.update(kwargs)

        self.__wait_time = wait_time
        self.__wrap_length = wrap_length
        self.__widget = widget

        # set message
        self.text = text
        self.__widget.bind("<Enter>", self.__enter)
        self.__widget.bind("<Leave>", self.__leave)
        self.__widget.bind("<ButtonPress>", self.__leave)

    def __enter(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Enter> event."""
        self.__schedule()

    def __leave(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Leave> event."""
        self.__unschedule()
        self.__hidetip()

    def __schedule(self) -> None:
        """Schedule method."""
        self.__unschedule()
        self.__id = self.__widget.after(self.__wait_time, self.__showtip)

    def __unschedule(self) -> None:
        """Unschedule method."""
        __id: Optional[str] = self.__id
        self.__id = None
        if __id:
            self.__widget.after_cancel(__id)

    def __showtip(self, event: Optional[tk.Event] = None) -> None:
        """Show tooltip."""
        __x: int = 0
        __y: int = 0
        __cx: int
        __cy: int
        __x, __y, __cx, __cy = self.__widget.bbox("insert")  # type: ignore
        __x += self.__widget.winfo_rootx() + 25
        __y += self.__widget.winfo_rooty() + 20
        # creates a toplevel window
        self.__tw = tk.Toplevel(self.__widget)
        # Leaves only the label and removes the app window
        self.__tw.wm_overrideredirect(True)
        self.__tw.wm_geometry(f"+{__x}+{__y}")
        label = tk.Label(
            self.__tw,
            wraplength=self.__wrap_length,
        )
        for key in self.__label_attr.keys():
            label[key.lower()] = self.__label_attr[key]
        if isinstance(self.text, tk.StringVar):
            label["textvariable"] = self.text
        else:
            label["text"] = self.text
        label.pack(ipadx=1)

    def __hidetip(self) -> None:
        """Hide tooltip."""
        __tw: Optional[Toplevel] = self.__tw
        self.__tw = None
        if __tw:
            __tw.destroy()

    @property
    def text(self) -> Union[str, tk.StringVar]:
        """Return text message."""
        if self.__text is None and self.__text_variable is None:
            self.__text = ""
        if self.__text_variable is None:
            if isinstance(self.__text, (List, Tuple)):
                tmp: str = ""
                for msg in self.__text:
                    tmp += msg if not tmp else f"\n{msg}"
                return tmp
            return self.__text
        else:
            return self.__text_variable

    @text.setter
    def text(self, value: Union[str, List[str], Tuple[str], tk.StringVar]) -> None:
        """Set text message object."""
        if isinstance(value, tk.StringVar):
            self.__text_variable = value
        else:
            self.__text = value


class VerticalScrolledTkFrame(tk.Frame, TkBase):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    __vscrollbar: tk.Scrollbar = None  # type: ignore
    __canvas: tk.Canvas = None  # type: ignore
    __interior: tk.Frame = None  # type: ignore
    __interior_id: int = None  # type: ignore

    def __init__(self, parent: tk.Misc, *args, **kw) -> None:
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self.__vscrollbar.set
        )
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.__vscrollbar.config(command=self.__canvas.yview)

        # Reset the view
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self.__interior = tk.Frame(self.__canvas)
        self.__interior_id: int = self.__canvas.create_window(
            0, 0, window=self.__interior, anchor=tk.NW
        )

        # Configure Events
        self.__interior.bind("<Configure>", self.__configure_interior)
        self.__canvas.bind("<Configure>", self.__configure_canvas)
        self.__canvas.bind("<Enter>", self.__bind_mouse)
        self.__canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> tk.Frame:
        """The interior property."""
        return self.__interior

    def __configure_interior(self, event: Optional[tk.Event] = None) -> None:
        # Update the scrollbar to match the size of the inner frame.
        self.__canvas.config(
            scrollregion=(
                0,
                0,
                self.__interior.winfo_reqwidth(),
                self.__interior.winfo_reqheight(),
            )
        )
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.__canvas.config(width=self.__interior.winfo_reqwidth())

    def __configure_canvas(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.__canvas.itemconfigure(
                self.__interior_id, width=self.__canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.bind_all("<4>", self.__on_mousewheel)
        self.__canvas.bind_all("<5>", self.__on_mousewheel)
        self.__canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.unbind_all("<4>")
        self.__canvas.unbind_all("<5>")
        self.__canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Linux uses event.num; Windows / Mac uses event.delta"""
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


class VerticalScrolledTtkFrame(ttk.Frame, TkBase):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' property to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    __vscrollbar: ttk.Scrollbar = None  # type: ignore
    __canvas: tk.Canvas = None  # type: ignore
    __interior: ttk.Frame = None  # type: ignore
    __interior_id: int = None  # type: ignore

    def __init__(self, parent: tk.Misc, *args, **kw) -> None:
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.__vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=self.__vscrollbar.set
        )
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.__vscrollbar.config(command=self.__canvas.yview)

        # Reset the view
        self.__canvas.xview_moveto(0)
        self.__canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self.__interior = ttk.Frame(self.__canvas)
        self.__interior_id: int = self.__canvas.create_window(
            0, 0, window=self.__interior, anchor=tk.NW
        )

        # Configure Events
        self.__interior.bind("<Configure>", self.__configure_interior)
        self.__canvas.bind("<Configure>", self.__configure_canvas)
        self.__canvas.bind("<Enter>", self.__bind_mouse)
        self.__canvas.bind("<Leave>", self.__unbind_mouse)

    @property
    def interior(self) -> ttk.Frame:
        """The interior property."""
        return self.__interior

    def __configure_interior(self, event: Optional[tk.Event] = None) -> None:
        # Update the scrollbar to match the size of the inner frame.
        self.__canvas.config(
            scrollregion=(
                0,
                0,
                self.__interior.winfo_reqwidth(),
                self.__interior.winfo_reqheight(),
            )
        )
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.__canvas.config(width=self.__interior.winfo_reqwidth())

    def __configure_canvas(self, event: tk.Event) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        if self.__interior.winfo_reqwidth() != self.__canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.__canvas.itemconfigure(
                self.__interior_id, width=self.__canvas.winfo_width()
            )

    def __bind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.bind_all("<4>", self.__on_mousewheel)
        self.__canvas.bind_all("<5>", self.__on_mousewheel)
        self.__canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    def __unbind_mouse(self, event: Optional[tk.Event] = None) -> None:
        # print(f"{event}")
        # print(f"{type(event)}")
        self.__canvas.unbind_all("<4>")
        self.__canvas.unbind_all("<5>")
        self.__canvas.unbind_all("<MouseWheel>")

    def __on_mousewheel(self, event: tk.Event) -> None:
        """Linux uses event.num; Windows / Mac uses event.delta"""
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


# #[EOF]#######################################################################
