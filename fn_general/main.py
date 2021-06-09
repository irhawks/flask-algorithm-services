from flask import Blueprint, jsonify

## https://stackoverflow.com/questions/51991365/expose-python-class-functions-as-rest-services

handler_blueprint = Blueprint(
        '通用函数调用工具',
        __name__,
        url_prefix='/call'
)

import json

from flask import request

from flask import Flask
app = Flask(__name__)

## ============================================================================
# sample functions

# 有时候也可以使用GET来解决问题
def hello_world():
    return "Hello world!"


# curl -H 'Content-Type: application/json' -XPOST http://localhost:5000/call/hello_name -d'{"name": "Tom"}'
def hello_name(params: dict):
    name = params["name"]
    return "Hello " + name

## ============================================================================

## Python的函数有无参数，固定位置参数还有关键字参数三类，大概也需要使用*args, **kwargs两种方式
## 传递参数的时候需要注意一下（这样是一个通用的传参工具）
## 生产级别时，注意类型安全
## 生产级别时，注意错误检查

## 在Java里面也可以做到类似的东西，通过反射调用类的函数并传递参数，见<https://blog.csdn.net/Cy_LightBule/article/details/88956013>。
## <https://o-u-u.com/?p=441>

## 使用jionlp测试一下，比如jio.extract_money函数
import jionlp as jio
## curl -H 'Content-Type: application/json' -XPOST http://localhost:5000/call/jio.extract_money -d'{"text": "张三赔偿李四人民币车费601,293.11元，工厂费一万二千三百四十五元,利息9佰日元，打印费十块钱"}'
## 有这样的关键字的话，<https://github.com/dongrixinyu/JioNLP/wiki/%E6%AD%A3%E5%88%99%E6%8A%BD%E5%8F%96%E4%B8%8E%E8%A7%A3%E6%9E%90-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3>里面的函数就都可以抽取和解析了。


@handler_blueprint.route('/<fn_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def call_function(fn_name: str):

    """
    以后在用的时候注意类型安全之类的信息
    """
    function_to_call = eval(fn_name)

    
    body = request.json

    ## 使用jsonify封装返回值
    return jsonify(function_to_call(**body))
