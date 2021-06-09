from flask import Blueprint, jsonify

# cocoNLP

handler_blueprint = Blueprint(
        'cocoNLP中文信息抽取工具',
        __name__,
        url_prefix='/coconlp'
)

import cocoNLP

import json

from flask import request

from flask import Flask
app = Flask(__name__)

## ============================================================================

from cocoNLP.extractor import extractor
ex = extractor()

@handler_blueprint.route('/coconlp/extractor/email', methods=['GET', 'POST'])
def extract_email(lang):

    if request.method == 'GET':
        text = request.args.get("text")
    else:
        text = request.json["text"]

    return jsonify( ex.extract_email(text) )

@handler_blueprint.route('/coconlp/extractor/phone', methods=['GET', 'POST'])
def extract_phone(lang):

    if request.method == 'GET':
        text = request.args.get("text")
    else:
        text = request.json["text"]

    return jsonify( ex.extract_cellphone(text, nation='CHN') )

# 抽取身份证号
@handler_blueprint.route('/coconlp/extractor/identity', methods=['GET', 'POST'])
def extract_phone(lang):

    if request.method == 'GET':
        text = request.args.get("text")
    else:
        text = request.json["text"]

    return jsonify( ex.extract_ids(text) )

# 抽取手机归属地以及运营商
@handler_blueprint.route('/coconlp/extractor/phone_location', methods=['GET', 'POST'])
def extract_phone_location(lang):

    if request.method == 'GET':
        text = request.args.get("text")
    else:
        text = request.json["text"]

    cellphones = ex.extract_cellphone(text, nation='CHN')

    return jsonify( [ex.extract_cellphone_locaion(cell, 'CHN')
        for cell in cellphones
        ])

# 抽取地址信息
@handler_blueprint.route('/coconlp/extractor/location', methods=['GET', 'POST'])
def extract_location(lang):

    if request.method == 'GET':
        text = request.args.get("text")
    else:
        text = request.json["text"]

    return jsonify(ex.extract_location(text))

# 抽取时间
@handler_blueprint.route('/coconlp/extractor/time', methods=['POST'])
def extract_time(lang):
    text = request.json["text"]
    return jsonify(ex.extract_times(text))

# 抽取人名
@handler_blueprint.route('/coconlp/extractor/name', methods=['POST'])
def extract_time(lang):
    text = request.json["text"]
    return jsonify(ex.extract_name(text))


## ============================================================================
# 语言检测组件

import langid

@handler_blueprint.route('/langid/classify', methods=['POST'])
def detect_by_langid():
    text = request.json["text"]
    return jsonify(langid.classify(text))

import langdetect
from langdetect import detect
from langdetect import detect_langs

@handler_blueprint.route('/langdetect/classify', methods=['POST'])
def detect_by_langdetect():
    text = request.json["text"]
    return jsonify(detect_langs(text))
