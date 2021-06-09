from flask import Blueprint, jsonify

handler_blueprint = Blueprint(
        'PaddleHub各类预训练模型',
        __name__,
        url_prefix='/paddlehub'
)

import json

from flask import request

from flask import Flask
app = Flask(__name__)

import paddlehub as hub ## pip install paddlehub==1.7.1

## ============================================================================
## https://aistudio.baidu.com/aistudio/projectdetail/215711
@handler_blueprint.route('/lac', methods=['POST'])
def lac(lang):
    module = hub.Module(name="lac")

    sentence = request.json["texts"] ## texts是句子的列表，每个代表一句

    return jsonify(module.lexical_analysis(texts=texts))

## ============================================================================
## https://aistudio.baidu.com/aistudio/projectdetail/215814
@handler_blueprint.route('/senta/<string:module_name>', methods=['POST'])
def senta(module_name):

    # available modules: senta_bow, senta_cnn, senta_gru, senta_lstm, senta_bilstm
    senta = hub.Module(name="senta_" + module_name)

    sentence = request.json["texts"] ## texts是句子的列表，每个代表一句

    return jsonify(senta.sentiment_classify(data={"text": texts}))
