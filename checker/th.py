# -*- coding: utf-8 -*-
"""
  th.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 21.01.2024, 01:31:24
  
  Purpose: 
"""

from time import sleep
import tkinter as tk

from typing import Optional, Union, Dict, Any
from queue import Empty, Queue, SimpleQueue
from threading import Event, Thread


from checker.jsktoolbox.basetool.threads import ThBaseObject
from checker.jsktoolbox.attribtool import ReadOnlyClass

from checker.jsktoolbox.edmctool.base import BLogClient
from checker.jsktoolbox.edmctool.stars import StarsSystem
from checker.jsktoolbox.edmctool.logs import LogClient
from checker.jsktoolbox.edmctool.edsm import Url
from checker.jsktoolbox.edmctool.edsm_keys import EdsmKeys


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys class."""

    Q_SEARCH: str = "__q_search__"
    EXIT: str = "__exit__"
    STATUS: str = "__status__"


class ThSearchSystem(ThBaseObject, BLogClient, Thread):
    """Threaded system search engine."""

    def __init__(
        self,
        log_queue: Union[Queue, SimpleQueue],
        status: tk.StringVar,
    ) -> None:
        Thread.__init__(self, name=self._c_name, daemon=True)
        self._stop_event = Event()

        # init log subsystem
        self.logger = LogClient(log_queue)

        # status
        self._set_data(key=_Keys.STATUS, value=status, set_default_type=tk.StringVar)

        # init search queue
        self._set_data(key=_Keys.Q_SEARCH, value=Queue(), set_default_type=Queue)

        # EXIT flag
        self._set_data(key=_Keys.EXIT, value=False, set_default_type=bool)

    @property
    def status(self) -> tk.StringVar:
        return self._get_data(
            key=_Keys.STATUS,
        )  # type: ignore

    @property
    def search_queue(self) -> Queue:
        return self._get_data(
            key=_Keys.Q_SEARCH,
        )  # type: ignore

    def run(self) -> None:
        """Go to work."""

        url = Url()

        self.logger.debug = f"{self._c_name} start"

        while not self._get_data(key=_Keys.EXIT):
            try:
                item: StarsSystem = self.search_queue.get_nowait()
                # processing
                if item and item.name:
                    system: Optional[Dict[str, Any]] = url.system_query(item)
                    self.logger.debug = f"{self._c_name}: {system}"
                    if system:
                        self.status.set("")
                        item.update_from_edsm(system)
                        query: str = url.bodies_url(item)
                        self.logger.debug = f"url: {query}"
                        bodies = url.url_query(query)
                        if bodies and isinstance(bodies, Dict):
                            item.update_from_edsm(bodies)
                            self.logger.debug = f"system information: {item}"
                            out: str = ""
                            if (
                                EdsmKeys.BODY_COUNT in item.data
                                and EdsmKeys.BODIES in item.data
                            ):
                                bodies = item.data[EdsmKeys.BODIES]
                                count = item.data[EdsmKeys.BODY_COUNT]
                                if not f"{bodies}".isnumeric():
                                    bodies = "??"
                                if not f"{count}".isnumeric():
                                    count = "??"
                                out = f"[{bodies}/{count}]"
                            else:
                                out = "[??/??]"
                            if EdsmKeys.COORDS_LOCKED in item.data:
                                if item.data[EdsmKeys.COORDS_LOCKED]:
                                    out = f"Lock {out}"
                                else:
                                    out = f"Unlock {out}"
                            if (
                                EdsmKeys.REQUIRE_PERMIT in item.data
                                and item.data[EdsmKeys.REQUIRE_PERMIT]
                            ):
                                out = f"Permit {out}"
                                self.logger.debug = f"OUT: {out}"
                            self.status.set(f"{item.name} - {out}")

                    else:
                        self.status.set(f"{item.name} - system unknown")

            except Empty:
                sleep(0.5)

        self.logger.debug = f"{self._c_name} end"

    def quit(self) -> None:
        """Set exit flag."""
        self._set_data(key=_Keys.EXIT, value=True)


# #[EOF]#######################################################################
