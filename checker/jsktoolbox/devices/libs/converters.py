# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: module to string converting.
"""

import base64

from ...attribtool import NoDynamicAttributes


class B64Converter(NoDynamicAttributes):
    """Base64 Converter class."""

    @classmethod
    def string_to_base64(cls, string: str, encoding: str = "ascii") -> bytes:
        """Returns encoded string to bytes."""
        return base64.b64encode(string.encode(encoding=encoding))

    @classmethod
    def base64_to_string(
        cls, bytes64: bytes, encoding: str = "ascii", errors: str = "replace"
    ) -> str:
        """Returns decoded bytes to string."""
        return base64.b64decode(bytes64).decode(encoding=encoding, errors=errors)


# #[EOF]#######################################################################
