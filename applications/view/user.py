from flask import Blueprint, jsonify, request, session
import json
from applications.extensions import db
from applications.models import User
from applications.schemas import NanoEnzyDataSchema
from flask_login import login_required
from flask_login import login_required, current_user, login_user, logout_user

bp = Blueprint('user', __name__, url_prefix='/user')


# 登录
@bp.post('/login')
def login():
    req = request.form
    username = req.get('username')
    password = req.get('password')

    if not username or not password:
        return "ERROR"

    user = User.query.filter_by(username=username).first()

    if not user:
        return "ERROR"

    if username == user.username and user.password_hash == password:

        # 登录
        login_user(user)
        res = {
            "code": 0,
            "msg": "Login Success",
        }
        return jsonify(res)
    else:
        return "ERROR"


@bp.post('/logout')
@login_required  # 使用@login_required装饰器保护此路由，确保只有登录用户才能访问
def logout():
    logout_user()
    return 'Logged out successfully'


# 注册路由
@bp.post('/register')
def register():
    req = request.form
    username = req.get('username')
    password = req.get('password')

    if not username or not password:
        return "ERROR"

    # 检查用户名是否已经被使用
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "用户名已被占用"

    # 创建一个新用户
    new_user = User(username=username, password_hash=password)

    # 将新用户添加到数据库
    # （确保提交更改以持久保存它们）
    db.session.add(new_user)
    db.session.commit()

    res = {
        "code": 0,
        "msg": "注册成功",
    }
    return jsonify(res)
