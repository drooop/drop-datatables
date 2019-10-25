from flask import jsonify, render_template, make_response
from app.src import bp1


@bp1.route('/ping', methods=['GET'])
def ping():
    '''前端Vue.js用来测试与后端Flask API的连通性'''
    return jsonify('Pong!')


@bp1.route('/test', methods=['GET'])
def test():
    return render_template('MDB_try/dashboard.html')


@bp1.route('/js/<filename>', methods=['GET'])
def get_js(filename):
    resp = make_response(open(r'C:\Users\TQ_Designer_01\Documents\codebase\projects\with Vue\dropblog\back-end\templates\MDB_try\js\{}'.format(filename)).read())
    resp.headers["Content-type"] = "text/plain;charset=UTF-8"
    return resp


@bp1.route('/css/<filename>', methods=['GET'])
def get_css(filename):
    resp = make_response(open(r'C:\Users\TQ_Designer_01\Documents\codebase\projects\with Vue\dropblog\back-end\templates\MDB_try\css\{}'.format(filename)).read())
    resp.headers["Content-type"] = "text/css;charset=UTF-8"
    return resp
