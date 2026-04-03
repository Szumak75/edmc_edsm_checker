"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-10-29

Purpose: Provide reusable networking utilities including IPv4 and IPv6 helpers.

This module exposes default safety limits for legacy list-based helpers, allowing
applications to override them globally when needed.
"""

from .ipv4 import (  # noqa: F401
    DEFAULT_IPV4_HOST_LIMIT,
    DEFAULT_IPV4_SUBNET_LIMIT,
)
from .ipv6 import (  # noqa: F401
    DEFAULT_IPV6_HOST_LIMIT,
    DEFAULT_IPV6_SUBNET_LIMIT,
)

__all__ = [
    "DEFAULT_IPV4_HOST_LIMIT",
    "DEFAULT_IPV4_SUBNET_LIMIT",
    "DEFAULT_IPV6_HOST_LIMIT",
    "DEFAULT_IPV6_SUBNET_LIMIT",
]
