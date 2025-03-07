# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 06.12.2023

Purpose: RB /interface/
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

    AAA: str = "aaa"
    ACCESS_LIST: str = "access-list"
    ACTIVE: str = "active"  # v7
    ACTUAL_CONFIGURATION: str = "actual-configuration"
    ALIGN: str = "align"
    APN: str = "apn"
    BGP_VPLS: str = "bgp-vpls"
    BONDING: str = "bonding"
    BRIDGE: str = "bridge"
    CALEA: str = "calea"
    CAP: str = "cap"
    CAPSMAN: str = "capsman"
    CHANNEL: str = "channel"
    CHANNELS: str = "channels"
    CISCO_BGP_VPLS: str = "cisco-bgp-vpls"
    CLIENT: str = "client"  # v7
    CONFIGURATION: str = "configuration"
    CONNECT_LIST: str = "connect-list"
    DATAPATH: str = "datapath"
    DEVICE: str = "device"
    DOT1X: str = "dot1x"  # v7
    EOIP: str = "eoip"
    EOIPV6: str = "eoipv6"  # v7
    ESIM: str = "esim"
    ETHERNET: str = "ethernet"
    FDB: str = "fdb"
    FILTER: str = "filter"
    GRE6: str = "gre6"  # v7
    GRE: str = "gre"
    HOST: str = "host"
    INFO: str = "info"
    INTERWORKING: str = "interworking"
    INTERWORKING_PROFILES: str = "interworking-profiles"
    IPIP: str = "ipip"
    IPIPV6: str = "ipipv6"  # v7
    L2TP_CLIENT: str = "l2tp-client"
    L2TP_ETHER: str = "l2tp-ether"  # v7
    L2TP_SERVER: str = "l2tp-server"
    LIST: str = "list"
    LTE: str = "lte"
    MACSEC: str = "macsec"  # v7
    MANUAL_TX_POWER_TABLE: str = "manual-tx-power-table"
    MDB: str = "mdb"
    MEMBER: str = "member"
    MESH: str = "mesh"
    MSTI: str = "msti"
    MST_OVERRIDE: str = "mst-override"
    NAT: str = "nat"
    NEIGHBOR_GROUP: str = "neighbor-group"
    NSTREME: str = "nstreme"
    NSTREME_DUAL: str = "nstreme-dual"
    OVPN_CLIENT: str = "ovpn-client"
    OVPN_SERVER: str = "ovpn-server"
    PACKET: str = "packet"
    PEERS: str = "peers"
    POE: str = "poe"
    PORT: str = "port"
    PORT_CONTROLLER: str = "port-controller"
    PORT_EXTENDER: str = "port-extender"
    PORT_ISOLATION: str = "port-isolation"
    PPPOE_CLIENT: str = "pppoe-client"
    PPPOE_SERVER: str = "pppoe-server"
    PPP_CLIENT: str = "ppp-client"
    PPP_SERVER: str = "ppp-server"
    PPTP_CLIENT: str = "pptp-client"
    PPTP_SERVER: str = "pptp-server"
    PROFILE: str = "profile"  # v7
    PROVISIONING: str = "provisioning"
    RADIO: str = "radio"
    REGISTRATION_TABLE: str = "registration-table"
    REMOTE_CAP: str = "remote-cap"
    ROOT: str = "interface"
    RULE: str = "rule"
    SECURITY: str = "security"
    SECURITY_PROFILES: str = "security-profiles"
    SERVER: str = "server"  # v7
    SETTINGS: str = "settings"
    SNIFFER: str = "sniffer"
    SNOOPER: str = "snooper"
    SSTP_CLIENT: str = "sstp-client"
    SSTP_SERVER: str = "sstp-server"
    STATE: str = "state"  # v7
    STATION: str = "station"
    STEERING: str = "steering"
    SWITCH: str = "switch"
    VETH: str = "veth"  # v7
    VIRTUAL_ETHERNET: str = "virtual-ethernet"
    VLAN: str = "vlan"
    VPLS: str = "vpls"
    VRRP: str = "vrrp"
    VTEPS: str = "vteps"  # v7
    VXLAN: str = "vxlan"  # v7
    W60G: str = "w60g"
    WDS: str = "wds"
    WIFI: str = "wifi"  # v7
    WIREGUARD: str = "wireguard"  # v7
    WIRELESS: str = "wireless"
    _6TO4_: str = "6to4"  # v7


