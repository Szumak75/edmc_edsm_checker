# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2025-08-29

Purpose: Provide helpers for IPv4/IPv6 reachability checks, traceroute and host
validation utilities used by NetTool modules.

This module aggregates lightweight wrappers around `ping`, `traceroute` and
`socket.getaddrinfo`, exposing a consistent API across supported platforms.
"""

import os
import re
import socket
import subprocess

from inspect import currentframe
from typing import Optional, Dict, List, Tuple
from socket import getaddrinfo
from re import Pattern

from .basetool.data import BData
from .attribtool import ReadOnlyClass
from .attribtool import NoDynamicAttributes
from .netaddresstool.ipv4 import Address
from .netaddresstool.ipv6 import Address6
from .raisetool import Raise

try:
    # For Python < 3.12
    from distutils.spawn import find_executable
except ImportError:
    # For Python >= 3.12
    from shutil import which as find_executable


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys definition class.

    For internal purpose only.
    """

    CMD: str = "cmd"
    COMMAND: str = "__command_found__"
    COMMANDS: str = "__commands__"
    MULTIPLIER: str = "__multiplier__"
    OPTS: str = "opts"
    TIMEOUT: str = "__timeout__"


class Pinger(BData):
    """Ping remote IPv4 hosts using available system utilities."""

    def __init__(self, timeout: int = 1) -> None:
        """Initialise pinger configuration.

        ### Arguments:
        * timeout: int - Timeout in seconds applied to the selected system command.

        ### Returns:
        None - Constructor.

        ### Raises:
        * ValueError: Propagated from `BData._set_data` when invalid timeout is provided.
        """
        self._set_data(key=_Keys.TIMEOUT, value=timeout, set_default_type=int)
        self._set_data(key=_Keys.COMMANDS, value=[], set_default_type=List)
        self._set_data(key=_Keys.MULTIPLIER, value=1, set_default_type=int)

        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "fping",
                _Keys.MULTIPLIER: 1000,
                _Keys.OPTS: "-AaqR -B1 -r2 -t{} {} >/dev/null 2>&1",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                # FreeBSD ping
                _Keys.CMD: "ping",
                _Keys.MULTIPLIER: 1000,
                _Keys.OPTS: "-Qqo -c3 -W{} {} >/dev/null 2>&1",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                # Linux ping
                _Keys.CMD: "ping",
                _Keys.MULTIPLIER: 1,
                _Keys.OPTS: "-q -c3 -W{} {} >/dev/null 2>&1",
            }
        )
        tmp: Optional[Tuple[str, int]] = self.__is_tool
        if tmp:
            (command, multiplier) = tmp
            self._set_data(key=_Keys.COMMAND, value=command, set_default_type=str)
            self._set_data(key=_Keys.MULTIPLIER, value=multiplier)

    def is_alive(self, ip: str) -> bool:
        """Check whether the target host responds to ICMP echo.

        ### Arguments:
        * ip: str - IPv4 address to probe.

        ### Returns:
        bool - True when the remote host replies successfully.

        ### Raises:
        * ChildProcessError: Raised when no suitable ping command is available.
        """
        command: Optional[str] = self._get_data(key=_Keys.COMMAND)
        timeout: int = self._get_data(key=_Keys.TIMEOUT)  # type: ignore
        multiplier: int = self._get_data(key=_Keys.MULTIPLIER)  # type: ignore
        if command is None:
            raise Raise.error(
                "Command for testing ICMP echo not found.",
                ChildProcessError,
                self._c_name,
                currentframe(),
            )
        if (
            os.system(
                command.format(
                    int(timeout * multiplier),
                    str(Address(ip)),
                )
            )
        ) == 0:
            return True
        return False

    @property
    def __is_tool(self) -> Optional[Tuple[str, int]]:
        """Determine the first available ping command tuple.

        ### Returns:
        Optional[Tuple[str, int]] - Formatted command template and timeout multiplier
        if the underlying system utility is operational, otherwise None.
        """
        for cmd in self._get_data(key=_Keys.COMMANDS):  # type: ignore
            if find_executable(cmd[_Keys.CMD]) is not None:
                test_cmd: str = f"{cmd[_Keys.CMD]} {cmd[_Keys.OPTS]}"
                multiplier: int = cmd[_Keys.MULTIPLIER]
                if (
                    os.system(
                        test_cmd.format(
                            int(self._get_data(key=_Keys.TIMEOUT) * multiplier),  # type: ignore
                            "127.0.0.1",
                        )
                    )
                    == 0
                ):
                    return test_cmd, multiplier
        return None


