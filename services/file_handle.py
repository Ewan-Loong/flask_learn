#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/11/28 11:13
# @Author  : Ewan
# @File    : file_handle.py
# @Description : 文件数据操作

import os
import json
from flask import Blueprint, request, send_from_directory, current_app
from werkzeug.utils import secure_filename
import pandas as pd
from app import app
from core.api_check import check_files, required_token, check_params
from core.utils import generate_unique_filename

bp = Blueprint('file_handle', __name__, url_prefix='/FileHandle')


@bp.route('/upload_file', methods=['POST'])
# @required_token
@check_files
def upload_file():
    UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER')
    try:
        file = request.files['file']
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return {'data': {"fileId": filename, "originalName": secure_filename(file.filename), }, "msg": "文件上传成功"}, 200
    except Exception as e:
        return {"msg": "文件上传失败" + str(e)}, 500


@bp.route('/parse_file', methods=['POST'])
@required_token
@check_params('fileId')
def parse_file():
    """文件解析API"""
    data = request.json
    file_id = data['fileId']
    UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER')
    file_path = os.path.join(UPLOAD_FOLDER, file_id)

    if not os.path.exists(file_path):
        return {"msg": "文件不存在"}, 404

    try:
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')

        if ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path, engine='openpyxl')
            result = {
                "data": df.to_dict(orient="records"),
                "metadata": {
                    "row_count": len(df),
                    "column_count": len(df.columns),
                    "file_type": "excel"
                }
            }
        elif ext == 'csv':
            df = pd.read_csv(file_path)
            result = {
                "data": df.to_dict(orient="records"),
                "metadata": {
                    "row_count": len(df),
                    "column_count": len(df.columns),
                    "file_type": "csv"
                }
            }
        elif ext == 'txt':
            df = pd.read_csv(file_path, sep='\t')
            result = {
                "data": df.to_dict(orient="records"),
                "metadata": {
                    "row_count": len(df),
                    "column_count": len(df.columns),
                    "file_type": "txt"
                }
            }
        elif ext == 'json':
            with open(file_path, 'r') as f:
                json_data = json.load(f)

            if isinstance(json_data, dict):
                result = {
                    "data": [json_data],
                    "metadata": {
                        "row_count": 1,
                        "column_count": len(json_data),
                        "file_type": "json"
                    }
                }
            elif isinstance(json_data, list):
                result = {
                    "data": json_data,
                    "metadata": {
                        "row_count": len(json_data),
                        "column_count": len(json_data[0]) if json_data else 0,
                        "file_type": "json"
                    }
                }
            else:
                raise ValueError("JSON格式不支持")
        else:
            raise ValueError(f"不支持的文件类型: {ext}")

        return {"data": result, "msg": "文件解析成功"}, 200

    except Exception as e:
        app.logger.error(f"文件解析失败: {str(e)}")
        return {"msg": str(e)}, 400


@bp.route('/download/<filename>')
def download_file(filename):
    """提供已上传文件的下载接口 - 优化安全"""
    UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER')
    safe_filename = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, safe_filename, as_attachment=True)
