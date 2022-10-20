# main.py
#
# Copyright 2022 Francisco Curin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .login import TiendaLogin
from .window import TiendaWindow
from .database import User

class TiendaApplication(Adw.Application):

    def __remove_current_window(self):
        win = self.props.active_window
        self.remove_window(win)
        win.destroy()

    def show_login_window(self):
        self.__remove_current_window()
        win = TiendaLogin(application=self)
        win.present()

    def show_main_window(self, user:User):
        self.__remove_current_window()
        win = TiendaWindow(application=self, user=user)
        win.present()

    def __init__(self):
        super().__init__(application_id='com.github.ffrancoc.Tienda',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = TiendaLogin(application=self)

            # Agregar estilos css
            # Add css styles
            css_provider = Gtk.CssProvider()
            css_provider.load_from_resource("/com/github/ffrancoc/Tienda/css/style.css")
            style_context = win.get_style_context()
            style_context.add_provider_for_display(win.get_display(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='tienda',
                                application_icon='com.github.ffrancoc.Tienda',
                                developer_name='Francisco Curin',
                                version='0.1.0',
                                developers=['Francisco Curin'],
                                copyright='© 2022 Francisco Curin')
        about.present()

    def on_preferences_action(self, widget, _):
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = TiendaApplication()
    return app.run(sys.argv)
