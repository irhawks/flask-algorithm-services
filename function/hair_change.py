from flask import Blueprint,Flask, request,make_response,send_from_directory
import os
import cv2
import keras
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 上传文件夹


handler_blueprint = Blueprint(
	'头发变色',
  	__name__,
  	url_prefix='/hair'
)




def predict(model, im):
    h, w, _ = im.shape
    inputs = cv2.resize(im, (480, 480))
    inputs = inputs.astype('float32')
    inputs.shape = (1,) + inputs.shape
    inputs = inputs / 255
    mask = model.predict(inputs)
    # ret, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY_INV)
    mask.shape = mask.shape[1:]
    mask = cv2.resize(mask, (w, h))
    mask.shape = h, w, 1
    return mask


def change_v(v, mask, target):
    # 染发
    epsilon = 1e-7
    x = v / 255                             # 数学化
    target = target / 255
    target = -np.log(epsilon + 1 - target)
    x_mean = np.sum(-np.log(epsilon + 1 - x)  * mask) / np.sum(mask)
    alpha = target / x_mean
    x = 1 - (1 - x) ** alpha
    v[:] = x * 255                          # 二进制化


def recolor(im, mask, color=(0x40, 0x16, 0x66)):
    # 工程化
    color = np.array(color, dtype='uint8', ndmin=3)
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    color_hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    # 染发
    im_hsv[..., 0] = color_hsv[..., 0]      # 修改颜色
    change_v(im_hsv[..., 2:], mask, color_hsv[..., 2:])
    im_hsv[..., 1] = color_hsv[..., 1]      # 修改饱和度
    x = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)
    im = im * (1 - mask) + x * mask
    return im


@handler_blueprint.route("/predict",methods = ['POST'])
def hair():
    if request.method == 'POST':
        f = request.files['file']
        #保存文件
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'src.jpg'))
        ifn = os.path.join(app.config['UPLOAD_FOLDER'], 'src.jpg')
        src = cv2.imread(ifn)
        model = keras.models.load_model('function/weights.005.h5')
        mask = predict(model, src)
        keras.backend.clear_session()  # 清除session（否则keras报错）
        color =[169, 169, 169]#银色
        res = recolor(src, mask, color)
        ofn = os.path.join(app.config['UPLOAD_FOLDER'], 'res.jpg')
        cv2.imwrite(ofn, res)
        return send_from_directory(app.config['UPLOAD_FOLDER'],"res.jpg",as_attachment=True)
