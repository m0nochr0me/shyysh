"""
ShyySH

Utility functions
"""

from __future__ import annotations
import os
import libtmux
from shyysh.core import config


def get_current_pane(srv: libtmux.server.Server) -> dict | None:
    """Returns current tmux pane if any"""
    if os.getenv("TMUX_PANE") is not None:
        try:
            return [
                p
                for p in [pane.__dict__ for pane in srv.panes]
                if p.get("pane_id") == os.getenv("TMUX_PANE")
            ][0]
        except IndexError:
            ...


def make_shell_cmd(conn: dict) -> str:
    """Generate ssh connection command"""
    _ssh = [
        f'{conn["prepend_cmd"]} ' if conn["prepend_cmd"] else "",
        f'{config["ssh"]["cmd"]} ',
        f' -p {conn["port"]} ' if conn["port"] else "",
        f" -C " if conn["compression"] else "",
        f" -X " if conn["fwd_x"] else "",
        f" -A " if conn["fwd_a"] else "",
        f" -g " if conn["allow_rpc"] else "",
        f" -N " if conn["no_exec"] else "",
        f' {conn["custom_opt"] }' if conn["custom_opt"] else "",
        " ",
        f'{conn["user"]}@' if conn["user"] else "",
        f'{conn["host"]} ',
        f'{conn["append_cmd"]} ' if conn["append_cmd"] else "",
    ]

    _r = "".join(_ssh)
    return " ".join(_r.split())  # to remove duplicate spaces
