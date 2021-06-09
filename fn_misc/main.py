from flask import Blueprint, jsonify

# https://github.com/fighting41love/funNLP

handler_blueprint = Blueprint(
        'NLP词库、工具包、学习资料',
        __name__,
        url_prefix='/hanlp'
)

import hanlp
import json

from flask import request

from flask import Flask
app = Flask(__name__)

## ============================================================================


@handler_blueprint.route('/tokenizer/<lang>', methods=['GET', 'POST'])
def tokenizer(lang):

    if request.method == 'GET':
        sentence = request.args.get("data")
    else:
        sentence = request.json["data"]
    app.logger.warn("Data is %s", sentence)

    if lang == 'en':
        return jsonify(tokenizer_en(sentence))

    if lang == 'zh':
        return jsonify(tokenizer_zh(sentence))

    return 404

