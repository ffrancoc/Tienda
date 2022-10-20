# login.py
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

from gi.repository import Adw
from gi.repository import Gtk
from .dialogs import TiendaDialog

@Gtk.Template(resource_path='/com/github/ffrancoc/Tienda/gtk/login.ui')
class TiendaLogin(Adw.ApplicationWindow):
    __gtype_name__ = 'TiendaLogin'

    status_page    = Gtk.Template.Child()
    entry_username = Gtk.Template.Child()
    entry_password = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_login(self, button):
        username = self.entry_username.get_text()
        password = self.entry_password.get_text()

        # Validar usuario y mostrar la ventana principal
        # Validate user and show the main window
        if len(username) > 0 and len(password) > 0:
            if (username == 'admin' and password == 'admin'):
                app = self.get_application()
                app.show_main_window()
            else:
                dialog = TiendaDialog.show_information(
                    window=self.get_root(),
                    heading='',
                    body=_('Invalid username or password')
                )
                dialog.present()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
