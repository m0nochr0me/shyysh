#!/usr/bin/env python
"""
ShyySH

TUI
"""

import sys
import os
from asciimatics.widgets import Frame, ListBox, Layout, Divider, \
    Text, Button, TextBox, Widget, CheckBox, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen, ManagedScreen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import libtmux
from libtmux.exc import LibTmuxException

from shyysh.core import config, logger
from shyysh.util import get_current_pane, make_shell_cmd
from shyysh.models import ConnectionItem


class ListView(Frame):
    def __init__(self, screen, model):
        super().__init__(screen, screen.height, screen.width, on_load=self._reload_list,
                         hover_focus=True, can_scroll=False, title='Connections')
        # DB
        self._model: ConnectionItem = model

        # Tmux
        self._tmux_server = libtmux.Server()
        self._pane = get_current_pane(self._tmux_server)
        if not self._pane:
            logger.critical('Please start using shyysh_main.py')
            raise Exception('Tmux not found')
        self._session = self._tmux_server.find_where({'session_id': self._pane['session_id']})

        # Widgets
        self.set_theme(config['tui']['theme'])

        self._list_view = ListBox(
            height=Widget.FILL_FRAME,
            options=self._model.summary(),
            name='connections',
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._connect)

        self._edit_button = Button('[E]dit', self._edit)
        self._copy_button = Button('C[o]py', self._copy)
        self._delete_button = Button('[D]elete', self._delete)
        self._connect_button = Button('[C]onnect', self._connect)
        self._info_panel = Text('', readonly=True)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout.add_widget(self._info_panel)
        layout.add_widget(Divider())

        layout2 = Layout([1, 1, 1, 1, 2, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button('[A]dd', self._add), 0)
        layout2.add_widget(self._copy_button, 1)
        layout2.add_widget(self._edit_button, 2)
        layout2.add_widget(self._delete_button, 3)
        layout2.add_widget(self._connect_button, 4)
        layout2.add_widget(Button('[Q]uit ', self._quit_confirmation), 5)

        self.fix()
        self._on_pick()

    def _connect(self):
        self.save()
        _conn_id = self.data['connections']
        if not _conn_id:
            return
        self._model.cursor = _conn_id
        _conn = self._model.get_current(as_dict=True)
        _conn_cmd = make_shell_cmd(_conn)
        logger.debug(f'Connecting to {_conn_id} -- "{_conn_cmd}"')
        self._session.new_window(f'{_conn["title"]}', attach=True,
                                 window_shell=_conn_cmd)

    def _on_pick(self):
        _value = self._list_view.value
        self._edit_button.disabled = _value is None
        self._copy_button.disabled = _value is None
        self._delete_button.disabled = _value is None
        self._connect_button.disabled = _value is None
        if _value:
            _conn = self._model.get(_value, as_dict=True)
            _conn_cmd = make_shell_cmd(_conn)
            self._info_panel.value = _conn_cmd
        else:
            self._info_panel.value = ' '

    def _reload_list(self, new_value=None):
        self._model.reorder()
        self._list_view.options = self._model.summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.cursor = None
        raise NextScene('Edit Connection')

    def _edit(self):
        self.save()
        _conn_id = self.data['connections']
        if not _conn_id:
            return
        logger.debug(f'Connection {_conn_id} -- Edit')
        self._model.cursor = _conn_id
        raise NextScene('Edit Connection')

    def _copy(self):
        self.save()
        _conn_id = self.data['connections']
        if not _conn_id:
            return
        logger.debug(f'Connection {_conn_id} -- Copy')
        _conn = self._model.get(doc_id=_conn_id, as_dict=True)
        _conn['title'] += ' #copy'
        self._model.add(_conn)
        self._reload_list()

    def _delete(self):
        self.save()
        _conn_id = self.data['connections']
        if not _conn_id:
            return
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        'Delete connection?',
                        ['Yes', 'No'],
                        has_shadow=True,
                        on_close=self._delete_confirm))

    def _delete_confirm(self, value):
        if value != 0:
            return
        _conn_id = self.data['connections']
        if not _conn_id:
            return
        logger.debug(f'Connection {_conn_id} -- Delete')
        self._model.delete_single(_conn_id)
        self._reload_list()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q')]:
                self._quit_confirmation()
            elif event.key_code in [Screen.ctrl("c")]:
                self._immediate_quit()
            elif event.key_code in [ord('e'), ord('E')]:
                self._edit()
            elif event.key_code in [ord('a'), ord('A')]:
                self._add()
            elif event.key_code in [ord('d'), ord('D')]:
                self._delete()
            elif event.key_code in [ord('c'), ord('C')]:
                self._connect()
            elif event.key_code in [ord('o'), ord('O')]:
                self._copy()

        return super().process_event(event)

    def _quit_confirmation(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        'Confirm quit?',
                        ['Yes', 'No'],
                        has_shadow=True,
                        on_close=self._quit))

    @staticmethod
    def _quit(value):
        if value == 0:
            raise StopApplication('Confirmed quit')

    @staticmethod
    def _immediate_quit():
        raise StopApplication('Immediate quit')


