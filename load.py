# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: plugin entry point.
"""


import logging
import tkinter as tk
from typing import Any, Dict, Optional, Tuple

from jsktoolbox.tktool.widgets import CreateToolTip

from config import config

from checker_libs.system import LogLevels
from checker_libs.checker import Checker

checker_object = Checker()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    checker_object.logger.debug = f"{checker_object.pluginname}->plugin_start3 start..."
    # loglevel set from config
    loglevel: Optional[int] = LogLevels().get(config.get_str("loglevel"))
    checker_object.log_processor.loglevel = (
        loglevel if loglevel is not None else logging.DEBUG
    )
    checker_object.logger.debug = f"{checker_object.pluginname}->plugin_start3 done."
    return f"{checker_object.pluginname}"


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    checker_object.logger.debug = f"{checker_object.pluginname}->plugin_stop: start..."
    checker_object.shutting_down = True
    checker_object.logger.debug = (
        f"{checker_object.pluginname}->plugin_stop: shut down flag is set"
    )
    # something to do
    # shut down logger at last
    checker_object.logger.debug = (
        f"{checker_object.pluginname}->plugin_stop: terminating the logger"
    )
    if checker_object._search:
        checker_object._search.quit()
        checker_object._search.join()
    checker_object.qlog.put(None)
    checker_object.th_log.join()


def plugin_app(parent: tk.Frame) -> Tuple[tk.Label, tk.Label]:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    checker_object.logger.debug = f"{checker_object.pluginname}->plugin_app: start..."
    # add button to main frame
    label = tk.Label(
        parent,
        text=f"Jump target:",
    )
    CreateToolTip(
        label,
        [
            f"{checker_object.pluginname} v{checker_object.version}",
            "",
            "Check EDSM database information\nabout jump target.",
        ],
    )

    status = tk.StringVar()
    status_label: tk.Label = tk.Label(parent, textvariable=status)
    checker_object.status = status
    checker_object.start_search_engine()
    return label, status_label


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """Save settings.

    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    checker_object.logger.debug = (
        f"{checker_object.pluginname}->prefs_changed: start..."
    )
    # set loglevel after config update
    loglevel: Optional[int] = LogLevels().get(config.get_str("loglevel"))
    checker_object.log_processor.loglevel = (
        loglevel if loglevel is not None else logging.DEBUG
    )
    checker_object.logger.debug = f"{checker_object.pluginname}->prefs_changed: done."


def journal_entry(
    cmdr: str,
    is_beta: bool,
    system: str,
    station: str,
    entry: Dict[str, Any],
    state: Dict[str, Any],
) -> Optional[str]:
    """Get new entry in the game's journal.

    cmdr:       Current commander name
    is_beta:    Is the game currently in beta
    system:     Current system, if known
    station:    Current station, if any
    entry:      The journal event
    state:      More info about the commander, their ship, and their cargo
    """
    checker_object.logger.debug = (
        f"{checker_object.pluginname}->journal_entry: start..."
    )
    # new
    if entry["event"] == "FSDTarget":
        checker_object.jumpsystem.name = entry.get(
            "Name", checker_object.jumpsystem.name
        )
        checker_object.jumpsystem.address = entry.get(
            "SystemAddress", checker_object.jumpsystem.address
        )
        checker_object.jumpsystem.star_class = entry.get(
            "StarClass", checker_object.jumpsystem.star_class
        )
        checker_object.update()
    if entry["event"] == "FSDJump":
        starsystem: str = entry.get("StarSystem", "")
        if checker_object.jumpsystem.name == starsystem:
            checker_object.status.set("Waiting for data...")
    checker_object.logger.debug = f"{checker_object.pluginname}->journal_entry: done."


# #[EOF]#######################################################################
