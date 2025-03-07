# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 08.12.2023

Purpose: RB '/routing/'
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

    ADVERTISEMENTS: str = "advertisements"
    AGGREGATE: str = "aggregate"
    AREA: str = "area"
    AREA_BORDER_ROUTER: str = "area-border-router"
    AS_BORDER_ROUTER: str = "as-border-router"
    BFD: str = "bfd"
    BGP: str = "bgp"
    BSR: str = "bsr"
    BSR_CANDIDATES: str = "bsr-candidates"
    CANDIDATE: str = "candidate"
    CHAIN: str = "chain"
    COMMUNITY_EXT_LIST: str = "community-ext-list"
    COMMUNITY_LARGE_LIST: str = "community-large-list"
    COMMUNITY_LIST: str = "community-list"
    CONFIGURATION: str = "configuration"
    CONNECTION: str = "connection"
    FANTASY: str = "fantasy"  # v7
    FILTER: str = "filter"
    GMP: str = "gmp"  # v7
    ID: str = "id"  # v7
    IGMP_GROUP: str = "igmp-group"
    IGMP_INTERFACE_TEMPLATE: str = "igmp-interface-template"
    IGMP_PROXY: str = "igmp-proxy"
    INSTANCE: str = "instance"
    INTERFACE: str = "interface"
    INTERFACE_TEMPLATE: str = "interface-template"
    ISIS: str = "isis"  # v7
    JOIN: str = "join"
    KEYS: str = "keys"
    LSA: str = "lsa"
    LSP: str = "lsp"
    MEMORY: str = "memory"
    MFC: str = "mfc"
    MME: str = "mme"  # v6
    MRIB: str = "mrib"
    NBMA_NEIGHBOR: str = "nbma-neighbor"
    NEIGHBOR: str = "neighbor"
    NEIGHBORS: str = "neighbors"
    NETWORK: str = "network"
    NEXTHOP: str = "nexthop"  # v7
    NUM_LIST: str = "num-list"
    ORIGIN: str = "origin"
    ORIGINATORS: str = "originators"
    OSPF: str = "ospf"
    OSPF_ROUTER: str = "ospf-router"
    OSPF_V3: str = "ospf-v3"  # v6
    PCAP: str = "pcap"
    PEER: str = "peer"
    PIM: str = "pim"  # v6
    PIMSM: str = "pimsm"  # v7
    PREFIX_LIST: str = "prefix-lists"  # v6
    PROCESS: str = "process"
    RANGE: str = "range"
    RIP: str = "rip"
    RIPNG: str = "ripng"  # v6
    ROOT: str = "routing"
    ROUTE: str = "route"  # v7
    RP: str = "rp"
    RPKI: str = "rpki"  # v7
    RP_CANDIDATE: str = "rp-candidate"
    RP_CANDIDATES: str = "rp-candidates"
    RP_SET: str = "rp-set"
    RULE: str = "rule"  # v7
    SELECT_RULE: str = "select-rule"
    SESSION: str = "session"
    SETTINGS: str = "settings"  # v7
    SHAM_LINK: str = "sham-link"
    STATIC_NEIGHBOR: str = "static-neighbor"
    STATIC_RP: str = "static-rp"
    STATS: str = "stats"  # v7
    STEP: str = "step"
    TABLE: str = "table"  # v7
    TEMPLATE: str = "template"
    UIB_G: str = "uib-g"
    UIB_SG: str = "uib-sg"
    VIRTUAL_LINK: str = "virtual-link"
    VPLS: str = "vpls"
    VPN: str = "vpn"
    VPNV4_ROUTE: str = "vpnv4-route"
    VRF: str = "vrf"


