# table-detect

## table detect(yolo) , table line(unet) （表格检测/表格单元格定位）

links(下载链接): http://gofile.me/4Nlqh/fNHlWzVWo  
download models weights  and move to ./modes

### test table detect（表格检测）  

`
python table_detect.py --jpgPath img/table-detect.jpg
`

### test table ceil detect with unet（表格识别输出到excel）

`
python table_ceil.py --isToExcel True --jpgPath img/table-detect.jpg
`


## train table line(训练表格)
### label table with labelme(https://github.com/wkentaro/labelme)
`
python train/train.py
`

# 创建环境

依赖：``cuda 10.1``

```
conda create --name table-ocr python=3.7
conda activate table-ocr
pip install -r requirements.txt
```

# 模块运行

``python3 -m chineseocr_lite.test``