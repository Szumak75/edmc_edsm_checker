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


# #[EOF]#######################################################################
