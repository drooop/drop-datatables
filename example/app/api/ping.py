import os

from jinja2 import Template
from flask import jsonify, render_template, make_response, send_from_directory, url_for, Response
from app.api import bp

from app.api import tq_ip
import json


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify('Pong!')


@bp.route('/vars', methods=['GET'])
def test():
    vars_url = "http://"+tq_ip+":5000/api/vars"
    download_page_url = "http://"+tq_ip+":5000/api/download_page"
    ipconfig_url = "http://"+tq_ip+":5000/api/ipconfig"

    return render_template('vars_block.html',
                           vars_url=vars_url,
                           download_page_url=download_page_url,
                           ipconfig_url=ipconfig_url)


@bp.route('/download_page', methods=['GET'])
def download():
    vars_url = "http://"+tq_ip+":5000/api/vars"
    download_page_url = "http://"+tq_ip+":5000/api/download_page"
    ipconfig_url = "http://"+tq_ip+":5000/api/ipconfig"
    return render_template('download_block.html',
                           vars_url=vars_url,
                           download_page_url=download_page_url,
                           ipconfig_url=ipconfig_url)


@bp.route('/ipconfig', methods=['GET'])
def ipconfig():
    vars_url = "http://"+tq_ip+":5000/api/vars"
    download_page_url = "http://"+tq_ip+":5000/api/download_page"
    ipconfig_url = "http://"+tq_ip+":5000/api/ipconfig"
    return render_template('ipconfig.html',
                           vars_url=vars_url,
                           download_page_url=download_page_url,
                           ipconfig_url=ipconfig_url)


@bp.route('/wwstudio', methods=['GET'])
def wwstudio():
    return render_template('wwStudio.html')


@bp.route('/get_data/<filename>', methods=['GET'])
def get_data(filename):
    base_dir = os.path.dirname(__file__)
    resp = make_response(
        open(os.path.join(base_dir, f'../../static/ajax/data/{filename}'), 'r', encoding='UTF-8').read())
    resp.headers["Content-type"] = "text/plan;charset=UTF-8"
    return resp


@bp.route('/change/<info>', methods=['GET'])
def change(info):
    index_list = info.split(',')
    with open('static/ajax/data/config', 'r') as f:
        f_list = f.readlines()
    for index in index_list:
        index = int(index)
        info_list = f_list[index].split(',')
        if info_list[2].startswith('true'):
            if not (index == (len(f_list) - 1)):
                f_list[index] = f'{info_list[0]},{info_list[1]},false\n'
            else:
                f_list[index] = f'{info_list[0]},{info_list[1]},false'
        else:
            if not (index == (len(f_list) - 1)):
                f_list[index] = f'{info_list[0]},{info_list[1]},true\n'
            else:
                f_list[index] = f'{info_list[0]},{info_list[1]},true'
    with open('static/ajax/data/config_new', 'w') as f:
        f.writelines(f_list)
    with open('static/ajax/data/config', 'w') as f:
        f.writelines(f_list)
    return str(f_list)


@bp.route('/read_ip', methods=['GET'])
def read_ip():
    with open('static/ajax/data/PLC_IP', 'r') as f:
        rows = f.readlines()
    return rows[0]


@bp.route('/change_ip/<ip>', methods=['GET'])
def change_ip(ip):
    f_list = ip
    with open('static/ajax/data/PLC_IP', 'w') as f:
        f.writelines(f_list)
    return str(f_list)


@bp.route('/reset', methods=['GET'])
def reset(info):
    with open('static/ajax/data/vars', 'r') as f:
        f_list = f.readlines()
    with open('static/ajax/data/config', 'w') as f:
        f.writelines(f_list)
    return json.dumps({"result": "success"})


@bp.route('/dir', methods=['GET'])
def get_file_list():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'downloads')
    dir_l = ['']
    base_dir = file_path
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.yhld':
                # dir_l.append(os.path.join(root, file))
                dir_l.append(file)

    # to csv
    csv_content = ''
    for i in range(len(dir_l)):
        if not (i == len(dir_l) - 1):
            csv_content += f'{i},{dir_l[i].split(".")[0]}\n'
        else:
            csv_content += f'{i},{dir_l[i].split(".")[0]}'
    return csv_content


@bp.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'downloads')
    print(file_path)
    try:
        response = make_response(
            send_from_directory(file_path,
                                filename=filename,
                                as_attachment=True))
        return response
    except Exception as e:
        return jsonify({"code": "error", "message": "{}".format(e)})
