from flask import Blueprint

handler_blueprint = Blueprint(
        'Sklearn机器学习框架接口',
        __name__,
        url_prefix='/sklearn'
)

import sklearn
import joblib
import time
import json


## ============================================================================

from sklearn.cluster import KMeans

@handler_blueprint.route('/kmeans/train', methods=['POST'])
def kmeans_train():
    data = request.form.get('data')
    if 'params' in request.form.keys():
        params = request.form.get('params')
    else:
        params = {}

    model = KMeans(**params)
    result = model.fit(X)
    utc_now = int(time.time())

    target_model_path = '/tmp/model_kmeans_{}.pkl'.format(utc_now)
    joblib.dump(result, target_model_path)
    return target_model_path

@handler_blueprint.route('/kmeans/predict', methods=['POST'])
def kmeans_predict():

    data = request.form.get('data')
    model_path = request.form.get('model_path')
    model = joblib.load(model_path)
    result = model.predict(data)
    
    r = request.form
    r['prediction'] = result.tolist()

    return r ## 结果不保存本地，直接返回给前台服务

## ============================================================================

import numpy as np
from sklearn import linear_model

@handler_blueprint.route('/regression/linear/train', methods=['POST'])
def linear_regression_train():

    data = request.form.get('data')

    if 'params' in request.form.keys():
        params = request.form.get('params')
    else:
        params = {}

    model = linear_model.LinearRegression(**params)
    result = model.fit(data.x, data.y)

    utc_now = int(time.time())

    model_path = '/tmp/linear_regression_{}.pkl'.format(utc_now)
    joblib.dump(result, model_path)

    return model_path

## 预测的接口其实是一样的，特别是在这种模型名称写在参数里面的情况下

@handler_blueprint.route('/regression/linear/predict', methods=['POST'])
def linear_regression_predict():

    data = request.form.get('data')
    model_path = request.form.get('model_path')
    model = joblib.load(model_path)
    result = model.predict(data)
    
    r = request.form
    r['prediction'] = result.tolist()

    return r ## 结果不保存本地，直接返回给前台服务

## ============================================================================

from sklearn.metrics import log_loss
from sklearn.naive_bayes import BernoulliNB

@handler_blueprint.route('/naive_bayes/BernoulliNB/train', methods=['POST'])
def bernoulliNB_train():

    data = request.form.get('data')

    if 'params' in request.form.keys():
        params = request.form.get('params')
    else:
        params = {}

    model = BernoulliNB(**params)
    result = model.fit(data.x, data.y)

    utc_now = int(time.time())

    model_path = '/tmp/bernoulliNB_{}.pkl'.format(utc_now)
    joblib.dump(result, model_path)

    return model_path

## 预测的接口其实是一样的，特别是在这种模型名称写在参数里面的情况下

@handler_blueprint.route('/naive_bayes/BernoulliNB/predict', methods=['POST'])
def bernoulliNB_predict():

    data = request.form.get('data')
    model_path = request.form.get('model_path')
    model = joblib.load(model_path)
    result = model.predict(data)
    
    r = request.form
    r['prediction'] = result.tolist()

    return r ## 结果不保存本地，直接返回给前台服务


## ============================================================================

from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np

@handler_blueprint.route('/cluster/dbscan', methods=['POST'])
def dbscan():

    data = np.array(request.json['data'])

    if 'params' in request.form.keys():
        params = request.json['params']
    else:
        params = {}

    model = DBSCAN(**params)
    result = model.fit(data)

    return jsonify(result.labels_.tolist())


