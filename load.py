# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: plugin entry point.
"""


import logging
import tkinter as tk
from typing import Any, Dict, Optional, Tuple

from checker.jsktoolbox.tktool.widgets import CreateToolTip

from config import config

from checker.jsktoolbox.edmctool.logs import LogLevels
from checker.jsktoolbox.edmctool.ed_keys import EDKeys
from checker.checker import Checker

checker_object = Checker()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    checker_object.logger.debug = (
        f"{checker_object.plugin_name}->plugin_start3 start..."
    )
    # loglevel set from config
    loglevel: Optional[int] = LogLevels().get(config.get_str("loglevel"))
    checker_object.log_processor.loglevel = (
        loglevel if loglevel is not None else logging.DEBUG
    )
    checker_object.logger.debug = f"{checker_object.plugin_name}->plugin_start3 done."
    return f"{checker_object.plugin_name}"


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    checker_object.logger.debug = f"{checker_object.plugin_name}->plugin_stop: start..."
    checker_object.shutting_down = True
    checker_object.logger.debug = (
        f"{checker_object.plugin_name}->plugin_stop: shut down flag is set"
    )
    # something to do
    # shut down logger at last
    checker_object.logger.debug = (
        f"{checker_object.plugin_name}->plugin_stop: terminating the logger"
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
    checker_object.logger.debug = f"{checker_object.plugin_name}->plugin_app: start..."
    # add button to main frame
    label = tk.Label(
        parent,
        text=f"Jump target:",
    )
    CreateToolTip(
        label,
        [
            f"{checker_object.plugin_name} v{checker_object.version}",
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
        f"{checker_object.plugin_name}->prefs_changed: start..."
    )
    # set loglevel after config update
    loglevel: Optional[int] = LogLevels().get(config.get_str("loglevel"))
    checker_object.log_processor.loglevel = (
        loglevel if loglevel is not None else logging.DEBUG
    )
    checker_object.logger.debug = f"{checker_object.plugin_name}->prefs_changed: done."


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
        f"{checker_object.plugin_name}->journal_entry: start..."
    )
    # new
    if entry[EDKeys.EVENT] == EDKeys.FSD_TARGET:
        checker_object.jump_system.name = entry.get(
            EDKeys.NAME, checker_object.jump_system.name
        )
        checker_object.jump_system.address = entry.get(
            EDKeys.SYSTEM_ADDRESS, checker_object.jump_system.address
        )
        checker_object.jump_system.star_class = entry.get(
            EDKeys.STAR_CLASS, checker_object.jump_system.star_class
        )
        checker_object.dialog_update()
    elif entry[EDKeys.EVENT] == EDKeys.CARRIER_JUMP_REQUEST:
        checker_object.jump_system.name = entry.get(
            EDKeys.SYSTEM_NAME, checker_object.jump_system.name
        )
        checker_object.jump_system.address = entry.get(
            EDKeys.SYSTEM_ADDRESS, checker_object.jump_system.address
        )
        checker_object.jump_system.star_class = entry.get(
            EDKeys.STAR_CLASS, checker_object.jump_system.star_class
        )
        checker_object.dialog_update()
    if entry[EDKeys.EVENT] in (EDKeys.FSD_JUMP, EDKeys.CARRIER_JUMP):
        star_system: str = entry.get(EDKeys.STAR_SYSTEM, "")
        if checker_object.jump_system.name == star_system:
            checker_object.status.set("Waiting for data...")
    checker_object.logger.debug = f"{checker_object.plugin_name}->journal_entry: done."


# #[EOF]#######################################################################
