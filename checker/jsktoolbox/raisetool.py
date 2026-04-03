# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.05.2023

Purpose: This module provides the `Raise` class, a utility for creating
and formatting standardized exception messages. It helps in generating
rich, informative error messages that include details like the class name,
method name, and line number where the error occurred, facilitating easier debugging.
"""
from types import FrameType
from typing import Optional

from .attribtool import NoDynamicAttributes


class Raise(NoDynamicAttributes):
    """A utility class for formatting and creating exception objects.

    This class contains only static methods and is not meant to be instantiated.
    It serves as a centralized tool for generating consistent and descriptive
    error messages and exception instances throughout a project.
    """

    @classmethod
    def message(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> str:
        """Format a message string with contextual information.

        This method constructs a detailed message string by prepending the
        class name, method name, and line number.

        ### Arguments:
        * message: str - The core message to be formatted.
        * class_name: str - The name of the class from which the call is made. Defaults to "".
        * currentframe: Optional[FrameType] - A frame object from `inspect.currentframe()`.

        ### Returns:
        str - A formatted message string with contextual details.
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
        """Create an exception instance with a formatted message.

        This is the primary factory method for creating standardized exceptions.
        It validates the exception type and formats the message.

        ### Arguments:
        * message: str - The core error message.
        * exception: type[Exception] - The exception class to be instantiated. Defaults to `Exception`.
        * class_name: str - The name of the class where the error occurred. Defaults to "".
        * currentframe: Optional[FrameType] - A frame object from `inspect.currentframe()`.

        ### Returns:
        Exception - An instance of the specified exception class.

        ### Raises:
        * TypeError: If the `exception` argument is not a class that inherits from `Exception`.
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
