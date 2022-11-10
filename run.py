"""
ShyySH

Entry point
"""

import libtmux

from util import get_current_pane
from confmaker import config


def main():
    _shell_cmd = 'python manager.py'
    _app_name = 'shyysh'

    _tmux_server = libtmux.Server()
    _pane = get_current_pane(_tmux_server)

    if _pane:
        _session = _tmux_server.find_where({'session_id': _pane['session_id']})
        _session.new_window(_app_name, attach=True, window_shell=_shell_cmd)
        _session.switch_client()
    else:
        _session = _tmux_server.new_session(attach=False, kill_session=True,
                                            window_name=_app_name, window_command=_shell_cmd)
        _session.attach_session()


if __name__ == '__main__':
    main()