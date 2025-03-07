# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 23.06.2023

Purpose: Classes for IPv4
"""

import socket
import struct
from copy import deepcopy
from inspect import currentframe
from typing import TypeVar, Union, List

from ..attribtool import NoDynamicAttributes
from ..raisetool import Raise
from .libs.octets import Octet
from ..libs.interfaces.comparators import IComparators
from ..basetool.classes import BClasses

TAddress = TypeVar("TAddress", bound="Address")


class Address(IComparators, BClasses, NoDynamicAttributes):
    """Address class for representing IPv4 addresses.

    Constructor arguments:
    addr: Union[str, int, List[Octets]] -- IPv4 address representation as string, integer or list of four Octets

    Public property:
    octets: List[Octet] -- Return list of four Octets

    Public setter:
    octets: Union[str, int, List] -- Set IPv4 address from string, integer or list of octets.
    """

    __var_int: int = 0

    def __init__(
        self, addr: Union[str, int, Union[List[str], List[int], List[Octet]]]
    ) -> None:
        """Constructor."""
        self.octets = addr

    def __eq__(self, arg: TAddress) -> bool:
        """Equal."""
        return int(self) == int(arg)

    def __ge__(self, arg: TAddress) -> bool:
        """Greater or equal."""
        return int(self) >= int(arg)

    def __gt__(self, arg: TAddress) -> bool:
        """Greater."""
        return int(self) > int(arg)

    def __le__(self, arg: TAddress) -> bool:
        """Less or equal."""
        return int(self) <= int(arg)

    def __lt__(self, arg: TAddress) -> bool:
        """Less."""
        return int(self) < int(arg)

    def __ne__(self, arg: TAddress) -> bool:
        """Negative."""
        return int(self) != int(arg)

    @staticmethod
    def __int_to_ip(ip_int: int) -> str:
        """Convert ip int representation to ipv4 str."""
        return socket.inet_ntoa(struct.pack("!L", ip_int))

    @staticmethod
    def __ip_to_int(ip_str: str) -> int:
        """Convert ipv4 str representation to ip int."""
        return struct.unpack("!L", socket.inet_aton(ip_str))[0]

    def __set_octets_from_list(
        self, value: Union[List[str], List[int], List[Octet]]
    ) -> None:
        if not value:
            raise Raise.error(
                "Empty list received.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        if len(value) != 4:
            raise Raise.error(
                f"Expected list with four elements, len({len(value)}) received.",
                ValueError,
                self._c_name,
                currentframe(),
            )

        self.__var_int = Address.__ip_to_int(
            f"{Octet(value[0])}.{Octet(value[1])}.{Octet(value[2])}.{Octet(value[3])}"
        )

    def __set_octets_from_int(self, value: int) -> None:
        if value in range(0, 4294967296):
            self.__var_int = value
        else:
            raise Raise.error(
                f"IP-int out of range (0-4294967295), received: {value}",
                ValueError,
                self._c_name,
                currentframe(),
            )

    def __set_octets_from_str(self, value: str) -> None:
        self.__set_octets_from_list(value.split("."))

    def __int__(self) -> int:
        """Return ipv4 representation as integer."""
        return self.__var_int

    def __str__(self) -> str:
        """Return string representation of address."""
        return Address.__int_to_ip(self.__var_int)

    def __repr__(self) -> str:
        """Return representation of object."""
        return f"{self._c_name}('{str(self)}')"

    @property
    def octets(self) -> List[Octet]:
        """Return octets list of four Octets."""
        tmp: list[str] = str(self).split(".")
        return [Octet(tmp[0]), Octet(tmp[1]), Octet(tmp[2]), Octet(tmp[3])]

    @octets.setter
    def octets(
        self, value: Union[str, int, Union[List[str], List[int], List[Octet]]]
    ) -> None:
        if isinstance(value, List):
            self.__set_octets_from_list(value)
        elif isinstance(value, int):
            self.__set_octets_from_int(value)
        elif isinstance(value, str):
            self.__set_octets_from_str(value)
        else:
            raise Raise.error(
                f"Expected String or Integer or List type, received: {type(value)}.",
                TypeError,
                self._c_name,
                currentframe(),
            )


# netmask
class Netmask(BClasses, NoDynamicAttributes):
    """Netmask class for IPv4 addresses.

    Constructor argument:
    addr: Union[str, int, List] -- Set netmask from string, integer or list of proper format of netmask octets.

    Public property:
    octets: List[Octet] -- Return netmask as list of four octets.
    cidr: str -- Return netmask in CIDR string format.

    Public setter:
    octets: List[Octet] -- Set netmask from list of 4 values [int||str||Octets].
    cidr: Union[str, int] -- Set netmask from CIDR format of string or integer.
    """

    # CIDR format
    __cidr: int = 0

    def __init__(
        self, addr: Union[str, int, Union[List[str], List[int], List[Octet]]]
    ) -> None:
        """Constructor."""
        if isinstance(addr, int):
            self.cidr = addr
        elif isinstance(addr, str):
            if len(addr) < 3:
                self.cidr = addr
            else:
                self.octets = addr
        elif isinstance(addr, List):
            self.octets = str(Address(addr))
        else:
            raise Raise.error(
                f"Expected String, Integer or List type, received: '{type(addr)}'.",
                ValueError,
                self._c_name,
                currentframe(),
            )

    def __int__(self) -> int:
        return self.__cidr

    def __str__(self) -> str:
        # convert CIDR to netmask
        return socket.inet_ntoa(
            struct.pack("!I", (1 << 32) - (1 << (32 - self.__cidr)))
        )

    def __repr__(self) -> str:
        return f"{self._c_name}({self.cidr})"

    def __cidr_validator(self, cidr: int) -> None:
        """Check and set cidr."""
        if cidr >= 0 and cidr <= 32:
            self.__cidr = cidr
        else:
            raise Raise.error(
                f"CIDR is out of range (0-32), received: {cidr}",
                ValueError,
                self._c_name,
                currentframe(),
            )

    @staticmethod
    def __octets_validator(octets: int) -> bool:
        """Check if given octets list is valid."""
        test: list[int] = [
            0,  # '0.0.0.0'
            2147483648,  # "128.0.0.0",
            3221225472,  # "192.0.0.0",
            3758096384,  # "224.0.0.0",
            4026531840,  # "240.0.0.0",
            4160749568,  # "248.0.0.0",
            4227858432,  # "252.0.0.0",
            4261412864,  # "254.0.0.0",
            4278190080,  # "255.0.0.0",
            4286578688,  # "255.128.0.0",
            4290772992,  # "255.192.0.0",
            4292870144,  # "255.224.0.0",
            4293918720,  # "255.240.0.0",
            4294443008,  # "255.248.0.0",
            4294705152,  # "255.252.0.0",
            4294836224,  # "255.254.0.0",
            4294901760,  # "255.255.0.0",
            4294934528,  # "255.255.128.0",
            4294950912,  # "255.255.192.0",
            4294959104,  # "255.255.224.0",
            4294963200,  # "255.255.240.0",
            4294965248,  # "255.255.248.0",
            4294966272,  # "255.255.252.0",
            4294966784,  # "255.255.254.0",
            4294967040,  # "255.255.255.0",
            4294967168,  # "255.255.255.128",
            4294967232,  # "255.255.255.192",
            4294967264,  # "255.255.255.224",
            4294967280,  # "255.255.255.240",
            4294967288,  # "255.255.255.248",
            4294967292,  # "255.255.255.252",
            4294967294,  # "255.255.255.254",
            4294967295,  # "255.255.255.255",
        ]
        if octets in test:
            return True
        return False

    @property
    def octets(self) -> List[Octet]:
        """Return octets list of four Octets."""
        tmp: list[str] = str(self).split(".")
        return [Octet(tmp[0]), Octet(tmp[1]), Octet(tmp[2]), Octet(tmp[3])]

    @octets.setter
    def octets(
        self, addr: Union[str, int, Union[List[str], List[int], List[Octet]]]
    ) -> None:
        """Set netmask from list of 4 values [int||str||Octets]."""
        tmp = int(Address(addr))
        if not Netmask.__octets_validator(tmp):
            raise Raise.error(
                f"Invalid mask, received: {str(Address(addr))}",
                ValueError,
                self._c_name,
                currentframe(),
            )
        self.cidr = sum([bin(x.value).count("1") for x in Address(addr).octets])

    @property
    def cidr(self) -> str:
        """Return CIDR netmask as string type."""
        return str(self.__cidr)

    @cidr.setter
    def cidr(self, value: Union[str, int]) -> None:
        if isinstance(value, str) and value.isdigit():
            self.__cidr_validator(int(value))
        elif isinstance(value, int):
            self.__cidr_validator(value)
        else:
            raise Raise.error(
                f"Expected Digit string or Int, received: {value}",
                ValueError,
                self._c_name,
                currentframe(),
            )


# Network
class Network(BClasses, NoDynamicAttributes):
    """Network IPv4 class.

    Constructor argument:
    addr: Union[str, List] -- Set IPv4 network address from string or two element list of address [Address,str,int,list] and netmask [Netmask, str, int, list].

    Public property:
    address: Address -- Return IPv4 address set in the constructor.
    broadcast: Address -- Return broadcast address.
    count: int -- Return count hosts addresses in network range.
    hosts: List[Address] -- Return hosts address list.
    network: Address -- Return network address.
    mask: Netmask -- Return netmask.
    max: Address -- Return max address of host in network range.
    min: Address -- Return min address of host in network range.
    """

    __address: Address = None  # type: ignore
    __mask: Netmask = None  # type: ignore

    def __init__(self, addr: Union[str, List]) -> None:
        """Constructor."""
        if isinstance(addr, str):
            self.__network_from_str(addr)
        elif isinstance(addr, List):
            self.__network_from_list(addr)
        else:
            raise Raise.error(
                f"Expected IP network string or list type, received: '{type(addr)}'.",
                ValueError,
                self._c_name,
                currentframe(),
            )

    def __str__(self) -> str:
        """Return string representation of network address."""
        return f"{self.network}/{int(self.mask)}"

    def __repr__(self) -> str:
        """Return  string representation of class object."""
        return f"{self._c_name}({str(self)})"

    def __network_from_str(self, addr: str) -> None:
        """Build configuration from string."""
        if addr.find("/") > 0:
            tmp: list[str] = addr.split("/")
            self.__address = Address(tmp[0])
            self.__mask = Netmask(tmp[1])
        else:
            raise Raise.error(
                f"Expected network address in 'ip/mask' format string, received: '{addr}'.",
                ValueError,
                self._c_name,
                currentframe(),
            )

    def __network_from_list(self, addr: List) -> None:
        """Build configuration from list."""
        if len(addr) != 2:
            raise Raise.error(
                "Expected two element list ['ip','netmask']",
                ValueError,
                self._c_name,
                currentframe(),
            )
        if isinstance(addr[0], Address):
            self.__address = deepcopy(addr[0])
        else:
            self.__address = Address(addr[0])
        if isinstance(addr[1], Netmask):
            self.__mask = deepcopy(addr[1])
        else:
            self.__mask = Netmask(addr[1])

    @property
    def address(self) -> Address:
        """Return IPv4 address."""
        return self.__address

    @property
    def broadcast(self) -> Address:
        """Return broadcast address."""
        ip = int(self.address)
        mask = int(Address(self.mask.octets))
        broadcast: int = ip | (mask ^ (1 << 32) - 1)
        return Address(broadcast)

    @property
    def count(self) -> int:
        """Return count hosts addresses in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        return broadcast - net - 1 if broadcast - net > 2 else 0

    @property
    def hosts(self) -> List[Address]:
        """Return list of hosts in network range."""
        tmp: List[Address] = []
        net = int(self.network)
        broadcast = int(self.broadcast)
        for i in range(1, broadcast - net):
            tmp.append(Address(net + i))
        return tmp

    @property
    def mask(self) -> Netmask:
        """Return IPv4 network mask."""
        return self.__mask

    @property
    def max(self) -> Address:
        """Return last address of host in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        ip = broadcast - 1
        return Address(ip) if ip > net else self.broadcast

    @property
    def min(self) -> Address:
        """Return first host address in network range."""
        net = int(self.network)
        broadcast = int(self.broadcast)
        ip: int = net + 1
        return Address(ip) if ip < broadcast else self.network

    @property
    def network(self) -> Address:
        """Return network address."""
        ip = int(self.address)
        mask = int(Address(self.mask.octets))
        net: int = ip & mask
        return Address(net)


# SubNetwork
class SubNetwork(BClasses, NoDynamicAttributes):
    """SubNetwork calculator class.

    Constructor argument:
    network: Network -- The address of the network where the subnet is being searched for.
    mask: Netmask -- Subnet mask.

    Public property:
    subnets: List[Network] -- Subnet list.
    """

    __network: Network = None  # type: ignore
    __mask: Netmask = None  # type: ignore

    def __init__(self, network: Network, mask: Netmask) -> None:
        """Constructor."""
        if isinstance(network, Network) and isinstance(mask, Netmask):
            if int(network.mask) <= int(mask):
                self.__network = network
                self.__mask = mask
            else:
                raise Raise.error(
                    (
                        "The network mask must be greater then or equal to the subnet mask you are looking for."
                        f"Received: {int(network.mask)} and {int(mask)}"
                    ),
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        else:
            raise Raise.error(
                f"Expected argument of (Network, Netmask), received: ({type(network)},{type(mask)}).",
                TypeError,
                self._c_name,
                currentframe(),
            )

    @property
    def subnets(self) -> List[Network]:
        """Return subnets list."""
        tmp: List[Network] = []
        net_start = int(self.__network.network)
        net_end = int(self.__network.broadcast)
        start: int = net_start
        while True:
            subnet = Network([Address(start), self.__mask])
            tmp.append(subnet)
            if int(subnet.broadcast) >= net_end:
                break
            start = int(subnet.broadcast) + 1
        return tmp


# #[EOF]#######################################################################
