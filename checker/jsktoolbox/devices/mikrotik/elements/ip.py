# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 06.12.2023

Purpose: RB '/ip/'
"""

from typing import Dict, Optional, Any

from ....logstool.queue import LoggerQueue

from ....attribtool import ReadOnlyClass
from ....logstool.logs import LoggerClient
from ..base import BRouterOS, BDev
from ...network.connectors import IConnector


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ACCESS: str = "access"
    ACCOUNTING: str = "accounting"
    ACTIVE: str = "active"
    ACTIVE_PEERS: str = "active-peers"
    ADDRESS: str = "address"
    ADDRESS_LIST: str = "address-list"
    ADVANCED: str = "advanced"
    ALERT: str = "alert"
    ALL: str = "all"
    ARP: str = "arp"
    CACHE: str = "cache"
    CACHE_CONTENTS: str = "cache-contents"
    CALEA: str = "calea"
    CLOUD: str = "cloud"
    CONFIG: str = "config"
    CONNECTION: str = "connection"
    CONNECTIONS: str = "connections"
    COOKIE: str = "cookie"
    DEVICE: str = "device"
    DHCP_CLIENT: str = "dhcp-client"
    DHCP_RELAY: str = "dhcp-relay"
    DHCP_SERVER: str = "dhcp-server"
    DIRECT: str = "direct"
    DISCOVERY_SETTINGS: str = "discovery-settings"
    DNS: str = "dns"
    FILTER: str = "filter"
    FIREWALL: str = "firewall"
    GROUP: str = "group"
    HOST: str = "host"
    HOTSPOT: str = "hotspot"
    IDENTITY: str = "identity"
    INSERTS: str = "inserts"
    INSTALLED_SA: str = "installed-sa"
    INTERFACES: str = "interfaces"
    IP: str = "ip"
    IPFIX: str = "ipfix"
    IPSEC: str = "ipsec"
    IP_BINDING: str = "ip-binding"
    KEY: str = "key"
    KID_CONTROL: str = "kid-control"
    LAYER7_PROTOCOL: str = "layer7-protocol"
    LEASE: str = "lease"
    LOOKUPS: str = "lookups"
    MANGLE: str = "mangle"
    MATCHER: str = "matcher"
    MODE_CONFIG: str = "mode-config"
    NAT: str = "nat"
    NAT_PMP: str = "nat-pmp"  # v7
    NEIGHBOR: str = "neighbor"
    NETWORK: str = "network"
    NEXTHOP: str = "nexthop"
    OPTION: str = "option"
    PACKING: str = "packing"
    PEER: str = "peer"
    POLICY: str = "policy"
    POOL: str = "pool"
    PROFILE: str = "profile"
    PROPOSAL: str = "proposal"
    PROXY: str = "proxy"
    RAW: str = "raw"
    REFRESHES: str = "refreshes"
    ROOT: str = "ip"
    ROUTE: str = "route"
    RULE: str = "rule"
    SERVICE: str = "service"
    SERVICE_PORT: str = "service-port"
    SETS: str = "sets"
    SETTINGS: str = "settings"
    SHARES: str = "shares"
    SMB: str = "smb"
    SNAPSHOT: str = "snapshot"
    SOCKS: str = "socks"
    SSH: str = "ssh"
    STATIC: str = "static"
    STATISTICS: str = "statistics"
    TARGET: str = "target"
    TFTP: str = "tftp"
    TRACKING: str = "tracking"
    TRAFFIC_FLOW: str = "traffic-flow"
    UNCOUNTED: str = "uncounted"
    UPNP: str = "upnp"
    USED: str = "used"
    USER: str = "user"
    USERS: str = "users"
    VRF: str = "vrf"
    WALLED_GARDEN: str = "walled-garden"
    WEB_ACCESS: str = "web-access"


class RBIp(BRouterOS):
    """Ip class

    For command root: /ip/
    """

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        super().__init__(
            parent,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.root = f"{_Elements.ROOT}/"

        # add elements
        elements: Dict[str, Any] = {
            _Elements.ACCOUNTING: {
                _Elements.SNAPSHOT: {},
                _Elements.UNCOUNTED: {},
                _Elements.WEB_ACCESS: {},
            },
            _Elements.ADDRESS: {},
            _Elements.ARP: {},
            _Elements.CLOUD: {
                _Elements.ADVANCED: {},
            },
            _Elements.DHCP_CLIENT: {
                _Elements.OPTION: {},
            },
            _Elements.DHCP_RELAY: {},
            _Elements.DHCP_SERVER: {
                _Elements.ALERT: {},
                _Elements.CONFIG: {},
                _Elements.LEASE: {},
                _Elements.MATCHER: {},
                _Elements.NETWORK: {},
                _Elements.OPTION: {
                    _Elements.SETS: {},
                },
            },
            _Elements.DNS: {
                _Elements.CACHE: {
                    _Elements.ALL: {},
                },
                _Elements.STATIC: {},
            },
            _Elements.FIREWALL: {
                _Elements.ADDRESS_LIST: {},
                _Elements.CALEA: {},
                _Elements.CONNECTION: {
                    _Elements.TRACKING: {},
                },
                _Elements.FILTER: {},
                _Elements.LAYER7_PROTOCOL: {},
                _Elements.MANGLE: {},
                _Elements.NAT: {},
                _Elements.RAW: {},
                _Elements.SERVICE_PORT: {},
            },
            _Elements.HOTSPOT: {
                _Elements.ACTIVE: {},
                _Elements.COOKIE: {},
                _Elements.HOST: {},
                _Elements.IP_BINDING: {},
                _Elements.PROFILE: {},
                _Elements.SERVICE_PORT: {},
                _Elements.USER: {
                    _Elements.PROFILE: {},
                },
                _Elements.WALLED_GARDEN: {
                    _Elements.IP: {},
                },
            },
            _Elements.IPSEC: {
                _Elements.ACTIVE_PEERS: {},
                _Elements.IDENTITY: {},
                _Elements.INSTALLED_SA: {},
                _Elements.KEY: {},
                _Elements.MODE_CONFIG: {},
                _Elements.PEER: {},
                _Elements.POLICY: {
                    _Elements.GROUP: {},
                },
                _Elements.PROFILE: {},
                _Elements.PROPOSAL: {},
                _Elements.SETTINGS: {},
                _Elements.STATISTICS: {},
            },
            _Elements.KID_CONTROL: {
                _Elements.DEVICE: {},
            },
            _Elements.NAT_PMP: {_Elements.INTERFACES: {}},
            _Elements.NEIGHBOR: {
                _Elements.DISCOVERY_SETTINGS: {},
            },
            _Elements.PACKING: {},
            _Elements.POOL: {
                _Elements.USED: {},
            },
            _Elements.PROXY: {
                _Elements.ACCESS: {},
                _Elements.CACHE: {},
                _Elements.CACHE_CONTENTS: {},
                _Elements.CONNECTIONS: {},
                _Elements.DIRECT: {},
                _Elements.INSERTS: {},
                _Elements.LOOKUPS: {},
                _Elements.REFRESHES: {},
            },
            _Elements.ROUTE: {
                _Elements.CACHE: {},
                _Elements.NEXTHOP: {},
                _Elements.RULE: {},
                _Elements.VRF: {},
            },
            _Elements.SERVICE: {},
            _Elements.SETTINGS: {},
            _Elements.SMB: {
                _Elements.SHARES: {},
                _Elements.USERS: {},
            },
            _Elements.SOCKS: {
                _Elements.ACCESS: {},
                _Elements.CONNECTIONS: {},
                _Elements.USERS: {},
            },
            _Elements.SSH: {},
            _Elements.TFTP: {
                _Elements.SETTINGS: {},
            },
            _Elements.TRAFFIC_FLOW: {
                _Elements.IPFIX: {},
                _Elements.TARGET: {},
            },
            _Elements.UPNP: {
                _Elements.INTERFACES: {},
            },
            _Elements.VRF: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
