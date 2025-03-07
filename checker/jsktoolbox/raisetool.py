# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.05.2023

Purpose: Raise class for formatting thrown exception messages.
The message can be formatted with information about the class,
method, and line number where the exception was thrown.
"""
from types import FrameType
from typing import Optional

from .attribtool import NoDynamicAttributes


class Raise(NoDynamicAttributes):
    """Raise class for formatting thrown exception messages."""

    @classmethod
    def message(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> str:
        """Message formatter method.

        ### Arguments:
        * message: str    - message to format
        * class_name: str - caller class name (self.__class__.__name__)
        * currentframe: FrameType - object from inspect.currentframe()

        ### Returns:
        formatted message string
        """
        template: str = f"{message}"
        if currentframe and isinstance(currentframe, FrameType):
            template = f"{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {template}"
        elif isinstance(class_name, str) and class_name != "":
            template = f"{class_name}: {template}"
            return template
        else:
            return template
        template = f"{class_name}.{template}"
        return template

    @classmethod
    def error(
        cls,
        message: str,
        exception: type[Exception] = Exception,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> Exception:
        """Returns exception with formatted string.

        ### Arguments:
        * message: str - message to format
        * exception: type[Exception] - custom exception to return
        * class_name: str - caller class name (self.__class__.__name__)
        * currentframe: FrameType - object from inspect.currentframe()

        ### Returns:
        given exception type
        """
        if isinstance(exception, type):
            if not isinstance(exception(), Exception):
                raise cls.error(
                    f"Exception class or its derived class expected, '{exception.__qualname__}' received.",
                    TypeError,
                    class_name,
                    currentframe,
                )
        else:
            raise cls.error(
                "Exception class or its derived class expected.",
                TypeError,
                class_name,
                currentframe,
            )
        return exception(
            cls.message(
                (
                    f"[{exception.__qualname__}]: {message}"
                    if message
                    else f"[{exception.__qualname__}]"
                ),
                class_name,
                currentframe,
            )
        )


# #[EOF]#######################################################################
