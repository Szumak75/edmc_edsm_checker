# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 02.07.2023

Purpose: Provide helpers that restrict adding attributes to classes and instances.

The module collects mixins and metaclasses that prevent accidental creation of
new attributes at runtime. Inspired by recipes from *Python Cookbook*
(2004, Martelli et al.).
"""

from typing import Any, Callable


def _no_new_attributes(
    wrapped_setattr: Any,
) -> Callable[[Any, str, Any], None]:
    """Wrap `__setattr__` to prevent creation of unknown attributes.

    ### Arguments:
    * wrapped_setattr: Any - Original setter, e.g. `object.__setattr__` or `type.__setattr__`.

    ### Returns:
    [Callable[[Any, str, Any], None]] - Closure enforcing attribute existence before assignment.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """Delegate to the original setter when the attribute exists.

        Raises AttributeError if the attribute has not been defined.

        ### Arguments:
        * name: str - Attribute name to assign.
        * value: Any - Value destined for the attribute.
        """
        if hasattr(self, name):
            wrapped_setattr(self, name, value)
        else:
            raise AttributeError(
                f"Undefined attribute {name} cannot be added to {self}"
            )

    return __setattr__


class NoNewAttributes:
    """Prevent instances of subclasses from gaining new attributes.

    ### Purpose:
    Blocks dynamic attribute creation by overriding `__setattr__` for both
    instances and the metaclass.
    """

    __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
        object.__setattr__
    )

    class __metaclass__(type):
        __setattr__: Callable[[Any, str, Any], None] = _no_new_attributes(
            type.__setattr__
        )


class NoDynamicAttributes:
    """Mix-in that disallows adding attributes to class instances.

    ### Purpose:
    Ensures all attributes must be declared up-front; runtime additions raise
    AttributeError.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        if not hasattr(self, name):
            raise AttributeError(
                f"Cannot add new attribute '{name}' to {self.__class__.__name__} object"
            )
        super().__setattr__(name, value)


class ReadOnlyClass(type):
    """Metaclass that makes class attributes immutable after definition.

    ### Purpose:
    Raises AttributeError whenever class-level attributes are reassigned.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Read only attribute: {name}.")


# #[EOF]#######################################################################
