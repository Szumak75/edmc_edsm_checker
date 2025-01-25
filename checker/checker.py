# -*- coding: utf-8 -*-
"""
  checker.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 20.01.2024, 23:18:04
  
  Purpose: 
"""


from checker.jsktoolbox.edmctool.base import BLogClient, BLogProcessor
from checker.jsktoolbox.edmctool.logs import LogClient, LogProcessor
from checker.base_data import BCheckerData


from queue import SimpleQueue
from threading import Thread

from checker.th import ThSearchSystem


class Checker(BLogProcessor, BLogClient, BCheckerData):
    """checker_object main class."""

    def __init__(self) -> None:
        """Initialize main class."""
        # data
        self.plugin_name = "EDSM Checker"
        self.version = "1.1.1"

        # logging subsystem
        self.qlog = SimpleQueue()
        self.log_processor = LogProcessor(self.plugin_name)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.th_log = Thread(
            target=self._th_logger, name=f"{self.plugin_name} log worker"
        )
        self.th_log.daemon = True
        self.th_log.start()

        self.logger.debug = f"{self.plugin_name} object creation complete."

    def _th_logger(self) -> None:
        """Def th_logger - thread logs processor."""
        self.logger.info = "Starting logger worker"
        while not self.shutting_down:
            while True:
                log = self.qlog.get(True)
                if log is None:
                    break
                self.log_processor.send(log)

    def start_search_engine(self) -> None:
        self.logger.debug = f"{self.plugin_name} starting search engine..."
        if self._search is None:
            # init search thread
            search = ThSearchSystem(self.qlog, self.status)
            print(search.name)
            if search:
                search.start()
                self._search = search

    def dialog_update(self) -> None:
        if self._search:
            search: ThSearchSystem = self._search
            search.search_queue.put(self.jump_system)


# #[EOF]#######################################################################
