#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ヒスとグラムマッチング：切粉ではあまり差がでない？

"""hist matching."""

import cv2
import os

TARGET_FILE = '00001.png'
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '\\images\\'
IMG_SIZE = (640, 640)

target_img_path = IMG_DIR + TARGET_FILE
print(target_img_path)

target_img = cv2.imread(target_img_path)
# target_img = cv2.imread(TARGET_FILE)
target_img = cv2.resize(target_img, IMG_SIZE)
target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])

print('TARGET_FILE: %s' % (TARGET_FILE))

files = os.listdir(IMG_DIR)
print("files",files)
for i, file in enumerate(files):
    if file == '.DS_Store' or file == TARGET_FILE or file == '.gitignore':
        continue
    else:
        ret = ""
        comparing_img_path = IMG_DIR + file
        comparing_img = cv2.imread(comparing_img_path)
        comparing_img = cv2.resize(comparing_img, IMG_SIZE)
        comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])

        ret = cv2.compareHist(target_hist, comparing_hist, 0)
        print(file, ret)