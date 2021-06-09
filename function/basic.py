from flask import Blueprint
handler_blueprint = Blueprint(
        '缺省演示',
        __name__,
        url_prefix='/basic'
)
@handler_blueprint.route("/echo")
def hello():
    return "Hello, World!"