class RBRouting(BRouterOS):
    """Routing class

    For command root: /routing/
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
            _Elements.BFD: {
                _Elements.INTERFACE: {},
                _Elements.NEIGHBOR: {},
                _Elements.CONFIGURATION: {},
                _Elements.SESSION: {},
            },
            _Elements.BGP: {
                _Elements.ADVERTISEMENTS: {},
                _Elements.AGGREGATE: {},
                _Elements.CONNECTION: {},
                _Elements.INSTANCE: {
                    _Elements.VRF: {},
                },
                _Elements.NETWORK: {},
                _Elements.PEER: {},
                _Elements.SESSION: {},
                _Elements.TEMPLATE: {},
                _Elements.VPLS: {},
                _Elements.VPN: {},
                _Elements.VPNV4_ROUTE: {},
            },
            _Elements.FANTASY: {},
            _Elements.FILTER: {
                _Elements.CHAIN: {},
                _Elements.COMMUNITY_EXT_LIST: {},
                _Elements.COMMUNITY_LARGE_LIST: {},
                _Elements.COMMUNITY_LIST: {},
                _Elements.NUM_LIST: {},
                _Elements.RULE: {},
                _Elements.SELECT_RULE: {},
            },
            _Elements.GMP: {},
            _Elements.ID: {},
            _Elements.IGMP_PROXY: {
                _Elements.INTERFACE: {},
                _Elements.MFC: {},
            },
            _Elements.ISIS: {
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.LSP: {},
                _Elements.NEIGHBOR: {},
            },
            _Elements.NEXTHOP: {},
            _Elements.MME: {
                _Elements.INTERFACE: {},
                _Elements.NETWORK: {},
                _Elements.ORIGINATORS: {},
            },
            _Elements.OSPF: {
                _Elements.AREA: {
                    _Elements.RANGE: {},
                },
                _Elements.AREA_BORDER_ROUTER: {},
                _Elements.AS_BORDER_ROUTER: {},
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.LSA: {},
                _Elements.NBMA_NEIGHBOR: {},
                _Elements.NEIGHBOR: {},
                _Elements.NETWORK: {},
                _Elements.ROUTE: {},
                _Elements.SHAM_LINK: {},
                _Elements.STATIC_NEIGHBOR: {},
                _Elements.VIRTUAL_LINK: {},
            },
            _Elements.OSPF_V3: {
                _Elements.AREA: {_Elements.RANGE: {}},
                _Elements.AS_BORDER_ROUTER: {},
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.LSA: {},
                _Elements.NBMA_NEIGHBOR: {},
                _Elements.NEIGHBOR: {},
                _Elements.OSPF_ROUTER: {},
                _Elements.ROUTE: {},
                _Elements.VIRTUAL_LINK: {},
            },
            _Elements.PIM: {
                _Elements.BSR: {},
                _Elements.BSR_CANDIDATES: {},
                _Elements.IGMP_GROUP: {},
                _Elements.INTERFACE: {},
                _Elements.JOIN: {},
                _Elements.MFC: {},
                _Elements.MRIB: {},
                _Elements.NEIGHBORS: {},
                _Elements.RP: {},
                _Elements.RP_CANDIDATES: {},
            },
            _Elements.PIMSM: {
                _Elements.BSR: {
                    _Elements.CANDIDATE: {},
                    _Elements.RP_CANDIDATE: {},
                    _Elements.RP_SET: {},
                },
                _Elements.IGMP_INTERFACE_TEMPLATE: {},
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.NEIGHBOR: {},
                _Elements.STATIC_RP: {},
                _Elements.UIB_G: {},
                _Elements.UIB_SG: {},
            },
            _Elements.PREFIX_LIST: {},
            _Elements.RIP: {
                _Elements.INSTANCE: {},
                _Elements.INTERFACE: {},
                _Elements.INTERFACE_TEMPLATE: {},
                _Elements.KEYS: {},
                _Elements.NEIGHBOR: {},
                _Elements.NETWORK: {},
                _Elements.ROUTE: {},
                _Elements.STATIC_NEIGHBOR: {},
            },
            _Elements.RIPNG: {_Elements.INTERFACE: {}, _Elements.ROUTE: {}},
            _Elements.ROUTE: {
                _Elements.RULE: {},
            },
            _Elements.RPKI: {
                _Elements.SESSION: {},
            },
            _Elements.RULE: {},
            _Elements.SETTINGS: {},
            _Elements.STATS: {
                _Elements.MEMORY: {},
                _Elements.ORIGIN: {},
                _Elements.PCAP: {},
                _Elements.PROCESS: {},
                _Elements.STEP: {},
            },
            _Elements.TABLE: {},
        }

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
