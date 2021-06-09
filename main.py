from flask import Flask

#from function.basic       import handler_blueprint as basic
#from function.hair_change import handler_blueprint as hair_change
#from fn_hanlp.hanlp       import handler_blueprint as hanlp
#from fn_sklearn.generic   import handler_blueprint as sklearn
#from fn_paddle.main       import handler_blueprint as paddlehub
from fn_general.main       import handler_blueprint as function_call

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#使用 blueprint分模块导入用户写的handler目录文件
#app.register_blueprint(basic, url_prefix="/demo/basic")
#app.register_blueprint(hair_change, url_prefix="/demo/hair")
#app.register_blueprint(hanlp, url_prefix="/hanlp")
#app.register_blueprint(sklearn, url_prefix="/sklearn")
#app.register_blueprint(paddlehub, url_prefix="/paddlehub")
app.register_blueprint(function_call, url_prefix="/call")

if __name__ == '__main__':
    app.run(debug=True)
