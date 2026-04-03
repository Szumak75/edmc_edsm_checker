# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 16.10.2023

Purpose: Provide simple, string-centric cryptographic helpers.

This module offers lightweight encoding and cipher helpers intended for quick
experiments and utilities that operate on user-provided keyboard input.
"""

import string
import unicodedata
from typing import Dict

from base64 import b64decode, b64encode
from binascii import Error as BinasciiError
from codecs import decode
from inspect import currentframe
from secrets import randbelow

from ..attribtool import NoDynamicAttributes
from ..raisetool import Raise

# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_xor_process.htm
# https://teachen.info/cspp/unit4/lab04-02.html


class SimpleCrypto(NoDynamicAttributes):
    """Utility class for lightweight string encryption and encoding routines."""

    @staticmethod
    def chars_table_generator() -> str:
        """Build the character table used by Caesar-style transformations.

        ### Returns:
        [str] - Ordered set of printable and selected Unicode characters used for mapping.
        """
        base_chars: str = string.printable
        unicode_blocks: tuple[range, ...] = (
            range(0x00A0, 0x024F + 1),
            range(0x0370, 0x03FF + 1),
            range(0x0400, 0x052F + 1),
            range(0x0530, 0x058F + 1),
            range(0x0590, 0x05FF + 1),
            range(0x0600, 0x06FF + 1),
        )
        extra_chars = [
            chr(code)
            for block in unicode_blocks
            for code in block
            if unicodedata.category(chr(code))[0] != 'C'
        ]
        combined: str = base_chars + ''.join(extra_chars)
        return ''.join(dict.fromkeys(combined))

    @classmethod
    def salt_generator(cls, length: int = 8) -> int:
        """Generate a numeric salt with the requested number of digits.

        ### Arguments:
        * length: int - Desired digit count for the generated salt.

        ### Returns:
        [int] - Random salt constrained to the given length.

        ### Raises:
        * ValueError: Provided length is less than 1.
        """
        if length < 1:
            raise Raise.error(
                f"...{length}",
                ValueError,
                cls.__qualname__,
                currentframe(),
            )
        min_value: int = 10 ** (length - 1)
        range_size: int = 10**length - min_value
        return min_value + randbelow(range_size)

    @classmethod
    def caesar_encrypt(cls, salt: int, message: str) -> str:
        """Encode a message using a Caesar cipher over the generated table.

        ### Arguments:
        * salt: int - Value used to derive the rotation offset.
        * message: str - Plain-text message to encode.

        ### Returns:
        [str] - Encoded message.

        ### Raises:
        * TypeError: Salt is not an integer.
        * TypeError: Message is not a string instance.
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
        """Decode a Caesar-encrypted message using the generated table.

        ### Arguments:
        * salt: int - Value used to derive the rotation offset.
        * message: str - Encoded message to decode.

        ### Returns:
        [str] - Plain-text message.

        ### Raises:
        * TypeError: Salt is not an integer.
        * TypeError: Message is not a string instance.
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
        """Perform ROT13 translation for ASCII-compatible text.

        ### Arguments:
        * message: str - Text to encode or decode using ROT13.

        ### Returns:
        [str] - Transformed message.

        ### Raises:
        * TypeError: Message is not a string instance.
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return decode(message, "rot_13")

    @classmethod
    def b64_encrypt(cls, message: str) -> str:
        """Encode a string as Base64 using UTF-8 bytes.

        ### Arguments:
        * message: str - Text to encode.

        ### Returns:
        [str] - Base64-encoded representation.

        ### Raises:
        * TypeError: Message is not a string instance.
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return b64encode(message.encode("utf-8")).decode("ascii")

    @classmethod
    def b64_decrypt(cls, message: str) -> str:
        """Decode a Base64 string assuming UTF-8 payload.

        ### Arguments:
        * message: str - Base64 text to decode.

        ### Returns:
        [str] - Decoded plain-text message.

        ### Raises:
        * TypeError: Message is not a string instance.
        * ValueError: Provided payload is not valid Base64.
        """
        if not isinstance(message, str):
            raise Raise.error(
                "Expected 'message' as str type.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        try:
            raw_bytes = b64decode(message.encode("ascii"), validate=True)
        except (BinasciiError, UnicodeEncodeError) as exc:
            raise Raise.error(
                "Invalid Base64 payload.",
                ValueError,
                cls.__qualname__,
                currentframe(),
            ) from exc
        return raw_bytes.decode("utf-8")

    @classmethod
    def multiple_encrypt(cls, salt: int, message: str) -> str:
        """Apply Caesar, ROT13, and Base64 encoders sequentially.

        The method first performs ROT13, then a Caesar shift, and finally Base64
        encoding to produce a layered transformation.

        ### Arguments:
        * salt: int - Value used to derive the Caesar translation offset.
        * message: str - Plain-text message to encode.

        ### Returns:
        [str] - Result of the chained encoders.

        ### Raises:
        * TypeError: Message is not a string instance.
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
        """Reverse the layered encoding applied by `multiple_encrypt`.

        ### Arguments:
        * salt: int - Value used to derive the Caesar translation offset.
        * message: str - Encoded message produced by `multiple_encrypt`.

        ### Returns:
        [str] - Original plain-text message.

        ### Raises:
        * TypeError: Message is not a string instance.
        * ValueError: Nested Base64 payload is invalid.
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
