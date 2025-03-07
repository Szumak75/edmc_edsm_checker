# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 16.10.2023

Purpose: a simple class containing basic cryptographic procedures for strings.
"""

import string
from typing import Dict

from base64 import b64decode, b64encode
from codecs import getencoder
from inspect import currentframe
from random import randrange

from ..attribtool import NoDynamicAttributes
from ..raisetool import Raise

# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_xor_process.htm
# https://teachen.info/cspp/unit4/lab04-02.html


class SimpleCrypto(NoDynamicAttributes):
    """SimpleCrypto class.

    A class that allows performing simple cryptographic operations on strings of characters.
    """

    @staticmethod
    def chars_table_generator() -> str:
        """Return printable chars string.

        A static method that returns an extended string of printable characters
        that is used to generate a translation table in caesar methods.
        """
        return string.printable + "ĄĆĘŁŃÓŚŻŹąćęłńóśżź"

    @classmethod
    def salt_generator(cls, length: int = 8) -> int:
        """Method for generate random salt with specific length.

        ### Arguments
        * length [int] - number of digits in the generated salt

        ### Returns
        [int] - salt number
        """
        if length < 1:
            raise Raise.error(
                f"...{length}",
                ValueError,
                cls.__qualname__,
                currentframe(),
            )
        return randrange(int(10**length / 10), 10**length - 1)

    @classmethod
    def caesar_encrypt(cls, salt: int, message: str) -> str:
        """Caesar encoder method with chars translate table.

        ### Arguments:
        * salt [int]    - a number used to calculate the offset in the translation table,
        * message [str] - string to encode,

        ### Returns:
        [str]  - encoded string
        """
        if not isinstance(salt, int):
            raise Raise.error(
                "Expected 'salt' as integer.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        chars: str = cls.chars_table_generator()
        chars_len: int = len(chars)
        shift: int = salt % chars_len
        trans_table: Dict = str.maketrans(chars, chars[shift:] + chars[:shift])

        return message.translate(trans_table)

    @classmethod
    def caesar_decrypt(cls, salt: int, message: str) -> str:
        """Caesar decoder method with chars translate table.

        ### Arguments:
        * salt [int]    - a number used to calculate the offset in the translation table,
        * message [str] - encoded string,

        ### Returns:
        [str]  - decoded string
        """
        if not isinstance(salt, int):
            raise Raise.error(
                "Expected 'salt' as integer.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        chars: str = cls.chars_table_generator()
        chars_len: int = len(chars)
        shift: int = chars_len - (salt % chars_len)
        trans_table: Dict = str.maketrans(chars, chars[shift:] + chars[:shift])

        return message.translate(trans_table)

    @classmethod
    def rot13_codec(cls, message: str) -> str:
        """Rot13 encoder/decoder method.

        ### Arguments:
        * message [str] - string for encode/decode

        ### Returns:
        [str] - encoded/decoded string
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        codec = lambda s: getencoder("rot13")(s)[0]
        return codec(message)  # type: ignore

    @classmethod
    def b64_encrypt(cls, message: str) -> str:
        """Base64 encoder method.

        ### Arguments:
        * message [str] - string for encode,

        ### Returns:
        [str] - base64 encoded string.
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return b64encode(message.encode("UTF-32")).decode()

    @classmethod
    def b64_decrypt(cls, message: str) -> str:
        """Base64 decoder method.

        ### Arguments:
        * message [str] - base64 string for decode,

        ### Returns:
        [str] - decoded string.
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return b64decode(message.encode("UTF-32")).decode("UTF-32")

    @classmethod
    def multiple_encrypt(cls, salt: int, message: str) -> str:
        """Multiple encoder method.

        ### Arguments:
        * salt [int]    - a number used to calculate the offset in the translation table,
        * message [str] - string to encode,

        ### Returns:
        [str]  - encoded string
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return cls.b64_encrypt(cls.caesar_encrypt(salt, cls.rot13_codec(message)))

    @classmethod
    def multiple_decrypt(cls, salt: int, message: str) -> str:
        """Multiple decoder method.

        ### Arguments:
        * salt [int]    - a number used to calculate the offset in the translation table,
        * message [str] - encoded string,

        ### Returns:
        [str]  - decoded string
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return cls.rot13_codec(cls.caesar_decrypt(salt, cls.b64_decrypt(message)))


# #[EOF]#######################################################################