class ConnectionView(Frame):
    def __init__(self, screen, model):
        super().__init__(screen,
                         screen.height * 5 // 6,
                         screen.width * 7 // 8,
                         hover_focus=True,
                         can_scroll=False,
                         title='Connection Details',
                         reduce_cpu=True)

        self.set_theme(config['tui']['theme'])

        self._model = model

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text('Title:', 'title', validator=r'^(\S*)$'))
        layout.add_widget(Text('User:', 'user', validator=r'^([A-Za-z0-9].*)$|^$'))
        layout.add_widget(Text('Host:', 'host', validator=r'^(\S*)$'))
        layout.add_widget(Text('Port:', 'port', validator=r'^(6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$|^$'))
        layout.add_widget(Divider(height=2))
        layout.add_widget(CheckBox('-C', 'Compression', 'compression'))
        layout.add_widget(CheckBox('-X', 'Forward X', 'fwd_x'))
        layout.add_widget(CheckBox('-A', 'Forward Agent', 'fwd_a'))
        layout.add_widget(CheckBox('-g', 'Allow Remote Port Conn', 'allow_rpc'))
        layout.add_widget(CheckBox('-N', 'No exec', 'no_exec'))
        layout.add_widget(Divider(height=2))
        layout.add_widget(Text('Custom options:', 'custom_opt'))
        layout.add_widget(Text('Prepend command:', 'prepend_cmd'))
        layout.add_widget(Divider(height=2))
        layout.add_widget(Text('Sort order:', 'sort', validator=r'^(\d){0,4}$|^$'))

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button('OK', self._ok), 0)
        layout2.add_widget(Button('Cancel', self._cancel), 3)
        self.fix()

    def reset(self):
        super(ConnectionView, self).reset()
        self.data = self._model.get_current()

    def _ok(self):
        self.save()
        self._model.update_current(self.data)
        self._model.reorder()
        raise NextScene('Main')

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [Screen.KEY_ESCAPE]:
                self._cancel()

        return super().process_event(event)

    @staticmethod
    def _cancel():
        raise NextScene('Main')


class ShyySH:
    def __init__(self):
        logger.info('Shyysh manager init')
        self._connections = ConnectionItem()
        self._last_scene = None

    def play(self, screen, scene):
        scenes = [Scene([ListView(screen, self._connections)], -1, name='Main'),
                  Scene([ConnectionView(screen, self._connections)], -1, name='Edit Connection')]
        screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

    @ManagedScreen
    def run(self, screen=None):
        while True:
            try:
                screen.wrapper(self.play, catch_interrupt=True, arguments=[self._last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                self._last_scene = e.scene


def main():
    app = ShyySH()
    app.run()


if __name__ == '__main__':
    main()
