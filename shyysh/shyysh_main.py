#!/usr/bin/env python
"""
ShyySH

Entry point
"""

import libtmux

from shyysh.core import logger
from shyysh.util import get_current_pane


def main():
    logger.info("Shyysh starting")
    shell_cmd = "shyysh_manager"
    app_name = "shyysh"

    tmux_server = libtmux.Server()
    pane = get_current_pane(tmux_server)

    if pane:
        logger.info("Tmux pane found")
        session = tmux_server.sessions.get(session_id=pane["session_id"])
        assert session is not None, "Session not found"
        session.new_window(app_name, attach=True, window_shell=shell_cmd)
        session.switch_client()
    else:
        logger.info("Tmux pane not found")
        session = tmux_server.new_session(
            attach=False,
            kill_session=True,
            window_name=app_name,
            window_command=shell_cmd,
        )
        session.attach()


if __name__ == "__main__":
    main()
