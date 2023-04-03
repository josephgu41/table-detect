#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 9 23:11:51 2020

@author: chineseocr
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from image import gen
from glob import glob
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from table_line import model
import sys

sys.path.append('.')


if __name__ == '__main__':
    filepath = './models/table-line-fine-tuned.h5'  # 模型权重存放位置

    if os.path.exists(filepath):
        model.load_weights(filepath)
        print("从预训练模型加载权重：", filepath)
    else:
        print("没有找到预训练模型. Please provide the pre-trained model.")

    # 降低了学习率，从原来的0.0001降为0.00001
    model.compile(optimizer=Adam(lr=0.00001),
                  loss='binary_crossentropy', metrics=['acc'])

    # table line dataset label with labelme
    paths = glob('./train/dataset-line/*/*.json')
    trainP, testP = train_test_split(paths, test_size=0.1)
    print('total:', len(paths), 'train:', len(trainP), 'test:', len(testP))
    batchsize = 4
    testloader = gen(testP, batchsize=batchsize, linetype=1)

    # 评估模型多次，并计算平均损失和准确率
    n_evaluations = 5  # 设置评估次数
    total_loss = 0
    total_accuracy = 0

    for i in range(n_evaluations):
        loss, accuracy = model.evaluate_generator(testloader, steps=max(1, len(testP) // batchsize))
        print(f"第{i + 1}次模型在测试集上的损失: {loss}, 准确率: {accuracy}")
        total_loss += loss
        total_accuracy += accuracy

    avg_loss = total_loss / n_evaluations
    avg_accuracy = total_accuracy / n_evaluations

    print("模型在测试集上的平均损失：", avg_loss)
    print("模型在测试集上的平均准确率：", avg_accuracy)
