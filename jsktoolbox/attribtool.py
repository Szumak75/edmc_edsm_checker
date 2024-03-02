# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 02.07.2023

  Purpose: Base classes for restricting the creation of dynamic attributes
  on instance of derived types.

  [NoNewAttributes]
  The solution idea published in: Python Cookbook (2004), A. Martelli,
  A. Ravenscroft, D. Ascher

  [NoDynamicAttributes]
  Another solution with the same functionality.
"""

from typing import Any, Callable


def _no_new_attributes(
    wrapped_setattr: Any,
) -> Callable[[Any, str, Any], None]:
    """Internal function for use in the current module only."""

    def __setattr__(self, name: str, value: Any) -> None:
        """Check if the attribute is defined, throw an exception if not."""
        if hasattr(self, name):
            wrapped_setattr(self, name, value)
        else:
            raise AttributeError(
                f"Undefined attribute {name} cannot be added to {self}"
            )

    return __setattr__


class NoNewAttributes:
    """NoNewAttributes - base class.

    Class for restricting the creation of dynamic attributes on instances
    of derived types.
    """

    __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
        object.__setattr__
    )

    class __metaclass__(type):
        __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
            type.__setattr__
        )


class NoDynamicAttributes:
    """NoDynamicAttributes - base class.

    Class for restricting the creation of dynamic attributes on instances
    of derived types.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        if not hasattr(self, name):
            raise AttributeError(
                f"Cannot add new attribute '{name}' to {self.__class__.__name__} object"
            )
        super().__setattr__(name, value)


class ReadOnlyClass(type):
    """ReadOnlyClass - metaclass for creating read only classes.

    example:
    class A(object, metaclass=ReadOnlyClass):
          foo = "don't change me"
    """

    def __setattr__(self, name: str, value: Any) -> None:
        raise ValueError(f"Read only attribute: {name}.")


# #[EOF]#######################################################################
