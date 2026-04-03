# -*- coding: utf-8 -*-
"""
thlogs.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 27.06.2025, 21:35:02

Purpose: Threaded Logs Processor
This module provides a threaded log processor that reads logs from a file,
processes them, and writes the results to a specified output file.
"""

from inspect import currentframe
import logging
import os
from typing import Union, Optional, List, Dict
from logging.handlers import RotatingFileHandler
from queue import Queue, SimpleQueue
from io import TextIOWrapper
from time import sleep
from types import FunctionType
from typing import Any, Callable, Optional, Tuple, Dict
from threading import Event
from _thread import LockType

from ..edmctool.system import EnvLocal

from ..attribtool import ReadOnlyClass, NoDynamicAttributes
from ..basetool.data import BData
from ..raisetool import Raise


# #[EOF]#######################################################################
