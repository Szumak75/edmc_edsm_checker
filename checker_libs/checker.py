# -*- coding: utf-8 -*-
"""
  checker.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 20.01.2024, 23:18:04
  
  Purpose: 
"""

from typing import Optional
from checker_libs.base_log import BLogClient, BLogProcessor

from checker_libs.base_data import BCheckerData
from checker_libs.system import LogClient, LogProcessor

from jsktoolbox.libs.base_data import BClasses
from jsktoolbox.raisetool import Raise

from inspect import currentframe
from queue import SimpleQueue
from threading import Thread

from checker_libs.th import ThSearchSystem


class Checker(BLogProcessor, BLogClient, BCheckerData):
    """checker_object main class."""

    def __init__(self) -> None:
        """Initialize main class."""
        # data

        self.pluginname = "EDSM Checker"
        self.version = "1.0.0"

        # logging subsystem
        self.qlog = SimpleQueue()
        self.log_processor = LogProcessor(self.pluginname)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.thlog = Thread(target=self.th_logger, name=f"{self.pluginname} log worker")
        self.thlog.daemon = True
        self.thlog.start()

        self.logger.debug = f"{self.pluginname} object creation complete."

    def th_logger(self) -> None:
        """Def th_logger - thread logs processor."""
        self.logger.info = "Starting logger worker"
        while not self.shutting_down:
            while True:
                log = self.qlog.get(True)
                if log is None:
                    break
                self.log_processor.send(log)

    def start_search_engine(self) -> None:
        self.logger.debug = f"{self.pluginname} starting search engine..."
        if self._search is None:
            # init search thread
            self._search = ThSearchSystem(self.qlog, self.status)
            search: Optional[ThSearchSystem] = self._search
            if search:
                search.start()

    def update(self) -> None:
        if self._search:
            search = self._search
            search.search_queue.put(self.jumpsystem)


# #[EOF]#######################################################################