class Tracert(BData):
    """Execute traceroute commands against IPv4 destinations."""

    def __init__(self) -> None:
        """Initialise traceroute command definitions.

        ### Returns:
        None - Constructor populates command candidates.
        """
        self._set_data(key=_Keys.COMMANDS, value=[], set_default_type=List)
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-I -q2 -S -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-P UDP -q2 -S -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-I -q2 -e -w1 -n -m 10",
            }
        )
        self._get_data(key=_Keys.COMMANDS).append(  # type: ignore
            {
                _Keys.CMD: "traceroute",
                _Keys.OPTS: "-U -q2 -e -w1 -n -m 10",
            }
        )
        self._set_data(
            key=_Keys.COMMAND, value=self.__is_tool, set_default_type=Optional[Dict]
        )

    @property
    def __is_tool(self) -> Optional[Dict]:
        """Choose a working traceroute command definition.

        ### Returns:
        Optional[Dict] - Command descriptor containing executable and options when
        a traceroute utility is reachable, otherwise None.
        """
        for cmd in self._get_data(key=_Keys.COMMANDS):  # type: ignore
            if find_executable(cmd[_Keys.CMD]) is not None:
                if (
                    os.system(
                        "{} {} {} > /dev/null 2>&1".format(
                            cmd[_Keys.CMD], cmd[_Keys.OPTS], "127.0.0.1"
                        )
                    )
                    == 0
                ):
                    out = {}
                    out.update(cmd)
                    return out
        return None

    def execute(self, ip: str) -> List[str]:
        """Run traceroute against the provided IPv4 address.

        ### Arguments:
        * ip: str - Destination IPv4 address to trace.

        ### Returns:
        List[str] - Lines captured from traceroute output.

        ### Raises:
        * ChildProcessError: Raised when no traceroute utility is available.
        """
        command: Optional[Dict] = self._get_data(key=_Keys.COMMAND)
        if command is None:
            raise Raise.error(
                "Command for testing traceroute not found.",
                ChildProcessError,
                self._c_name,
                currentframe(),
            )
        out: List[str] = []
        args: List[str] = []
        args.append(command[_Keys.CMD])
        args.extend(command[_Keys.OPTS].split(" "))
        args.append(str(Address(ip)))

        # Unexpected output but possible:
        # traceroute to 192.168.255.255 (192.168.255.255), 10 hops max, 60 byte packets
        # 1  * *
        # 2  * *
        # 3  * *
        # 4  * *
        # 5  * *
        # 6  * *
        # 7  * *
        # 8  * *
        # 9  * *
        # 10  * *

        with subprocess.Popen(
            args,
            env={
                "PATH": "/bin:/sbin:/usr/bin:/usr/sbin",
            },
            stdout=subprocess.PIPE,
        ) as proc:
            if proc.stdout is not None:
                for line in proc.stdout:
                    out.append(line.decode("utf-8"))
        return out


