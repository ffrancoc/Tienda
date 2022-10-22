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

from gi.repository import Adw
from gi.repository import Gtk
from .database import *

@Gtk.Template(resource_path='/com/github/ffrancoc/Tienda/gtk/user-view.ui')
class TiendaUserView(Gtk.Box):
    __gtype_name__ = 'TiendaUserView'

    # Widgets de la interfaz
    # GUI widgets
    treeview          = Gtk.Template.Child()
    lbl_treeview_info = Gtk.Template.Child()


    # Función para recargar los usuarios
    # Function to reload the users
    @Gtk.Template.Callback()
    def on_reload_treeview(self, button):
        self.treemodel.clear()
        self.init()


    # Función para cargar los usuarios
    # Function to load the users
    def init(self):
        # Si el modelo esta vacio entonces consultar y cargar los usuarios
        # If the model is empty then try get and load the users
        if len(self.treemodel) == 0:
            users = session.query(User).all()
            for user in users:
                last_session = user.last_session.strftime("%Y-%m-%d, %H:%M:%S") if user.last_session else ''
                self.treemodel.append([user.id, user.username, last_session, user.status])
            # Actualizar la etiqueta con el numero de registros
            # Update tag count register
            self.lbl_treeview_info.set_label(_('%d users found' % len(self.treemodel)))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Creación y asignación del modelo
        # Model creation and assignment it
        self.treemodel = Gtk.ListStore(int, str, str, int)
        self.treeview.set_model(self.treemodel)

        # Creación de las columnas para el treeview
        # Creation the columns for the treeview
        for i,title in enumerate(['id', _('username'), _('last session'), _('status')]):
            column = Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=i)
            self.treeview.append_column(column)

        
