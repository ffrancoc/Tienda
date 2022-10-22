# window.py
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

import datetime
from gi.repository import Adw
from gi.repository import Gtk
from .database import *
from .home import TiendaHomeView
from .user import TiendaUserView

@Gtk.Template(resource_path='/com/github/ffrancoc/Tienda/gtk/window.ui')
class TiendaWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TiendaWindow'

    # Widgets de la interfaz
    # GUI widgets
    btn_home          = Gtk.Template.Child()
    btn_users         = Gtk.Template.Child()
    lbl_currentuser   = Gtk.Template.Child()
    stack_view        = Gtk.Template.Child()


    # Función para mostrar la vista home
    # Function to show home view
    def on_show_home_view(self, button, n_press, x, y):
        self.stack_view.set_visible_child_name('home-view')
        # Eliminar los estilos css del botón
        # Delete css styles from button
        self.btn_home.get_style_context().add_class('sidebar-button-selected')
        self.btn_users.get_style_context().remove_class('sidebar-button-selected')


    # Función para mostrar la vista usuario
    # Function to show user view
    def on_show_user_view(self, button, n_press, x, y):
        self.stack_view.set_visible_child_name('user-view')
        self.user_view.init()
        # Eliminar los estilos css del botón
        # Delete css styles from button
        self.btn_users.get_style_context().add_class('sidebar-button-selected')
        self.btn_home.get_style_context().remove_class('sidebar-button-selected')


    # Sobreescribir el evento para cerrar la ventana
    # Override close window event
    def do_close_request(self):
        app = self.get_application()
        app.show_login_window()
        return False


    def __init__(self, application:Gtk.Application, user:User):
        super().__init__(application=application)

        # Agregar controlladores a los botones
        # Add button's controller
        home_controller = Gtk.GestureClick()
        home_controller.connect('pressed', self.on_show_home_view)
        self.btn_home.add_controller(home_controller)

        user_controller = Gtk.GestureClick()
        user_controller.connect('pressed', self.on_show_user_view)
        self.btn_users.add_controller(user_controller)

        # Mostrar nombre de usuario logueado
        # Show username of user logged in
        self.lbl_currentuser.set_label(user.username)

        # Actualizar fecha y hora de ultima sesion
        # Update last session datetime
        user.last_session = datetime.datetime.now()
        session.commit()

        # Creando las vistas
        # Creating the views
        self.home_view = TiendaHomeView()
        self.user_view = TiendaUserView()

        # Agregando las vistas al contenedor
        # Adding the views to container
        self.stack_view.add_named(self.home_view, 'home-view')
        self.btn_home.get_style_context().add_class('sidebar-button-selected')
        self.stack_view.add_named(self.user_view, 'user-view')
            
