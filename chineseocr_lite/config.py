import os

filt_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(filt_path) + os.path.sep + ".")

GPU_ID = "cpu" # "cpu"

# psenet相关
pse_long_size = 320  # 图片长边 960
dbnet_short_size = 480 # 960
# det_model_type = "pse_mobilenetv2"
det_model_type = "dbnet"
pse_scale = 1

if det_model_type == "pse_mobilenetv2":
    model_path = os.path.join(father_path, "models/psenet_lite_mbv2.pth")

elif det_model_type == "dbnet":
    # model_path = os.path.join(father_path, "models/dbnet.onnx")
    model_path = os.path.join(father_path, "models/dbnet_optimized.onnx")

# crnn相关
nh = 256
crnn_type = "full_lstm"
# crnn_type = "lite_lstm"  #"full_lstm"

crnn_vertical_model_path = os.path.join(father_path, "models/crnn_dw_lstm_vertical.pth")

if crnn_type == "lite_lstm":
    LSTMFLAG = True
    crnn_model_path = os.path.join(father_path, "models/crnn_lite_lstm_dw_v2.pth")
elif crnn_type == "lite_dense":
    LSTMFLAG = False
    crnn_model_path = os.path.join(father_path, "models/crnn_lite_dense_dw.pth")
elif crnn_type == "full_lstm":
    LSTMFLAG = True
    crnn_model_path = os.path.join(father_path, "models/ocr-lstm.pth")
elif crnn_type == "full_dense":
    LSTMFLAG = False
    crnn_model_path = os.path.join(father_path, "models/ocr-dense.pth")

# crnn_model_path = os.path.join(father_path,"models/ocr-lstm.pth")

# from crnn.keys import  alphabet
from .crnn.keys import alphabetChinese as alphabet

# angle_class相关
lable_map_dict = {0: "hengdao", 1: "hengzhen", 2: "shudao", 3: "shuzhen"}  # hengdao: 文本行横向倒立 其他类似
rotae_map_dict = {"hengdao": 180, "hengzhen": 0, "shudao": 180, "shuzhen": 0}  # 文本行需要旋转的角度
angle_type = "shufflenetv2_05"
# angle_type  = "resnet18"
angle_model_path = os.path.join(father_path, "models/{}.pth".format(angle_type))

TIMEOUT = 30

# dbnet 参数
dbnet_max_size = 6000 #长边最大长度
pad_size = 0 #检测是pad尺寸，有些文档文字充满整个屏幕检测有误，需要pad

max_post_time = 100 # ip 访问最大次数

white_ips = [] #白名单

version = 'api/v1'
