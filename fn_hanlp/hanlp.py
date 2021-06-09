from flask import Blueprint, jsonify

handler_blueprint = Blueprint(
        'HanLP自然语言处理程序接口',
        __name__,
        url_prefix='/hanlp'
)

import hanlp
import json

from flask import request

from flask import Flask
app = Flask(__name__)



tokenizer_zh = hanlp.load('LARGE_ALBERT_BASE')
tokenizer_en = hanlp.utils.rules.tokenize_english
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

#tagger_en = hanlp.load(hanlp.pretrained.pos.PTB_POS_RNN_FASTTEXT_EN)
#tagger_zh = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ALBERT_BASE)
#@handler_blueprint.route('/tagger/<lang>', methods=['GET', 'POST'])
#def tagger(lang):
#
#    if request.method == 'GET':
#        sentence = request.args.get("data")
#    else:
#        sentence = request.form.get("data")
#
#    if lang == 'en':
#        return tagger_en(sentence)
#
#    if lang == 'zh':
#        return tagger_zh(sentence)
#
#    return 404
#
#
#recognizer_en = hanlp.load(hanlp.pretrained.ner.CONLL03_NER_BERT_BASE_UNCASED_EN)
#recognizer_zh = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
#@handler_blueprint.route('/recognizer/<lang>', methods=['GET', 'POST'])
#def tagger(lang):
#
#    if request.method == 'GET':
#        sentence = request.args.get("data")
#    else:
#        sentence = request.form.get("data")
#
#    if lang == 'en':
#        return recognizer_en(sentence)
#
#    if lang == 'zh':
#        return recognizer_zh(sentence)
#
#    return 404
#
#syntatic_parser_en = hanlp.load(hanlp.pretrained.dep.PTB_BIAFFINE_DEP_EN)
#syntatic_parser_zh = hanlp.load(hanlp.pretrained.dep.CTB7_BIAFFINE_DEP_ZH)
#@handler_blueprint.route('/syntatic_parser/<lang>', methods=['GET', 'POST'])
#def syntatic_parser(lang):
#
#    if request.method == 'GET':
#        sentence = request.args.get("data")
#    else:
#        sentence = request.form.get("data")
#
#    if lang == 'en':
#        return syntatic_parser_en(sentence)
#
#    if lang == 'zh':
#        return syntatic_parser_zh(sentence)
#
#    return 404
#
#semantic_parser_en = hanlp.load(hanlp.pretrained.sdp.SEMEVAL15_PAS_BIAFFINE_EN)
#semantic_parser_zh = hanlp.load(hanlp.pretrained.sdp.SEMEVAL16_NEWS_BIAFFINE_ZH)
#@handler_blueprint.route('/semantic_parser/<lang>', methods=['GET', 'POST'])
#def syntatic_parser(lang):
#
#    if request.method == 'GET':
#        sentence = request.args.get("data")
#    else:
#        sentence = request.form.get("data")
#
#    if lang == 'en':
#        return semantic_parser_en(sentence)
#
#    if lang == 'zh':
#        return semantic_parser_zh(sentence)
#
#    return 404
#
#
#pipeline_zh = hanlp.pipeline() \
#    .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
#    .append(tokenizer_zh, output_key='tokens') \
#    .append(tagger_zh, output_key='part_of_speech_tags') \
#    .append(syntactic_parser_zh, input_key=('tokens', 'part_of_speech_tags'), output_key='syntactic_dependencies') \
#    .append(semantic_parser_zh, input_key=('tokens', 'part_of_speech_tags'), output_key='semantic_dependencies')
#pipeline_en = hanlp.pipeline() \
#    .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
#    .append(tokenizer_en, output_key='tokens') \
#    .append(tagger_en, output_key='part_of_speech_tags') \
#    .append(syntactic_parser_en, input_key=('tokens', 'part_of_speech_tags'), output_key='syntactic_dependencies') \
#    .append(semantic_parser_en, input_key=('tokens', 'part_of_speech_tags'), output_key='semantic_dependencies')
#@handler_blueprint.route('/pipeline/<lang>', methods=['GET', 'POST'])
#def syntatic_parser(lang):
#
#    if request.method == 'GET':
#        sentence = request.args.get("data")
#    else:
#        sentence = request.form.get("data")
#
#    if lang == 'en':
#        return pipeline_en(sentence)
#
#    if lang == 'zh':
#        return pipeline_zh(sentence)
#
#    return 404
