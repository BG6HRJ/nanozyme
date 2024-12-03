from flask import Flask
from .init_login import init_login_manager
from .init_migrate import init_migrate
from .init_sqlalchemy import db, init_databases


def init_plugs(app: Flask) -> None:
    init_login_manager(app)
    init_databases(app)
    init_migrate(app)
