from flask import Blueprint

bp = Blueprint('api',
               __name__,
               template_folder='../../templates'
               )
with open('static/config.js', 'r') as f:
    res = f.readlines()[0].split('\'')[1]
tq_ip = res
# print(type(tq_ip), tq_ip)
# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
from app.api import ping, users, tokens
