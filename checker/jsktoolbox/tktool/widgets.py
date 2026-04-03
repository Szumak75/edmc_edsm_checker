# -*- coding: utf-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide reusable Tk/ttk widgets such as status bars, tooltips, and scrollable frames.

The module centralises convenience components that enhance Tkinter UIs with common patterns like
status reporting, hover hints, and vertically scrolling containers.

VerticalScrolledFrame based on https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
"""


import tkinter as tk
from tkinter import Toplevel, ttk
from typing import Any, Optional, List, Tuple, Union, Dict

from .base import TkBase


class StatusBarTkFrame(tk.Frame, TkBase):
    """Tkinter status bar frame.

    Renders a label-driven status bar with a size grip for resizing actions.
    """

    __status: tk.StringVar = None  # type: ignore
    __status_label: tk.Label = None  # type: ignore
    __sizegrip: ttk.Sizegrip = None  # type: ignore

    def __init__(self, master: tk.Misc, *args, **kwargs) -> None:
        """Initialise the Tkinter status bar.

        ### Arguments:
        * master: tk.Misc - Parent widget that owns this frame.
        * *args: Any - Positional arguments forwarded to `tk.Frame`.
        * **kwargs: Any - Keyword arguments forwarded to `tk.Frame`.

        ### Returns:
        None - Constructor configures widget state.

        ### Raises:
        * None: Construction relies on Tkinter widget creation only.
        """
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
        """Update the status label text.

        ### Arguments:
        * value: str - Text displayed inside the status label.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self.__status.set(value)
        self.__status_label.update_idletasks()

    def clear(self) -> None:
        """Reset the status label to an empty string.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self.__status.set("")
        self.__status_label.update_idletasks()


class StatusBarTtkFrame(ttk.Frame, TkBase):
    """ttk status bar frame.

    Provides a themed status label with an optional size grip.
    """

    __status: tk.StringVar = None  # type: ignore
    __status_label: ttk.Label = None  # type: ignore
    __sizegrip: ttk.Sizegrip = None  # type: ignore

    def __init__(self, master: tk.Misc, *args, **kwargs) -> None:
        """Initialise the ttk status bar.

        ### Arguments:
        * master: tk.Misc - Parent widget that owns this frame.
        * *args: Any - Positional arguments forwarded to `ttk.Frame`.
        * **kwargs: Any - Keyword arguments forwarded to `ttk.Frame`.

        ### Returns:
        None - Constructor configures widget state.

        ### Raises:
        * None: Construction relies on ttk widget creation only.
        """
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
        """Update the status label text.

        ### Arguments:
        * value: str - Text displayed inside the status label.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self.__status.set(value)
        self.__status_label.update_idletasks()

    def clear(self) -> None:
        """Reset the status label to an empty string.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Performs widget update side effects.

        ### Raises:
        * None: Tkinter handles rendering errors internally.
        """
        self.__status.set("")
        self.__status_label.update_idletasks()


