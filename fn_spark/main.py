from flask import Blueprint, jsonify, request, Flask


# https://github.com/fighting41love/funNLP

handler_blueprint = Blueprint(
        'NLP词库、工具包、学习资料',
        __name__,
        url_prefix='/hanlp'
)

import json

app = Flask(__name__)

## ============================================================================
## FPGrowth挖掘算法以及算法预处理工作（转换CSV）

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.enabled", "false")
from pyspark.ml.fpm import FPGrowth

def spark_df_to_list(df):
    return json.loads(df.toPandas().to_json(orient="values", force_ascii=False))

import io
import pandas as pd

@handler_blueprint.route('/linkdata/fpgrowth/mining', methods=['POST'])
def fpgrowth():

    data = np.array(request.json['data'])
    df_pd = pd.DataFrame(data, columns=['id', 'item'])
    df = spark.createDataFrame(df_pd)
    df.createOrReplaceTempView("df")
    df_data = spark.sql("""
        SELECT id, ARRAY_DISTINCT(COLLECT_LIST(item)) items FROM df GROUP BY id
    """)
    alg_fpgrowth = FPGrowth().setItemsCol("items")\
            .setMinSupport(0.5)\
            .setMinConfidence(0.6)
    model = alg_fpgrowth.fit(df_data)

    resp = {'rules': spark_df_to_list(model.associationRules),
            'freqs': spark_df_to_list(model.freqItemsets)
           }
    return jsonify(resp)


@handler_blueprint.route("/linkdata/fpgrowth/prepare", methods=['POST'])
def fpgrowth_prepare():
    df = pd.read_csv(io.StringIO(request.data.decode('utf-8')))
    result = io.StringIO()
    df[['ID', 'place']].to_json(result, orient='values', force_ascii=False)

    return jsonify({'data': json.loads(result.getValue())})
