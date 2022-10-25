# user.py
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

import threading
from gi.repository import Adw
from gi.repository import Gtk, GLib
from .database import *

@Gtk.Template(resource_path='/com/github/ffrancoc/Tienda/gtk/user-view.ui')
class TiendaUserView(Gtk.Box):
    __gtype_name__ = 'TiendaUserView'

    # Widgets de la interfaz
    # GUI widgets
    treeview          = Gtk.Template.Child()
    spinn_progress    = Gtk.Template.Child()
    lbl_treeview_info = Gtk.Template.Child()


    # Función para recargar los usuarios
    # Function to reload the users
    @Gtk.Template.Callback()
    def on_reload_treeview(self, button):
        self.treeview.set_model(None)
        self.init()


    # Funcion para actualizar la interfaz
    # Function to update GUI
    def _on_idle(self, treemodel):
        self.treeview.set_model(treemodel)

        # Actualizar la etiqueta con el numero de registros
        # Update tag count register
        self.lbl_treeview_info.set_label(_('%d users found' % len(treemodel)))
        self.is_loading = False
        self.spinn_progress.set_spinning(False)
        return GLib.SOURCE_REMOVE


    # Funcion a executar en el hilo
    # Function to execute in thread
    def _thread_function(self):
        treemodel = Gtk.ListStore(int, str, str, int)
        users = session.query(User).all()
        for user in users:
            last_session = user.last_session.strftime("%Y-%m-%d, %H:%M:%S") if user.last_session else ''
            treemodel.append([user.id, user.username, last_session, user.status])

        GLib.idle_add(self._on_idle, treemodel)


    # Crear un nuevo hilo
    # Create a new thread
    def load_async(self):
        thread = threading.Thread(target=self._thread_function)
        thread.daemon=True
        thread.start()
        self.is_loading = True
        self.spinn_progress.set_spinning(True)


    # Función para cargar los usuarios
    # Function to load the users
    def init(self):
        if not self.is_loading and not self.treeview.get_model():
            self.load_async()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_loading = False

        # Creación de las columnas para el treeview
        # Creation the columns for the treeview
        for i,title in enumerate(['id', _('username'), _('last session'), _('status')]):
            column = Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=i)
            self.treeview.append_column(column)

        
