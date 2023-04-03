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
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from table_line import model

sys.path.append('.')


if __name__ == '__main__':
    filepath = './models/table-line.h5'  # 模型权重存放位置
    fine_tuned_filepath = './models/table-line-fine-tuned.h5'  # 微调后模型权重存放位置

    if os.path.exists(filepath):
        model.load_weights(filepath)
        print("从预训练模型加载权重：", filepath)
    else:
        print("没有找到预训练模型. Training from scratch.")

    checkpointer = ModelCheckpoint(filepath=fine_tuned_filepath, monitor='loss', verbose=0, save_weights_only=True,
                                   save_best_only=True)
    rlu = ReduceLROnPlateau(monitor='loss', factor=0.1,
                            patience=5, verbose=0, mode='auto', cooldown=0, min_lr=0)
    # 降低了学习率，从原来的0.0001降为0.00001
    model.compile(optimizer=Adam(lr=0.00001),
                  loss='binary_crossentropy', metrics=['acc'])

    # table line dataset label with labelme
    paths = glob('./train/dataset-line/*/*.json')
    trainP, testP = train_test_split(paths, test_size=0.1)
    print('total:', len(paths), 'train:', len(trainP), 'test:', len(testP))
    batchsize = 4
    trainloader = gen(trainP, batchsize=batchsize, linetype=1)
    testloader = gen(testP, batchsize=batchsize, linetype=1)
    # epochs原为30，现在调成10
    model.fit_generator(trainloader,
                        steps_per_epoch=max(1, len(trainP) // batchsize),
                        callbacks=[checkpointer],
                        validation_data=testloader,
                        validation_steps=max(1, len(testP) // batchsize),
                        epochs=30)  # 原为30
