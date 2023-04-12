#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from PIL import Image
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
            # cv2.imwrite('./img_temp/cropped.png', table_img)
            # img = "./img_temp/cropped.png"
            x = ChineseOcr(table_img)

        
            if x:
                txt = ""
                for i in range(len(x)):
                    if x[i]["text"]=="一":
                        txt = txt + " " + "---"
                    else:
                        txt = txt + " " + x[i]["text"]
                res.append(txt[1:])
            else:
                res.append("---")
                
        # print(res)
        return res
    

    
    
# excel转html表格
def to_html(workbook=None, file_path=None):
    """ 
    file_path存在，则代表从文件中读取workbook
    workbook存在，则代表从内存中读取workbook
    """
    import io
    import xlrd
    import xlwt
    from xlutils.copy import copy
    from xlwt.Utils import rowcol_to_cell
    
    
    output = []
    merged_cells = None
    
    # 如果 file_path 存在，则从文件中读取工作簿
    if file_path:
        book = xlrd.open_workbook(file_path)
    # 如果 workbook 存在，则从内存中读取工作簿
    elif workbook:
        # 将 xlwt.Workbook 对象写入内存中的二进制流
        stream = io.BytesIO()
        workbook.save(stream)
        # 使用 xlrd.open_workbook() 函数打开内存中的二进制流并返回一个 xlrd.Book 对象
        stream.seek(0)
        book = xlrd.open_workbook(file_contents=stream.read())
    else:
        return "未提供有效的工作簿信息"

    # 遍历工作簿中的表格
    for sheet in book.sheets():
        output.append('<table>')
        merged_cells = sheet.merged_cells
        for row in range(sheet.nrows):
            output.append('<tr>')
            for col in range(sheet.ncols):
                cell_value = sheet.cell_value(row, col)
                rowspan, colspan = get_merged_cell_range(merged_cells, row, col)
                if rowspan or colspan:
                    output.append(f'<td rowspan="{rowspan+1}" colspan="{colspan+1}">{cell_value}</td>')
                else:
                    output.append(f'<td>{cell_value}</td>')
            output.append('</tr>')
        output.append('</table>')
    return '\n'.join(output)


# 确定单元格是否是合并单元格，并返回其跨度
def get_merged_cell_range(merged_cells, row, col):
    for crange in merged_cells:
        rlo, rhi, clo, chi = crange
        if row == rlo and col == clo:
            return rhi - rlo, chi - clo
    return 0, 0
    
# 前端展示一张图的表格识别
def table_predict(img, short_size=480):
    import os
    import time


    t = time.time()
    tableDetect = table(img,tableSize=[416, 416],
                        tableLineSize=[1024, 1024],
                        isTableDetect=False,
                        isToExcel=True
                        )
    tableCeilBoxes = tableDetect.tableCeilBoxes
    tableJson = tableDetect.res
    workbook = tableDetect.workbook
    img = tableDetect.img
    print(time.time() - t)
    result = ""
    if workbook is not None:
        result = to_html(workbook=workbook)
    return result

# 将html保存为本地文件
def save_html_to_file(html_string, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_string)
        
    
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
    parser.add_argument('--isToHtml', default=False, type=bool, help="是否输出html")
    parser.add_argument('--folderPath', default='img', type=str, help="图像文件夹路径")
    parser.add_argument('--jpgPath', default='',type=str, help="单张图像路径")
    
    args = parser.parse_args()
    args.tableSize = [int(x) for x in args.tableSize.split(',')]
    args.tableLineSize = [int(x) for x in args.tableLineSize.split(',')]
    print(args)

    if args.jpgPath == '':
        # 递归获取图像文件路径
        img_paths = []
        for root, dirs, files in os.walk(args.folderPath):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    img_paths.append(os.path.join(root, file))

        for img_path in img_paths:
            img = cv2.imread(img_path)
            
            # 灰度增强
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            histogram = cv2.calcHist([gray_image],[0],None,[256],[0,256])
            minimum_pixel_value, maximum_pixel_value, _, _ = cv2.minMaxLoc(gray_image)
            for i in range(len(histogram)):
                histogram_value = histogram[i]
                if i < minimum_pixel_value or i > maximum_pixel_value:
                    histogram[i] = 0
                else:
                    histogram[i] = int(255 * (i - minimum_pixel_value) / (maximum_pixel_value - minimum_pixel_value))
            img = cv2.LUT(gray_image, histogram)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img = img.astype(np.uint8)
            
            # # 边缘锐化增强
            # kernel = np.array([[0, -2, 0], [-2, 9, -2], [0, -2, 0]])
            # img = cv2.filter2D(img, -1, kernel)
            
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
            
             # 获取文件名和文件后缀
            filename, extension = os.path.splitext(img_path)
            # 拼接新的文件路径
            new_path = os.path.join(os.path.dirname(os.path.dirname(filename)), 'result', os.path.basename(filename))        
            pngP = new_path+'ceil.png'
            cv2.imwrite(pngP, img)
            if workbook is not None:
                workbook.save(new_path+'.xls')
                if args.isToHtml == True:
                    html_string = to_html(file_path=new_path+'.xls')
                    save_html_to_file(html_string, new_path+'.html')
                
                
    else:
            img = cv2.imread(args.jpgPath)
            
            # 灰度增强
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            histogram = cv2.calcHist([gray_image],[0],None,[256],[0,256])
            minimum_pixel_value, maximum_pixel_value, _, _ = cv2.minMaxLoc(gray_image)
            for i in range(len(histogram)):
                histogram_value = histogram[i]
                if i < minimum_pixel_value or i > maximum_pixel_value:
                    histogram[i] = 0
                else:
                    histogram[i] = int(255 * (i - minimum_pixel_value) / (maximum_pixel_value - minimum_pixel_value))
            img = cv2.LUT(gray_image, histogram)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img = img.astype(np.uint8)
            
            # # 边缘锐化增强
            # kernel = np.array([[0, -2, 0], [-2, 9, -2], [0, -2, 0]])
            # img = cv2.filter2D(img, -1, kernel)
            
            t = time.time()
            tableDetect = table(img,tableSize=args.tableSize,
                                tableLineSize=args.tableLineSize,
                                isTableDetect=args.isTableDetect,
                                isToExcel=args.isToExcel
                                )
            tableCeilBoxes = tableDetect.tableCeilBoxes
            tableJson = tableDetect.res
            workbook = tableDetect.workbook
            img = tableDetect.img
            tmp = np.zeros_like(img)
            img = draw_boxes(tmp, tableDetect.tableCeilBoxes, color=(255, 255, 255))
            print(time.time() - t)
            
            # 获取文件名和文件后缀
            filename, extension = os.path.splitext(args.jpgPath)
            # 拼接新的文件路径
            new_path = os.path.join(os.path.dirname(os.path.dirname(filename)), 'result', os.path.basename(filename))
            print(new_path)         
            pngP = new_path+'ceil.png'
            cv2.imwrite(pngP, img)
            if workbook is not None:
                # workbook.save(os.path.splitext(args.jpgPath)[0]+'.xls')
                workbook.save(new_path+'.xls')
                if args.isToHtml == True:
                    # file_path = os.path.splitext(args.jpgPath)[0]
                    # html_string = to_html(file_path=file_path+'.xls')
                    # save_html_to_file(html_string, file_path+'.html')
                    html_string = to_html(file_path=new_path+'.xls')
                    save_html_to_file(html_string, new_path+'.html')
                    

