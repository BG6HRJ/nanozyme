from .html_view import bp as html_view_bp
from .nano_enzy_data import bp as nano_enzy_data_bp
from .prediction import bp as prediction_bp
from .user import bp as user_bp


def init_bps(app):
    # 在admin_bp下注册子蓝图
    app.register_blueprint(nano_enzy_data_bp)
    app.register_blueprint(html_view_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(user_bp)
