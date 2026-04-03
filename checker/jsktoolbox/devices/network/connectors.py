# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 25.08.2023

Purpose: Connector interfaces module.
"""

import socket
import ssl
import sys
import posix
import time
import binascii
import select
import hashlib

from abc import ABC, abstractmethod
from typing import List, Union, Optional, Tuple, TYPE_CHECKING, Any
from inspect import currentframe

from ...basetool.data import BData
from ...raisetool import Raise
from ...netaddresstool.ipv4 import Address
from ...netaddresstool.ipv6 import Address6
from ...attribtool import ReadOnlyClass
from ..libs.converters import B64Converter

if TYPE_CHECKING:
    from _hashlib import HASH as HashDigest
else:
    HashDigest = Any


class IConnector(ABC):
    """Connection class interface."""

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
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address."""

    @address.setter
    @abstractmethod
    def address(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address."""

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""

    @property
    @abstractmethod
    def login(self) -> Optional[str]:
        """Get login property."""

    @login.setter
    @abstractmethod
    def login(self, username: str) -> None:
        """Set login property."""

    @abstractmethod
    def outputs(self) -> Tuple:
        """Get list of results after executed commands."""

    @property
    @abstractmethod
    def password(self) -> Optional[str]:
        """Get password property."""

    @password.setter
    @abstractmethod
    def password(self, passwd: str) -> None:
        """Set password property."""

    @property
    @abstractmethod
    def port(self) -> Optional[int]:
        """Get port property."""

    @port.setter
    @abstractmethod
    def port(self, port: int) -> None:
        """Set port property."""

    @property
    @abstractmethod
    def prototype(self) -> str:
        """Get protocol type property."""


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys definition class.

    For internal purpose only.
    """

    ERRORS: str = "__err__"
    IPADDR: str = "host"
    OPTIONS: str = "opt"
    PASS: str = "password"
    PORT: str = "port"
    SOCKET: str = "__socket__"
    SSL: str = "__ssl__"
    STDERR: str = "__stderr__"
    STDIN: str = "__stdin__"
    STDOUT: str = "__stdout__"
    TIMEOUT: str = "timeout"
    USER: str = "login"


class API(IConnector, BData):
    """MikroTik RouterOS API connector class."""

    def __init__(
        self,
        ip_address: Optional[Union[Address, Address6]] = None,
        port: int = 8728,
        login: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = 60.0,
        use_ssl: bool = False,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        self._set_data(
            key=_Keys.OPTIONS,
            set_default_type=str,
            value="+cet1024w",
        )
        self._set_data(
            key=_Keys.TIMEOUT,
            set_default_type=float,
            value=float(timeout),
        )
        self._set_data(key=_Keys.ERRORS, set_default_type=List, value=[])
        self._set_data(key=_Keys.STDIN, set_default_type=List, value=[])
        self._set_data(key=_Keys.STDERR, set_default_type=List, value=[])
        self._set_data(key=_Keys.STDOUT, set_default_type=List, value=[])
        self._set_data(key=_Keys.SSL, set_default_type=bool, value=use_ssl)
        self._set_data(
            key=_Keys.SOCKET,
            set_default_type=Optional[socket.socket],
            value=None,
        )
        self.port = port
        if ip_address:
            self.address = ip_address
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password

    def __del__(self) -> None:
        """Destructor."""
        self.disconnect()

    @property
    def __stdin(self) -> List:
        """Returns stdin list."""
        return self._get_data(key=_Keys.STDIN)  # type: ignore

    @property
    def __stderr(self) -> List:
        """Returns stderr list."""
        return self._get_data(key=_Keys.STDERR)  # type: ignore

    @property
    def __stdout(self) -> List:
        """Returns stdout list."""
        return self._get_data(key=_Keys.STDOUT)  # type: ignore

    @property
    def __socket(self) -> Optional[socket.socket]:
        """Returns connection socket."""
        return self._get_data(key=_Keys.SOCKET)  # type: ignore

    @__socket.setter
    def __socket(self, connection_socket: Optional[socket.socket]) -> None:
        """Sets connection socket."""
        self._set_data(key=_Keys.SOCKET, value=connection_socket)

    def __command_translator(self, command: str) -> List[str]:
        """Method for translate mikrotik CLI commands to format accepted
        by API

        Keyword arguments:
        command -- type of string, for examples:
         '/ping address=10.0.0.1 count=3'

        Return: translated list with command and attributes, for example:
        ['/ping', '=address=10.0.0.1', '=count=3"']
        """
        com_list = []
        buf_list: List[str] = command.split()
        attr_flag = False
        where_flag = False
        unset_flag = False
        where_count = 0
        for line in buf_list:
            if line.find("where") > -1:
                where_flag = True
                attr_flag = False
                continue
            elif where_flag:
                com_list.append(f"?{line}")
                where_count += 1
            elif line.find("=b'") > -1:
                attr_flag = True
                cmd, attr = line.split("=", 1)
                encoded = bytes(attr.strip("b'"), "ascii")
                attr = B64Converter.base64_to_string(encoded)
                com_list.append(f"={cmd}={attr}")
            elif line.find("=") > -1 or line.find("detail") > -1 or attr_flag:
                # i have an attribute
                attr_flag = True
                if line.find("\\s") > -1:
                    line = line.replace("\\s", " ")
                if unset_flag and line.find("*") == -1:
                    com_list.append(f"=value-name={line}")
                else:
                    com_list.append(f"={line}")
            else:
                # i have a command member
                if line == "pr":
                    line = "print"
                elif line == "unset":
                    unset_flag = True
                if len(com_list) == 0:
                    com_list.append(line)
                else:
                    com_list[0] += "/" + line
        if where_flag and where_count > 1:
            com_list.append("?#&")
        return com_list

    def __talk(self, words: List) -> List:
        ret = []
        if self.__write_sentence(words) == 0:
            return ret
        while True:
            items_list = self.__read_sentence()
            if not items_list:
                continue
            reply = items_list[0]
            attrs = {}
            for word in items_list[1:]:
                idx = word.find("=", 1)
                if idx == -1:
                    attrs[word] = ""
                else:
                    attrs[word[:idx]] = word[slice(idx + 1, None)]
            ret.append((reply, attrs))
            if reply == "!done":
                return ret
        return ret

    def __write_sentence(self, words: List) -> int:
        if not words:
            return 0
        ret = 0
        for w in words:
            self.__write_word(w)
            ret += 1
        self.__write_word("")
        return ret

    def __read_sentence(self) -> List:
        ret_list = []
        while True:
            word = self.__read_word()
            if not word:
                return ret_list
            ret_list.append(word)

    def __write_word(self, word: str) -> None:
        self.__write_len(len(word))
        self.__write_str(word)

    def __read_word(self) -> Union[str, bytes]:
        ret = self.__read_str(self.__read_len())
        if isinstance(ret, bytes):
            try:
                return ret.decode(sys.stdout.encoding, "replace")
            except UnicodeDecodeError:
                return ret
        return ret

    def __write_len(self, value: int) -> None:
        def _write(part: int) -> None:
            self.__write_byte(part.to_bytes(1, sys.byteorder))

        if value < 0x80:
            _write(value)
        elif value < 0x4000:
            value |= 0x8000
            _write((value >> 8) & 0xFF)
            _write(value & 0xFF)
        elif value < 0x200000:
            value |= 0xC00000
            _write((value >> 16) & 0xFF)
            _write((value >> 8) & 0xFF)
            _write(value & 0xFF)
        elif value < 0x10000000:
            value |= 0xE0000000
            _write((value >> 24) & 0xFF)
            _write((value >> 16) & 0xFF)
            _write((value >> 8) & 0xFF)
            _write(value & 0xFF)
        else:
            _write(0xF0)
            _write((value >> 24) & 0xFF)
            _write((value >> 16) & 0xFF)
            _write((value >> 8) & 0xFF)
            _write(value & 0xFF)

    def __read_len(self) -> int:
        char: int = ord(self.__read_str(1))
        if (char & 0x80) == 0x00:
            pass
        elif (char & 0xC0) == 0x80:
            char &= ~0xC0
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xE0) == 0xC0:
            char &= ~0xE0
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xF0) == 0xE0:
            char &= ~0xF0
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        elif (char & 0xF8) == 0xF0:
            char = ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
            char <<= 8
            char += ord(self.__read_str(1))
        return char

    def __write_str(self, string: str) -> None:
        if not string:
            return
        if self.__socket is None:
            return None
        try:
            self.__socket.sendall(bytes(string, "UTF-8"))
        except socket.error as ex:
            raise Raise.error(
                f"connection closed by remote end: {ex}",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

    def __write_byte(self, string: bytes) -> None:
        if not string or self.__socket is None:
            return None
        try:
            self.__socket.sendall(string)
        except socket.error as ex:
            raise Raise.error(
                f"connection closed by remote end: {ex}",
                RuntimeError,
                self._c_name,
                currentframe(),
            )

    def __read_str(self, length: int) -> Union[str, bytes]:
        ret: str = ""
        if self.__socket is None:
            return ret
        while len(ret) < length:
            soc_ret: bytes = self.__socket.recv(length - len(ret))
            if soc_ret == b"":
                raise Raise.error(
                    "connection closed by remote end",
                    RuntimeError,
                    self._c_name,
                    currentframe(),
                )
            if soc_ret >= (128).to_bytes(1, "big"):
                return soc_ret
            try:
                ret += soc_ret.decode(sys.stdout.encoding, "replace")
            except UnicodeDecodeError:
                return soc_ret
        return ret

    @property
    def __errors(self) -> List[str]:
        """Returns ERRORS list."""
        return self._get_data(key=_Keys.ERRORS)  # type: ignore

    def __get_socket(self) -> bool:
        """Try to open client socket for communications."""
        res = socket.getaddrinfo(
            str(self.address),
            self.port,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
        )
        af, socktype, proto, canonname, sa = res[0]

        # try to create socket
        try:
            skt = socket.socket(af, socktype, proto)
        except socket.error as ex:
            self.__socket = None
            self.__errors.append(f"socket creation error: {ex}")
            return False
        except Exception as ex:
            self.__socket = None
            self.__errors.append(f"socket creation error: {ex}")
            return False

        # set ssl if needed
        if self._get_data(key=_Keys.SSL):
            context: ssl.SSLContext = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.__socket = context.wrap_socket(skt)
            # self.__socket = ssl.wrap_socket(
            #     skt,
            #     ssl_version=ssl.PROTOCOL_TLSv1_2,
            #     ciphers="ECDHE-RSA-AES256-GCM-SHA384",
            # )
        else:
            self.__socket = skt

        # try to connect
        try:
            self.__socket.connect(sa)
        except socket.error as ex:
            self.__socket = None
            self.__errors.append(f"socket connection error: {ex}")
            return False
        except Exception as ex:
            self.__socket = None
            self.__errors.append(f"socket connection error: {ex}")
            return False
        return True

    def __build_response(self, md: HashDigest) -> str:
        """Return API login response digest."""
        return binascii.hexlify(md.digest()).decode(sys.stdout.encoding)

    def __connect(self) -> bool:
        """connection method."""
        # get socket
        if not self.__get_socket():
            self.__errors.append("could not open socket")
            return False

        # try to login
        for repl, attrs in self.__talk(
            [
                "/login",
                f"=name={self._get_data(key=_Keys.USER)}",
                f"=password={self._get_data(key=_Keys.PASS)}",
            ]
        ):
            if repl == "!trap":
                return False
            elif "=ret" in attrs.keys():
                md: hashlib._Hash = hashlib.md5()
                md.update(b"\x00")
                md.update(
                    self._get_data(key=_Keys.PASS).encode(  # type: ignore
                        sys.stdout.encoding
                    )
                )
                challenge = (attrs["=ret"]).encode(sys.stdout.encoding)
                md.update(binascii.unhexlify(challenge))
                for repl2, attrs2 in self.__talk(
                    [
                        "/login",
                        f"=name={self._get_data(key=_Keys.USER)}",
                        "=response=00" + self.__build_response(md),
                    ]
                ):
                    if repl2 == "!trap":
                        return False
                    elif repl2 == "!done":
                        return True
            elif repl == "!done":
                return True

        return True

    def connect(self) -> bool:
        """Try to connect."""
        if self.address is None:
            raise Raise.error(
                f"Host IP address is not set.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        if self.port is None:
            raise Raise.error(
                "Port is not set.", ValueError, self._c_name, currentframe()
            )
        if self.login is None:
            raise Raise.error(
                "Login is not set.", ValueError, self._c_name, currentframe()
            )
        if self.password is None:
            raise Raise.error(
                "Password is not set.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        return self.__connect()

    def disconnect(self) -> bool:
        """Terminate connection."""
        if self.__socket is None:
            return True
        try:
            self.__socket.close()
        except Exception as ex:
            self.__errors.append(f'close error: "{ex}"')
        else:
            return True

        return False

    def errors(self) -> List[str]:
        """Get list of errors after executed commands."""
        return self.__errors

    def execute(self, commands: Union[str, List]) -> bool:
        """Execute commands."""
        # cleanup lists
        self.__stdin.clear()
        self.__stderr.clear()
        self.__stdout.clear()
        # init local variables
        ret = True
        comms = list()
        if isinstance(commands, str):
            comms.append(commands)
        elif isinstance(commands, List):
            comms.extend(commands)
        else:
            raise Raise.error(
                f"Expected string or list type, received: '{type(commands)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        # test connection
        if not self.is_alive:
            self.disconnect()
            if not self.connect():
                return False
        for com in comms:
            self.__stdin.append([])
            self.__stderr.append([])
            self.__stdout.append([])
            for repl, attrs in self.__talk(self.__command_translator(com)):
                tmp = {}
                for key in attrs:
                    tmp[key.strip("=")] = attrs[key]
                if repl == "!trap":
                    self.__stderr[len(self.__stderr) - 1].append(tmp)
                    ret = False
                elif repl == "!re":
                    # if ".id" in tmp:
                    # tmp[".id"].replace("*", "")
                    self.__stdout[len(self.__stdin) - 1].append(tmp)
        return ret

    @property
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        return self._get_data(key=_Keys.IPADDR, default_value=None)

    @address.setter
    def address(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            self._set_data(
                key=_Keys.IPADDR,
                value=ip_address,
                set_default_type=Union[Address, Address6],
            )

    @property
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""
        if self.__socket is None:
            return False
        try:
            self.__socket.settimeout(2)
        except Exception:
            # socket is closed
            return False

        try:
            self.__talk(["/system/identity/print"])
        except (socket.timeout, IndexError, BrokenPipeError):
            self.__errors.append("RouterOS does not respond, closing socket.")
            self.disconnect()
            return False
        self.__socket.settimeout(self._get_data(key=_Keys.TIMEOUT))
        return True

    @property
    def login(self) -> Optional[str]:
        """Get login property."""
        return self._get_data(key=_Keys.USER, default_value=None)

    @login.setter
    def login(self, username: str) -> None:
        """Set login property."""
        self._set_data(key=_Keys.USER, value=username, set_default_type=str)

    def outputs(self) -> Tuple:
        """Get list of results after executed commands."""
        return self.__stdout, self.__stderr

    @property
    def password(self) -> Optional[str]:
        """Get password property."""
        return self._get_data(key=_Keys.PASS, default_value=None)

    @password.setter
    def password(self, passwd: str) -> None:
        """Set password property."""
        self._set_data(key=_Keys.PASS, value=passwd, set_default_type=str)

    @property
    def port(self) -> Optional[int]:
        """Get port property."""
        return self._get_data(key=_Keys.PORT, default_value=None)

    @port.setter
    def port(self, port: int) -> None:
        """Set port property."""
        self._set_data(key=_Keys.PORT, value=port, set_default_type=int)

    @property
    def prototype(self) -> str:
        """Returns protocol type."""
        return "API"


class SSH(IConnector, BData):
    """SSH connector class."""

    def __init__(
        self,
        ip_address: Optional[Union[Address, Address6]] = None,
        port: Optional[int] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Constructor."""
        if ip_address:
            self.address = ip_address
        if port is not None:
            self.port = port
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password

    def connect(self) -> bool:
        """Try to connect."""
        return False

    def disconnect(self) -> bool:
        """Terminate connection."""
        return False

    def errors(self) -> List:
        """Get list or errors after executed commands."""
        return []

    def execute(self, commands: Union[str, List]) -> bool:
        """Execute commands."""
        return False

    @property
    def address(self) -> Optional[Union[Address, Address6]]:
        """Get host address property."""
        return self._get_data(key=_Keys.IPADDR, default_value=None)

    @address.setter
    def address(self, ip_address: Union[Address, Address6]) -> None:
        """Set host address setter."""
        if ip_address:
            self._set_data(
                key=_Keys.IPADDR,
                value=ip_address,
                set_default_type=Union[Address, Address6],
            )

    @property
    def is_alive(self) -> bool:
        """Get alive flag from connected protocol."""
        return False

    @property
    def login(self) -> Optional[str]:
        """Get login property."""
        return self._get_data(key=_Keys.USER, default_value=None)

    @login.setter
    def login(self, username: str) -> None:
        """Set login property."""
        self._set_data(key=_Keys.USER, value=username, set_default_type=str)

    def outputs(self) -> Tuple:
        """Get list of results after executed commands."""
        return tuple()

    @property
    def password(self) -> Optional[str]:
        """Get password property."""
        return self._get_data(key=_Keys.PASS, default_value=None)

    @password.setter
    def password(self, passwd: str) -> None:
        """Set password property."""
        self._set_data(key=_Keys.PASS, value=passwd, set_default_type=str)

    @property
    def port(self) -> Optional[int]:
        """Get port property."""
        return self._get_data(key=_Keys.PORT, default_value=None)

    @port.setter
    def port(self, port: int) -> None:
        """Set port property."""
        self._set_data(key=_Keys.PORT, value=port, set_default_type=int)

    @property
    def prototype(self) -> str:
        """Returns protocol type."""
        return "SSH"


# #[EOF]#######################################################################
