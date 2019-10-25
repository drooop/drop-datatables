from flask import Blueprint

bp = Blueprint('src', __name__, template_folder='../../templates', static_folder='../../static')

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
from app.api import ping, users, tokens
