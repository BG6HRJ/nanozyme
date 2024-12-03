import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_databases(app: Flask):
    db.init_app(app)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        with app.app_context():
            try:
                db.engine.connect()
            except Exception as e:
                exit(f"数据库连接失败: {e}")
