from flask import Blueprint, jsonify

handler_blueprint = Blueprint(
        'HMMlearn隐马模型推断与训练接口',
        __name__,
        url_prefix='/hmmlearn'
)

import joblib
import time, json

## https://hmmlearn.readthedocs.io/en/latest/tutorial.html#training-hmm-parameters-and-inferring-the-hidden-states

"""
通过这个例子能够总结生成模型的主要接口：训练，预测，样本评分，样本生成。
尤其是后面两个，样本评分用于评估一个样本能够从这个生成模型生成的概率，样本生成用于评估用这个生成模型生成测试样本的一个接口。在这里就是生成观察序列

官网https://hmmlearn.readthedocs.io/en/latest/auto_examples/plot_hmm_sampling.html#sphx-glr-auto-examples-plot-hmm-sampling-py里面还带了一个可视化的接口，用于对二维数据状态下不同状态之间的转换进行一次评估的过程。
"""

## ============================================================================
from hmmlearn import hmm
import numpy as np
# np.random.seed(100)

@handler_blueprint.route('/gaussian/train', methods=['POST'])
def gaussian_train():
    sequences = request.form.get('data')
    lengths   = [len(seq) for seq in sequences]

    if 'params' in request.form.keys():
        params = request.form.get('params')
    else:
        params = {}
    model = hmm.GaussianHMM(**params)

    seqs = np.concatenate(sequences).reshape(-1,1)
    result = model.fit(seqs, lengths)

    utc_now = int(time.time())
    target_model_path = '/tmp/model_hmm_gaussian_{}.pkl'.format(utc_now)
    joblib.dump(result, target_model_path)
    return jsonify({
        'name': target_model_path,
        'start_prob': model.startprob_.tolist(),
        'trans_mat' : model.transmat_.tolist(),
        'means'     : model.means_.tolist(),
        'score'     : model.score(seqs) ## 评价训练质量
        })

# 根据模型评价生成的观测序列的得分
@handler_blueprint.route('/guassian/score', methods=['POST'])
def guassian_score():

    sequences = request.form.get('data')
    lengths   = [len(seq) for seq in sequences]
    model  = joblib.load(request.json['name'])
    scores = model.score(sequences, lengths)

    return jsonify({
        'scores' : scores
        })

# 根据模型和观测序列预测隐藏状态
@handler_blueprint.route('/gaussian/predict', methods=['POST'])
def guassian_predict():

    data   = np.array(request.json['data']).reshape(-1,1)
    model  = joblib.load(request.json['name'])

    result = model.predict(data)

    return jsonify({
        'result': result.tolist()
        'score' : model.score(data)
        })


# 根据模型生成观测序列
@handler_blueprint.route('/gaussian/generate', methods=['POST'])
def guassian_generate():

    params = request.json['params']
    model  = joblib.load(request.json['name'])

    samples_x, samples_z = model.sample(params)

    return jsonify({
        "obs"   : samples_x.tolist(),
        'hidden': samples_z.tolist(),
        'score'  : model.score(samples_x)
        }) ## 结果不保存本地，直接返回给前台服务

## ============================================================================