class HostResolvableChecker(NoDynamicAttributes):
    """Utility helpers for validating and resolving host identifiers."""

    @staticmethod
    def is_resolvable(host: str) -> bool:
        """Check whether DNS can resolve the provided host.

        ### Arguments:
        * host: str - Hostname or IP literal to inspect.

        ### Returns:
        bool - True when `socket.getaddrinfo` resolves the host.
        """
        try:
            getaddrinfo(host, None)
            return True
        except Exception:
            return False

    @staticmethod
    def is_ip_address(host: str) -> bool:
        """Check if the supplied host represents an IPv4 or IPv6 address.

        ### Arguments:
        * host: str - Hostname or IP literal to inspect.

        ### Returns:
        bool - True when the string parses into either `Address` or `Address6`.
        """
        try:
            Address(host)
            return True
        except Exception:
            pass

        try:
            Address6(host)
            return True
        except Exception:
            pass

        return False

    @staticmethod
    def is_hostname(host: str) -> bool:
        """Validate whether the string matches hostname conventions.

        ### Arguments:
        * host: str - Hostname or IP literal to inspect.

        ### Returns:
        bool - True when the string satisfies hostname formatting rules.
        """
        if HostResolvableChecker.is_ip_address(host):
            return False

        # Basic regex for hostname validation
        hostname_regex: Pattern[str] = re.compile(
            r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
        )

        return bool(hostname_regex.match(host))

    @staticmethod
    def validate_host(host: str) -> Optional[str]:
        """Verify whether the host is a valid IP address or resolvable hostname.

        ### Arguments:
        * host: str - Hostname or IP literal to validate.

        ### Returns:
        Optional[str] - None when valid, otherwise an explanatory error message.
        """
        if HostResolvableChecker.is_ip_address(host):
            return None

        if HostResolvableChecker.is_hostname(host):
            if HostResolvableChecker.is_resolvable(host):
                return None
            else:
                return f"Hostname '{host}' is not resolvable."

        return f"'{host}' is neither a valid IP address nor a valid hostname."

    @staticmethod
    def ip_from_hostname(hostname: str) -> Optional[str]:
        """Return the first IP resolved for a hostname.

        ### Arguments:
        * hostname: str - Hostname to resolve using system DNS.

        ### Returns:
        Optional[str] - First resolved address string or None when resolution fails.
        """
        try:
            addr_info = getaddrinfo(hostname, None)
            if addr_info:
                return f"{addr_info[0][4][0]}"
            return None
        except Exception:
            return None

    @staticmethod
    def validate_hosts(hosts: List[str]) -> Dict[str, Optional[str]]:
        """Validate multiple hosts in bulk.

        ### Arguments:
        * hosts: List[str] - Collection of hostnames or IP literals to validate.

        ### Returns:
        Dict[str, Optional[str]] - Mapping of host strings to validation errors or None.
        """
        results = {}
        for host in hosts:
            results[host] = HostResolvableChecker.validate_host(host)
        return results

    @staticmethod
    def filter_valid_hosts(hosts: List[str]) -> List[str]:
        """Return only valid hosts from the provided sequence.

        ### Arguments:
        * hosts: List[str] - Hostnames or IP literals to inspect.

        ### Returns:
        List[str] - Subset containing only valid hosts.
        """
        return [
            host for host in hosts if HostResolvableChecker.validate_host(host) is None
        ]

    @staticmethod
    def filter_invalid_hosts(hosts: List[str]) -> Dict[str, str]:
        """Return invalid hosts with diagnostic messages.

        ### Arguments:
        * hosts: List[str] - Hostnames or IP literals to inspect.

        ### Returns:
        Dict[str, str] - Mapping of invalid host strings to error explanations.
        """
        results = {}
        for host in hosts:
            error: Optional[str] = HostResolvableChecker.validate_host(host)
            if error is not None:
                results[host] = error
        return results

    @staticmethod
    def ip4_from_hostname(hostname: str) -> Optional[Address]:
        """Resolve the first IPv4 address for the hostname.

        ### Arguments:
        * hostname: str - Hostname to resolve as IPv4.

        ### Returns:
        Optional[Address] - First IPv4 `Address` instance or None when resolution fails.
        """
        try:
            addr_info = getaddrinfo(hostname, None, family=socket.AF_INET)
            if addr_info:
                return Address(addr_info[0][4][0])
            return None
        except Exception:
            return None

    @staticmethod
    def ip6_from_hostname(hostname: str) -> Optional[Address6]:
        """Resolve the first IPv6 address for the hostname.

        ### Arguments:
        * hostname: str - Hostname to resolve as IPv6.

        ### Returns:
        Optional[Address6] - First IPv6 `Address6` instance or None when resolution fails.
        """
        try:
            addr_info = getaddrinfo(hostname, None, family=socket.AF_INET6)
            if addr_info:
                return Address6(addr_info[0][4][0])
            return None
        except Exception:
            return None


# #[EOF]#######################################################################
