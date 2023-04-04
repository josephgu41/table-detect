#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from table_detect import table_detect
from table_line import table_line
from table_build import tableBuid,to_excel
from utils import minAreaRectbox, measure, eval_angle, draw_lines
from chineseocr_lite.test import ChineseOcr


class table:
    def __init__(self, img, tableSize=(416, 416), tableLineSize=(1024, 1024), isTableDetect=False, isToExcel=False):
        self.img = img
        self.tableSize = tableSize
        self.tableLineSize = tableLineSize
        self.isTableDetect = isTableDetect
        self.isToExcel = isToExcel
        self.img_degree()
        self.table_boxes_detect()  ##表格定位
        self.table_ceil()  ##表格单元格定位
        
        self.ocr = self.table_ocr()  # yby_edit

        self.table_build()

    def img_degree(self):
        img, degree = eval_angle(self.img, angleRange=[-15, 15])
        self.img = img
        self.degree = degree

    def table_boxes_detect(self):
        h, w = self.img.shape[:2]

        if self.isTableDetect:
            boxes, adBoxes, scores = table_detect(self.img, sc=self.tableSize, thresh=0.2, NMSthresh=0.3)
            if len(boxes) == 0:
                boxes = [[0, 0, w, h]]
                adBoxes = [[0, 0, w, h]]
                scores = [0]
        else:
            boxes = [[0, 0, w, h]]
            adBoxes = [[0, 0, w, h]]
            scores = [0]

        self.boxes = boxes
        self.adBoxes = adBoxes
        self.scores = scores

    def table_ceil(self):
        ###表格单元格
        n = len(self.adBoxes)
        self.tableCeilBoxes = []
        self.childImgs = []
        for i in range(n):
            xmin, ymin, xmax, ymax = [int(x) for x in self.adBoxes[i]]

            childImg = self.img[ymin:ymax, xmin:xmax]
            rowboxes, colboxes = table_line(childImg[..., ::-1], size=self.tableLineSize, hprob=0.5, vprob=0.5)
            tmp = np.zeros(self.img.shape[:2], dtype='uint8')
            tmp = draw_lines(tmp, rowboxes + colboxes, color=255, lineW=2)
            labels = measure.label(tmp < 255, connectivity=2)  # 8连通区域标记
            regions = measure.regionprops(labels)
            ceilboxes = minAreaRectbox(regions, False, tmp.shape[1], tmp.shape[0], True, True)
            ceilboxes = np.array(ceilboxes)
            ceilboxes[:, [0, 2, 4, 6]] += xmin
            ceilboxes[:, [1, 3, 5, 7]] += ymin
            self.tableCeilBoxes.extend(ceilboxes)
            self.childImgs.append(childImg)

    def table_build(self):
        tablebuild = tableBuid(self.tableCeilBoxes)
        cor = tablebuild.cor
        for i, line in enumerate(cor):
            # line['text'] = 'table-test'##ocr
            line['text'] = self.ocr[i]
        if self.isToExcel:
            workbook = to_excel(cor, workbook=None)
        else:
            workbook=None
        self.res = cor
        self.workbook = workbook


    def table_ocr(self):
        """use ocr and match ceil"""
        res = []
        tablebuild = tableBuid(self.tableCeilBoxes)
        for box in tablebuild.diagBoxes:

            # 获取表格的左上角和右下角坐标
            x1, y1, x2, y2 = box[0],box[1],box[2],box[3]
            # 截取表格部分的图片
            table_img = self.img[y1:y2, x1:x2]

            cv2.imwrite('./img_temp/cropped.png', table_img)
            img = "./img_temp/cropped.png"
        
            x = ChineseOcr(img)
        
            if x:
                txt = ""
                for i in range(len(x)):
                    txt = txt + " " + x[i]["text"]
                res.append(txt[1:])
            else:
                res.append(" ")
                
        # print(res)
        return res


if __name__ == '__main__':
    import argparse
    import os
    import time
    from utils import draw_boxes

    parser = argparse.ArgumentParser(description='tabel to excel demo')
    parser.add_argument('--isTableDetect', default=False, type=bool, help="是否先进行表格检测")
    parser.add_argument('--tableSize', default='416,416', type=str, help="表格检测输入size")
    parser.add_argument('--tableLineSize', default='1024,1024', type=str, help="表格直线输入size")
    parser.add_argument('--isToExcel', default=False, type=bool, help="是否输出到excel")
    parser.add_argument('--folderPath', default='img', type=str, help="图像文件夹路径")
    args = parser.parse_args()
    args.tableSize = [int(x) for x in args.tableSize.split(',')]
    args.tableLineSize = [int(x) for x in args.tableLineSize.split(',')]
    print(args)

    # 递归获取图像文件路径
    img_paths = []
    for root, dirs, files in os.walk(args.folderPath):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                img_paths.append(os.path.join(root, file))

    for img_path in img_paths:
        img = cv2.imread(img_path)
        t = time.time()
        tableDetect = table(img,tableSize=args.tableSize,
                            tableLineSize=args.tableLineSize,
                            isTableDetect=args.isTableDetect,
                            isToExcel=args.isToExcel
                            )
        tableCeilBoxes = tableDetect.tableCeilBoxes
        tableJson = tableDetect.res
        workbook =  tableDetect.workbook
        img = tableDetect.img
        tmp = np.zeros_like(img)
        img = draw_boxes(tmp, tableDetect.tableCeilBoxes, color=(255, 255, 255))
        print(time.time() - t)
        pngP = os.path.splitext(img_path)[0]+'ceil.png'
        cv2.imwrite(pngP, img)
        if workbook is not None:
            workbook.save(os.path.splitext(img_path)[0]+'.xls')

