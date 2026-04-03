# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-09-06

Purpose: Provide helpers for command-line parsing, environment inspection,
and filesystem path validation used across the toolkit.
"""


import os
import sys
import getopt
import tempfile
import subprocess
import warnings

from inspect import currentframe
from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict, Any


from .attribtool import ReadOnlyClass
from .raisetool import Raise
from .basetool.data import BData


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ARGS: str = "__args__"
    CONFIGURED_ARGS: str = "__conf_args__"
    DESC_OPTS: str = "__desc_opts__"
    EXAMPLE_OPTS: str = "__ex_opts__"
    EXISTS: str = "__exists__"
    HOME: str = "__home__"
    IS_DIR: str = "__is_dir__"
    IS_FILE: str = "__is_file__"
    IS_SYMLINK: str = "__is_symlink__"
    LIST: str = "__list__"
    LONG_OPTS: str = "__long_opts__"
    PATH_NAME: str = "__pathname__"
    POSIXPATH: str = "__posix_path__"
    SHORT_OPTS: str = "__short_opts__"
    SPLIT: str = "__split__"
    TMP: str = "__tmp__"


class _CommandKeys(object, metaclass=ReadOnlyClass):
    """Keys definition class for command line arguments."""

    DESCRIPTION: str = "description"
    EXAMPLE: str = "example"
    HAS_VALUE: str = "has_value"
    SHORT: str = "short"


class CommandLineParser(BData):
    """Parser for command line options."""

    def __init__(self) -> None:
        """Initialise the parser state.

        ### Returns:
        None - Constructor.
        """
        self._set_data(key=_Keys.CONFIGURED_ARGS, value={}, set_default_type=Dict)
        self._set_data(key=_Keys.ARGS, value={}, set_default_type=Dict)

    def configure_option(
        self,
        short_arg: Optional[str],
        long_arg: str,
        desc_arg: Optional[Union[str, List, Tuple]] = None,
        has_value: bool = False,
        example_value: Optional[str] = None,
    ) -> None:
        """Register a command-line option and associated metadata.

        ### Arguments:
        * short_arg: Optional[str] - Optional one-character short form (None → placeholder).
        * long_arg: str - Long option name without leading dashes.
        * desc_arg: Optional[Union[str, List, Tuple]] - Optional description or sequence of lines.
        * has_value: bool - When True the option expects a value.
        * example_value: Optional[str] - Sample value appended to help text.

        ### Returns:
        None - Parser configuration is updated.

        ### Raises:
        * AttributeError: Raised when `long_arg` is empty.
        """
        if _Keys.SHORT_OPTS not in self.__config_args:
            self.__config_args[_Keys.SHORT_OPTS] = ""
        if _Keys.LONG_OPTS not in self.__config_args:
            self.__config_args[_Keys.LONG_OPTS] = []
        if _Keys.DESC_OPTS not in self.__config_args:
            self.__config_args[_Keys.DESC_OPTS] = []
        if _Keys.EXAMPLE_OPTS not in self.__config_args:
            self.__config_args[_Keys.EXAMPLE_OPTS] = []

        if not short_arg:
            short_arg = "_"

        if not long_arg:
            raise Raise.error(
                f"A long argument name is required.",
                AttributeError,
                self._c_name,
                currentframe(),
            )

        self.__config_args[_Keys.SHORT_OPTS] += short_arg + (":" if has_value else "")
        self.__config_args[_Keys.LONG_OPTS].append(
            long_arg + ("=" if has_value else "")
        )

        tmp: Union[str, List] = ""
        if desc_arg:
            if isinstance(desc_arg, str):
                tmp = desc_arg
            elif isinstance(desc_arg, (Tuple, List)):
                tmp = []
                for desc in desc_arg:
                    tmp.append(desc)
                if not tmp:
                    tmp = ""
            else:
                tmp = str(desc_arg)
        self.__config_args[_Keys.DESC_OPTS].append(tmp)

        tmp = ""
        if example_value:
            if isinstance(example_value, str):
                tmp = example_value

        self.__config_args[_Keys.EXAMPLE_OPTS].append(tmp)

    def configure_argument(
        self,
        short_arg: Optional[str],
        long_arg: str,
        desc_arg: Optional[Union[str, List, Tuple]] = None,
        has_value: bool = False,
        example_value: Optional[str] = None,
    ) -> None:
        """[Deprecated] Wrapper preserved for backwards compatibility."""
        warnings.warn(
            "The 'configure_argument' method is deprecated, use 'configure_option' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.configure_option(short_arg, long_arg, desc_arg, has_value, example_value)

    def parse(self) -> bool:
        """Parse command-line arguments using configured option metadata.

        ### Returns:
        bool - True on successful parsing, False when getopt fails.
        """
        short_mod = str(self.__config_args[_Keys.SHORT_OPTS]).replace(":", "")
        long_mod: List[str] = [
            item.replace("=", "") for item in self.__config_args[_Keys.LONG_OPTS]
        ]

        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                self.__config_args[_Keys.SHORT_OPTS],
                self.__config_args[_Keys.LONG_OPTS],
            )
        except getopt.GetoptError as ex:
            print(f"Command line argument error: {ex}")
            return False

        for opt, value in opts:
            for short_arg, long_arg in zip(short_mod, long_mod):
                if opt in ("-" + short_arg, "--" + long_arg):
                    self.args[long_arg] = value
        return True

    def parse_arguments(self) -> bool:
        """[Deprecated] Wrapper around :meth:`parse`.

        ### Returns:
        bool - Result of :meth:`parse`.
        """
        warnings.warn(
            "The 'parse_arguments' method is deprecated, use 'parse' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.parse()

    def has_option(self, long_arg: str) -> bool:
        """Check whether the provided long option was parsed.

        ### Arguments:
        * long_arg: str - Long option name without dashes.

        ### Returns:
        bool - True when the option exists in the parsed arguments.
        """
        return long_arg in self.args

    def get_option(self, long_arg: str) -> Optional[str]:
        """Retrieve the option value converted to string.

        ### Arguments:
        * long_arg: str - Long option name without dashes.

        ### Returns:
        Optional[str] - Option value string or None when missing.
        """
        out: Optional[Any] = self.args.get(long_arg)
        if out is None:
            return None
        return str(out)

    def dump(self) -> Dict[str, Any]:
        """Return configured options metadata as a dictionary.

        ### Returns:
        Dict[str, Any] - Mapping of long option names to description metadata.
        """
        out: Dict[str, Any] = {}
        short_mod: str = str(self.__config_args[_Keys.SHORT_OPTS]).replace(":", "")

        for short_arg, long_arg, desc_arg, ex_arg in zip(
            short_mod,
            self.__config_args[_Keys.LONG_OPTS],
            self.__config_args[_Keys.DESC_OPTS],
            self.__config_args[_Keys.EXAMPLE_OPTS],
        ):
            out[long_arg] = {
                _CommandKeys.SHORT: short_arg if short_arg != "_" else "",
                _CommandKeys.HAS_VALUE: long_arg.endswith("="),
                _CommandKeys.DESCRIPTION: desc_arg,
                _CommandKeys.EXAMPLE: ex_arg,
            }
        return out

    def help(self) -> None:
        """Print a human-readable help summary to stdout.

        ### Returns:
        None - Help information printed to standard output.
        """
        command_conf: Dict[str, Any] = self.dump()
        command_opts: str = ""
        desc_opts: List[str] = []
        max_len: int = 0
        opt_value: List[str] = []
        opt_no_value: List[str] = []
        for item in command_conf.keys():
            if max_len < len(item):
                max_len = len(item)
            if command_conf[item][_CommandKeys.HAS_VALUE]:
                opt_value.append(item)
            else:
                opt_no_value.append(item)
        max_len += 7
        for item in sorted(opt_no_value):
            if command_conf[item][_CommandKeys.SHORT]:
                tmp = f"-{command_conf[item][_CommandKeys.SHORT]}|--{item} "
            else:
                tmp = f"--{item}    "
            desc_opts.append(
                f" {tmp:<{max_len}}- {command_conf[item][_CommandKeys.DESCRIPTION]}"
            )
            command_opts += tmp
        for item in sorted(opt_value):
            if command_conf[item][_CommandKeys.SHORT]:
                tmp = f"-{command_conf[item][_CommandKeys.SHORT]}|--{item}"
            else:
                tmp = f"--{item}   "
            desc_opts.append(
                f" {tmp:<{max_len}}- {command_conf[item][_CommandKeys.DESCRIPTION]}"
            )
            command_opts += tmp
            if command_conf[item][_CommandKeys.EXAMPLE]:
                command_opts += f"{command_conf[item][_CommandKeys.EXAMPLE]}"
            command_opts += " "
        print("###[HELP]###")
        print(f"{sys.argv[0]} {command_opts}")
        print()
        print("# Arguments:")
        for item in desc_opts:
            print(item)

    @property
    def args(self) -> Dict[str, Any]:
        """Return parsed argument key/value data.

        ### Returns:
        Dict[str, Any] - Parsed arguments dictionary.
        """
        return self._get_data(key=_Keys.ARGS)  # type: ignore

    @property
    def __config_args(self) -> Dict[str, Any]:
        """Return internal option configuration dictionary.

        ### Returns:
        Dict[str, Any] - Configuration structure keyed by helper constants.
        """
        return self._get_data(key=_Keys.CONFIGURED_ARGS)  # type: ignore


class Env(BData):
    """Environment class."""

    def __init__(self) -> None:
        """Initialise environment lookups."""
        home: Optional[str] = os.getenv("HOME")
        if home is None:
            home = os.getenv("HOMEPATH")
            if home is not None:
                home = f"{os.getenv('HOMEDRIVE')}{home}"
        self._set_data(key=_Keys.HOME, set_default_type=str, value=home)

        tmp: Optional[str] = os.getenv("TMP")
        if tmp is None:
            tmp = os.getenv("TEMP")
            if tmp is None:
                tmp = tempfile.gettempdir()
        self._set_data(key=_Keys.TMP, set_default_type=str, value=tmp)

    @property
    def home(self) -> str:
        """Return the detected home directory path."""
        return self._get_data(key=_Keys.HOME, default_value="")  # type: ignore

    @property
    def tmpdir(self) -> str:
        """Return the detected temporary directory path."""
        return self._get_data(key=_Keys.TMP, default_value="")  # type: ignore

    @property
    def username(self) -> str:
        """Return the effective login name if available."""
        tmp: Optional[str] = os.getenv("USER")
        if tmp:
            return tmp
        return ""

    def os_arch(self) -> str:
        """Return the operating system architecture description.

        ### Returns:
        str - Human-readable architecture string (e.g. `64-bit`).
        """
        try:
            if os.name == "nt":
                output = subprocess.check_output(
                    ["wmic", "os", "get", "OSArchitecture"],
                    stderr=subprocess.DEVNULL,
                ).decode()
                parts = output.split()
                if len(parts) > 1:
                    return parts[1]
            else:
                output = subprocess.check_output(
                    ["uname", "-m"], stderr=subprocess.DEVNULL
                ).decode()
                return "64-bit" if "64" in output else "32-bit"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        import platform

        arch, _ = platform.architecture()
        return arch or ("64-bit" if sys.maxsize > 2**32 else "32-bit")

    @property
    def is_64bits(self) -> bool:
        """Return True when the interpreter runs in 64-bit mode."""
        return sys.maxsize > 2**32


class PathChecker(BData):
    """PathChecker class for filesystem path."""

    def __init__(self, pathname: str, check_deep: bool = True) -> None:
        """Initialise path metadata for the provided pathname.

        ### Arguments:
        * pathname: str - Path string to inspect.
        * check_deep: bool - When True analyse path components recursively.

        ### Returns:
        None - Constructor.

        ### Raises:
        * TypeError: When pathname is missing or not a string.
        * ValueError: When pathname is an empty string.
        """
        if pathname is None:
            raise Raise.error(
                "Expected 'pathname' as string, not None.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(pathname, str):
            raise Raise.error(
                f"Expected 'pathname' as string, received: '{type(pathname)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if isinstance(pathname, str) and len(pathname) == 0:
            raise Raise.error(
                "'pathname' cannot be an empty string.",
                ValueError,
                self._c_name,
                currentframe(),
            )
        self._set_data(key=_Keys.PATH_NAME, value=pathname, set_default_type=str)
        self._set_data(key=_Keys.SPLIT, value=check_deep, set_default_type=bool)
        self._set_data(key=_Keys.LIST, value=[], set_default_type=List)

        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Analyse the path and populate cached metadata.

        ### Returns:
        None - Internal state updated in place.
        """
        query = Path(self._get_data(key=_Keys.PATH_NAME))  # type: ignore
        # check exists
        self._set_data(key=_Keys.EXISTS, value=query.exists(), set_default_type=bool)
        if self.exists:
            # check if is file
            self._set_data(
                key=_Keys.IS_FILE, value=query.is_file(), set_default_type=bool
            )
            # check if is dir
            self._set_data(
                key=_Keys.IS_DIR, value=query.is_dir(), set_default_type=bool
            )
            # check if is symlink
            self._set_data(
                key=_Keys.IS_SYMLINK, value=query.is_symlink(), set_default_type=bool
            )
            # resolve symlink
            self._set_data(
                key=_Keys.POSIXPATH, value=str(query.resolve()), set_default_type=str
            )

        if self._get_data(key=_Keys.SPLIT):
            # split and analyse
            tmp: str = ""
            tmp_list: List[PathChecker] = self._copy_data(key=_Keys.LIST)  # type: ignore
            for item in self.path.split(os.sep):
                if item == "":
                    continue
                tmp += f"{os.sep}{item}"
                tmp_list.append(PathChecker(tmp, False))
            self._set_data(key=_Keys.LIST, value=tmp_list)

    def __str__(self) -> str:
        """Returns class data as string."""
        return (
            "PathChecker("
            f"'pathname': '{self.path}', "
            f"'exists': '{self.exists}', "
            f"'is_dir': '{self.is_dir if self.exists else ''}', "
            f"'is_file': '{self.is_file if self.exists else ''}', "
            f"'is_symlink': '{self.is_symlink if self.exists else ''}', "
            f"'posixpath': '{self.posixpath if self.exists else ''}'"
            ")"
        )

    def __repr__(self) -> str:
        """Returns string representation."""
        return f"PathChecker('{self.path}')"

    @property
    def dirname(self) -> Optional[str]:
        """Return the directory component when the path exists.

        ### Returns:
        Optional[str] - Directory path or None when unavailable.
        """
        tmp_list: List[PathChecker] = self._get_data(key=_Keys.LIST)  # type: ignore
        if self.exists:
            last: Optional[str] = None
            for item in tmp_list:
                if item.is_dir:
                    last = item.path
            return last
        return None

    @property
    def filename(self) -> Optional[str]:
        """Return the filename component when the path points to a file.

        ### Returns:
        Optional[str] - Filename string or None.
        """
        if self.exists and self.is_file:
            tmp: list[str] = self.path.split(os.sep)
            if len(tmp) > 0:
                if tmp[-1] != "":
                    return tmp[-1]
        return None

    @property
    def exists(self) -> bool:
        """Return True when the path exists on the filesystem.

        ### Returns:
        bool - Existence flag.
        """
        return self._get_data(key=_Keys.EXISTS)  # type: ignore

    @property
    def is_dir(self) -> bool:
        """Return True when the path represents a directory.

        ### Returns:
        bool - Directory flag.
        """
        return self._get_data(key=_Keys.IS_DIR)  # type: ignore

    @property
    def is_file(self) -> bool:
        """Return True when the path represents a file.

        ### Returns:
        bool - File flag.
        """
        return self._get_data(key=_Keys.IS_FILE)  # type: ignore

    @property
    def is_symlink(self) -> bool:
        """Return True when the path represents a symlink.

        ### Returns:
        bool - Symlink flag.
        """
        return self._get_data(key=_Keys.IS_SYMLINK)  # type: ignore

    @property
    def path(self) -> str:
        """Return the original input path string.

        ### Returns:
        str - Pathname.
        """
        return self._get_data(key=_Keys.PATH_NAME)  # type: ignore

    @property
    def posixpath(self) -> Optional[str]:
        """Return the resolved POSIX path when the target exists.

        ### Returns:
        Optional[str] - Resolved path or None.
        """
        if self.exists:
            return self._get_data(key=_Keys.POSIXPATH)  # type: ignore
        return None

    def create(self) -> bool:
        """Create intermediate directories or touch file as required.

        ### Returns:
        bool - True when the path exists after creation.
        """
        tmp_list: List[PathChecker] = self._get_data(key=_Keys.LIST)  # type: ignore
        test_path: str = self.path
        file = True
        if self.path[-1] == os.sep:
            file = False
            test_path = self.path[:-1]
        for item in tmp_list:
            if item.exists:
                continue
            if item.path == test_path:
                # last element
                if file:
                    # touch file
                    with open(item.path, "w"):
                        pass
                else:
                    os.mkdir(item.path)
            else:
                os.mkdir(item.path)
        # check
        self._set_data(key=_Keys.LIST, value=[])
        self.__run__()

        return self.exists


# #[EOF]#######################################################################
