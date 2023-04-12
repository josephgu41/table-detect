from .config import *
import os
import numpy as np
from PIL import Image
from .model import text_predict
from typing import List

filelock = 'file.lock'
if os.path.exists(filelock):
    os.remove(filelock)

# def ChineseOcr(img):
#     img = Image.open(img)
#     if img is not None:
#         img = np.array(img)
#     result = text_predict(img)
#     print(result)
#     res = [{'text': x['text'],
#             'name': str(i),
#             'box': {'cx': x['cx'],
#                     'cy': x['cy'],
#                     'w': x['w'],
#                     'h': x['h'],
#                     'angle': x['degree']

#                     }
#             } for i, x in enumerate(result)]

#     return res

def ChineseOcr(img):
    
    img = Image.fromarray(img)
    img = np.array(img)
    result = text_predict(img)
    print(result)
    res = [{'text': x['text'],
            'name': str(i),
            'box': {'cx': x['cx'],
                    'cy': x['cy'],
                    'w': x['w'],
                    'h': x['h'],
                    'angle': x['degree']
                    }
            } for i, x in enumerate(result)]
    return res