# database.py
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

import os, datetime, hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Engine
from sqlalchemy import Column, Integer, String, DateTime


DB_PATH = f'/home/{os.getlogin()}/.tienda'
DB_URL = f'sqlite:///{DB_PATH}/Tienda.db'


# Validar si la base de datos existe
# Validate if the database exists
def validate_engine()->Engine:
    os.makedirs(DB_PATH, exist_ok=True)
    engine = create_engine(DB_URL,
                connect_args={"check_same_thread": False},
                echo=True,
                future=True
             )
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


# Crear la sesion de la base de datos
# Create database session
engine = validate_engine()
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()
Base = declarative_base()


# Modelos para la base de datos
# Database models
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_session = Column(DateTime, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    status = Column(Integer, nullable=False, default=1)

    def __init__(self, username, password):
        self.username = username
        # Encriptar password con sha256
        # Encrypt password with sha256
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'User({self.username}, {self.password})'
