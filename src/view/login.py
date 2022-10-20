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

import os, hashlib, threading
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from .dialogs import TiendaDialog
from .database import *

@Gtk.Template(resource_path='/com/github/ffrancoc/Tienda/gtk/login.ui')
class TiendaLogin(Adw.ApplicationWindow):
    __gtype_name__ = 'TiendaLogin'

    # Widgets de la interfaz
    # GUI widgets
    status_page    = Gtk.Template.Child()
    entry_username = Gtk.Template.Child()
    entry_password = Gtk.Template.Child()
    btn_login      = Gtk.Template.Child()


    @Gtk.Template.Callback()
    def on_login(self, button):
        username = self.entry_username.get_text()
        password = self.entry_password.get_text()

        # Validar usuario y mostrar la ventana principal
        # Validate user and show the main window
        if len(username) > 0 and len(password) > 0:
            try:
                user = session.query(User).filter(User.username==username, User.password==hashlib.sha256(password.encode('utf-8')).hexdigest()).one_or_none()
                if user:
                    app = self.get_application()
                    app.show_main_window(user)
                else:
                    TiendaDialog.show_information(
                        window=self.get_root(),
                        heading='',
                        body=_('Invalid username or password')
                    ).present()
            except Exception as ex:
                TiendaDialog.show_information(
                        window=self.get_root(),
                        heading='',
                        body=_('Fatal error, could not execute the operation')
                    ).present()


    # Funcion para actualizar la interfaz
    # Function to update GUI
    def _on_idle(self, data):
        self.btn_login.set_sensitive(True)
        if data:
            TiendaDialog.show_information(
                window=self.get_root(),
                heading='',
                body=_('The initial user has been created with the following data:\nusername: %s\npassword: %s' % (data.username, data.username))
            ).present()
        return GLib.SOURCE_REMOVE


    # Funcion a executar en el hilo
    # Function to execute in thread
    def _thread_function(self):
        Base.metadata.create_all(engine)

        users = session.query(User).count()
        user = None
        if users == 0:
            self.btn_login.set_sensitive(False)
            os_user = os.getlogin()
            user = User(username=os_user, password=os_user)
            session.add(user)
            session.commit()

        GLib.idle_add(self._on_idle, user)


    # Crear un nuevo hilo
    # Create a new thread
    def start_database(self):
        thread = threading.Thread(target=self._thread_function)
        thread.daemon=True
        thread.start()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_database()


