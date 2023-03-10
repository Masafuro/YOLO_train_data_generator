#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AKAZEによる特徴量検出

"""feature detection."""

import cv2
import os
import csv
import datetime
import math

IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/'
IMG_SIZE = (200, 200)

def calc_sim(baseFile, compareFile):
    target_img_path = IMG_DIR + baseFile
    target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, IMG_SIZE)
    target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])

    comparing_img_path = IMG_DIR + compareFile
    comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
    comparing_img = cv2.resize(comparing_img, IMG_SIZE)
    comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])

    ret = 1/( cv2.compareHist(target_hist, comparing_hist, 0) + 0.000000000000000001 )

    return ret


extensions = ['.jpg', '.jpeg', '.png', '.gif']
files = [file for file in os.listdir(IMG_DIR) if os.path.splitext(file)[1].lower() in extensions]
# files = os.listdir(IMG_DIR)
print(files)

# 現在の日付と時刻を取得する
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d_%H:%M:%S')

header = ["Histdist_" + now_str]
data = []
data_now = []
rMax = 0
rmaxImageA = ""
rmaxImageB = ""


for file0 in files:
    header.append(file0)
    data_now.append(file0)
    for fileN in files:
        try:
            r = calc_sim(file0, fileN)
            print(file0,fileN,r)
            data_now.append(r)
            if r > rMax:
                rMax = r
                rmaxImageA = file0
                rmaxImageB = fileN

        except cv2.error:
            ret = "cv2.error"
    data.append(data_now)
    data_now = []

with open('Histdist.csv', mode='w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for row in data:
        writer.writerow(row)

print('CSV file created!')
print("最大距離", rmaxImageA, "-",rmaxImageB,":",rMax)
