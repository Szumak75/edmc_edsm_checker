# -*- coding: utf-8 -*-
"""
  keys.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 5.10.2024, 22:42:17
  
  Purpose: 
"""


from checker.jsktoolbox.attribtool import ReadOnlyClass


class CheckerKeys(object, metaclass=ReadOnlyClass):
    """Private Keys class."""

    # base data
    JUMP_SYSTEM: str = "_js_"
    PLUGIN_NAME: str = "_pn_"
    SHUTTING_DOWN: str = "_shut_d_"
    STATUS: str = "__status__"
    TH_SEARCH: str = "__search__"
    VERSION: str = "_ver_"

    # base logs
    LOGGER: str = "__logger__"
    LOG_PROCESSOR: str = "__logs_processor__"
    LOG_QUEUE: str = "__logger_queue__"
    TH_LOGGER: str = "__th_logger__"

    # stars system
    SS_NAME: str = "__ss_name__"
    SS_ADDRESS: str = "__ss_address__"
    SS_POS_X: str = "__ss_pos_x__"
    SS_POS_Y: str = "__ss_pos_y__"
    SS_POS_Z: str = "__ss_pos_z__"
    SS_DATA: str = "__ss_data__"

    # SYSTEM
    DIR: str = "__dir__"


# #[EOF]#######################################################################