class CreateToolTip(TkBase):
    """Tooltip manager for Tk widgets.

    Attaches hover-driven handlers that display timed toplevel hints for a target widget.
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
        """Initialise the tooltip manager.

        ### Arguments:
        * widget: tk.Misc - Widget that triggers tooltip display on hover.
        * text: Union[str, List[str], Tuple[str], tk.StringVar] - Tooltip message or Tk variable.
        * wait_time: int - Delay in milliseconds before the tooltip appears.
        * wrap_length: int - Maximum tooltip line width in pixels; 0 keeps Tk defaults.
        * **kwargs: Any - Extra keyword arguments forwarded to the tooltip label configuration.

        ### Returns:
        None - Constructor stores configuration and binds widget events.

        ### Raises:
        * None: Tkinter propagates runtime errors when they occur.
        """
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
        """Handle the `<Enter>` event.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Schedules tooltip presentation.

        ### Raises:
        * None: Scheduling operations route through Tkinter.
        """
        self.__schedule()

    def __leave(self, event: Optional[tk.Event] = None) -> None:
        """Handle the `<Leave>` event.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Cancels any pending tooltip display and hides the tip.

        ### Raises:
        * None: Tkinter handles cancellation routines internally.
        """
        self.__unschedule()
        self.__hidetip()

    def __schedule(self) -> None:
        """Schedule tooltip presentation.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Registers a timed callback via `widget.after`.

        ### Raises:
        * None: Tkinter handles scheduling errors internally.
        """
        self.__unschedule()
        self.__id = self.__widget.after(self.__wait_time, self.__showtip)

    def __unschedule(self) -> None:
        """Cancel scheduled tooltip presentation.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Removes any pending `after` callbacks.

        ### Raises:
        * None: Tkinter handles cancellation failures internally.
        """
        __id: Optional[str] = self.__id
        self.__id = None
        if __id:
            self.__widget.after_cancel(__id)

    def __showtip(self, event: Optional[tk.Event] = None) -> None:
        """Display the tooltip window.

        ### Arguments:
        * event: Optional[tk.Event] - Tkinter event payload supplied by the binding.

        ### Returns:
        None - Creates a transient toplevel with the tooltip label.

        ### Raises:
        * None: Tkinter manages window creation behaviour.
        """
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
        """Hide the tooltip window.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        None - Destroys the transient toplevel when present.

        ### Raises:
        * None: Tkinter handles destruction errors internally.
        """
        __tw: Optional[Toplevel] = self.__tw
        self.__tw = None
        if __tw:
            __tw.destroy()

    @property
    def text(self) -> Union[str, tk.StringVar]:
        """Return the tooltip text or Tk variable.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        Union[str, tk.StringVar] - Current text payload, flattened when a list or tuple is provided.

        ### Raises:
        * None: Text retrieval is free of side effects.
        """
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
        """Set the tooltip text content.

        ### Arguments:
        * value: Union[str, List[str], Tuple[str], tk.StringVar] - Tooltip message or Tk variable.

        ### Returns:
        None - Updates internal references for future tooltip displays.

        ### Raises:
        * None: Assignment updates internal state without validation errors.
        """
        if isinstance(value, tk.StringVar):
            self.__text_variable = value
        else:
            self.__text = value


class VerticalScrolledTkFrame(tk.Frame, TkBase):
    """Scrollable Tk frame container.

    Provides a canvas-driven vertical scroller and exposes an interior frame for child widgets.
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
        """Return the interior frame container.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        tk.Frame - Frame that should receive child widgets.

        ### Raises:
        * None: Accessors return cached references only.
        """
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
        """Translate mouse wheel events into vertical scrolling.

        Linux relies on `event.num` while Windows and macOS provide `event.delta`.

        ### Arguments:
        * event: tk.Event - Mouse wheel event emitted by Tkinter.

        ### Returns:
        None - Adjusts the canvas viewport in response to the event.

        ### Raises:
        * None: Scroll handling defers to Tkinter canvas methods.
        """
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


class VerticalScrolledTtkFrame(ttk.Frame, TkBase):
    """Scrollable ttk frame container.

    Uses a Tk canvas plus a themed frame to offer vertical scrolling for child widgets.
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
        """Return the interior frame container.

        ### Arguments:
        * None: No public arguments.

        ### Returns:
        ttk.Frame - Themed frame that should receive child widgets.

        ### Raises:
        * None: Accessors return cached references only.
        """
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
        """Translate mouse wheel events into vertical scrolling.

        Linux relies on `event.num` while Windows and macOS provide `event.delta`.

        ### Arguments:
        * event: tk.Event - Mouse wheel event emitted by Tkinter.

        ### Returns:
        None - Adjusts the canvas viewport in response to the event.

        ### Raises:
        * None: Scroll handling defers to Tkinter canvas methods.
        """
        # print(f"{event}")
        # print(f"{type(event)}")
        if event.num == 4 or event.delta > 0:
            self.__canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.__canvas.yview_scroll(1, "units")


# #[EOF]#######################################################################
