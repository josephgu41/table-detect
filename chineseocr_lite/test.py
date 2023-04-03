# -*- coding: utf-8 -*-
"""
@author: lywen
"""
from .config import *
import os
import numpy as np
from PIL import Image
from .model import text_predict
from typing import List

filelock = 'file.lock'
if os.path.exists(filelock):
    os.remove(filelock)

# def ChineseOcr(imgs: List[str]):
#     image_list = []
#     for img in imgs:
#         img = Image.open(img)
#         if img is not None:
#             img = np.array(img)
#         image_list.append(img)

#     results = text_predict(image_list)
#     # print(results)
    
#     final_results = []
#     for result in results:
#         res = [{'text': x['text'],
#                 'name': str(i),
#                 'box': {'cx': x['cx'],
#                         'cy': x['cy'],
#                         'w': x['w'],
#                         'h': x['h'],
#                         'angle': x['degree']
#                         }
#                 } for i, x in enumerate(result)]
#         final_results.append(res)

#     return final_results

def ChineseOcr(img):
    img = Image.open(img)
    if img is not None:
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

# # yby edit
# def ChineseOcr(img):
#     img = Image.fromarray(img)
#     result = text_predict(np.array(img))
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

