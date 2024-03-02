# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 25.08.2023

  Purpose: Connector interfaces module.
"""

from abc import ABC, abstractmethod
from typing import List, Union


class IConnect(ABC):
    """Conection class interface."""

    @abstractmethod
    def connect(self) -> bool:
        """Connection method."""

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect method."""

    @abstractmethod
    def errors(self) -> List:
        """Get list or errors after executed commands."""

    @abstractmethod
    def execute(self, commands: Union[str, List]) -> bool:
        """Execute method."""

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""

    @property
    @abstractmethod
    def login(self) -> str:
        """Get login property."""

    @login.setter
    @abstractmethod
    def login(self, username: str) -> None:
        """Set login property."""

    @abstractmethod
    def outputs(self) -> List:
        """Get list of results after executed commands."""

    @property
    @abstractmethod
    def password(self) -> str:
        """Get password property."""

    @password.setter
    @abstractmethod
    def password(self, passwordstring: str) -> None:
        """Set password property."""

    @property
    @abstractmethod
    def prototype(self) -> str:
        """Get protocol type property."""


# #[EOF]#######################################################################