class RBInterface(BRouterOS):
    """Interface class

    For command root: /interface/
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
            _Elements._6TO4_: {},
            _Elements.BONDING: {},
            _Elements.BRIDGE: {
                _Elements.CALEA: {},
                _Elements.FILTER: {},
                _Elements.HOST: {},
                _Elements.MDB: {},
                _Elements.MSTI: {},
                _Elements.NAT: {},
                _Elements.PORT: {
                    _Elements.MST_OVERRIDE: {},
                },
                _Elements.PORT_CONTROLLER: {
                    _Elements.DEVICE: {},
                    _Elements.PORT: {
                        _Elements.POE: {},
                    },
                },
                _Elements.PORT_EXTENDER: {},
                _Elements.SETTINGS: {},
                _Elements.VLAN: {},
            },
            _Elements.DOT1X: {
                _Elements.CLIENT: {},
                _Elements.SERVER: {_Elements.ACTIVE: {}, _Elements.STATE: {}},
            },
            _Elements.EOIP: {},
            _Elements.EOIPV6: {},
            _Elements.ETHERNET: {
                _Elements.SWITCH: {
                    _Elements.HOST: {},
                    _Elements.PORT: {},
                    _Elements.PORT_ISOLATION: {},
                    _Elements.RULE: {},
                    _Elements.VLAN: {},
                },
                _Elements.POE: {},
            },
            _Elements.GRE: {},
            _Elements.GRE6: {},
            _Elements.IPIP: {},
            _Elements.IPIPV6: {},
            _Elements.L2TP_CLIENT: {},
            _Elements.L2TP_ETHER: {},
            _Elements.L2TP_SERVER: {_Elements.SERVER: {}},
            _Elements.LIST: {_Elements.MEMBER: {}},
            _Elements.LTE: {
                _Elements.APN: {},
                _Elements.ESIM: {},
                _Elements.SETTINGS: {},
            },
            _Elements.MACSEC: {_Elements.PROFILE: {}},
            _Elements.MESH: {_Elements.FDB: {}, _Elements.PORT: {}},
            _Elements.OVPN_CLIENT: {},
            _Elements.OVPN_SERVER: {_Elements.SERVER: {}},
            _Elements.PPP_CLIENT: {},
            _Elements.PPP_SERVER: {},
            _Elements.PPPOE_CLIENT: {},
            _Elements.PPPOE_SERVER: {_Elements.SERVER: {}},
            _Elements.SSTP_CLIENT: {},
            _Elements.SSTP_SERVER: {_Elements.SERVER: {}},
            _Elements.VETH: {},
            _Elements.VIRTUAL_ETHERNET: {},
            _Elements.VLAN: {},
            _Elements.VPLS: {
                _Elements.BGP_VPLS: {},
                _Elements.CISCO_BGP_VPLS: {},
            },
            _Elements.VRRP: {},
            _Elements.VXLAN: {_Elements.FDB: {}, _Elements.VTEPS: {}},
            _Elements.WIFI: {
                _Elements.AAA: {},
                _Elements.ACCESS_LIST: {},
                _Elements.ACTUAL_CONFIGURATION: {},
                _Elements.CAP: {},
                _Elements.CAPSMAN: {_Elements.REMOTE_CAP: {}},
                _Elements.CHANNEL: {},
                _Elements.CONFIGURATION: {},
                _Elements.DATAPATH: {},
                _Elements.INTERWORKING: {},
                _Elements.PROVISIONING: {},
                _Elements.RADIO: {},
                _Elements.REGISTRATION_TABLE: {},
                _Elements.SECURITY: {},
                _Elements.STEERING: {_Elements.NEIGHBOR_GROUP: {}},
            },
            _Elements.WIREGUARD: {
                _Elements.PEERS: {},
            },
            _Elements.W60G: {
                _Elements.STATION: {},
            },
            _Elements.WIRELESS: {
                _Elements.ACCESS_LIST: {},
                _Elements.ALIGN: {},
                _Elements.CAP: {},
                _Elements.CHANNELS: {},
                _Elements.CONNECT_LIST: {},
                _Elements.INFO: {},
                _Elements.INTERWORKING_PROFILES: {},
                _Elements.MANUAL_TX_POWER_TABLE: {},
                _Elements.NSTREME: {},
                _Elements.NSTREME_DUAL: {},
                _Elements.REGISTRATION_TABLE: {},
                _Elements.SECURITY_PROFILES: {},
                _Elements.SNIFFER: {
                    _Elements.PACKET: {},
                },
                _Elements.SNOOPER: {},
                _Elements.WDS: {},
            },
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
