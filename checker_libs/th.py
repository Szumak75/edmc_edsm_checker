# -*- coding: utf-8 -*-
"""
  th.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 21.01.2024, 01:31:24
  
  Purpose: 
"""

from time import sleep
import tkinter as tk

from typing import Optional, Union
from queue import Empty, Queue, SimpleQueue
from inspect import currentframe

from jsktoolbox.libs.base_th import ThBaseObject
from jsktoolbox.libs.base_data import BData
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass

from threading import Event, Thread
from checker_libs.base_log import BLogClient
from checker_libs.stars import StarsSystem
from checker_libs.system import LogClient
from checker_libs.tools import Url


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys class."""

    QSEARCH: str = "__qsearch__"
    EXIT: str = "__exit__"


class ThSearchSystem(ThBaseObject, BLogClient, Thread):
    """Threaded system search engine."""

    def __init__(
        self,
        log_queue: Union[Queue, SimpleQueue],
        status: tk.StringVar,
    ) -> None:
        Thread.__init__(self, name=self._c_name)
        self._stop_event = Event()

        # init log subsystem
        if not isinstance(log_queue, (Queue, SimpleQueue)):
            raise Raise.error(
                f"Expected Queue or SimpleQueue type, received '{type(log_queue)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.logger = LogClient(log_queue)

        # init search queue
        self._data[_Keys.QSEARCH] = Queue()

        # EXIT flag
        self._data[_Keys.EXIT] = False

    @property
    def search_queue(self) -> Queue:
        return self._data[_Keys.QSEARCH]

    def run(self) -> None:
        """Go to work."""

        url = Url()

        while not self._data[_Keys.EXIT]:
            try:
                item: StarsSystem = self.search_queue.get_nowait()
                # processing
                if item and item.name:
                    system = url.system_query(item)
                    self.logger.debug = f"{self._c_name}: {system}"

            except Empty:
                sleep(0.5)

    def quit(self) -> None:
        """Set exit flag."""
        self._data[_Keys.EXIT] = True


# #[EOF]#######################################################################
