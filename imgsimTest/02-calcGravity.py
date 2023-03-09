#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# AKAZEによる特徴量検出

"""feature detection."""

import cv2
import os
import csv
import datetime
import math

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/selected/'
SOURCE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/imgsource/'
IMG_SIZE = (200, 200)

def calc_sim(baseFile, compareFile):
    target_img_path = baseFile
    target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, IMG_SIZE)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # detector = cv2.ORB_create()
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)
    
    comparing_img_path = compareFile
    comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
    comparing_img = cv2.resize(comparing_img, IMG_SIZE)
    (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
    matches = bf.match(target_des, comparing_des)
    dist = [m.distance for m in matches]
    ret = sum(dist) / len(dist)
    return ret


extensions = ['.jpg', '.jpeg', '.png', '.gif']
basefiles = [file for file in os.listdir(BASE_DIR) if os.path.splitext(file)[1].lower() in extensions]
sourcefiles = [file for file in os.listdir(SOURCE_DIR) if os.path.splitext(file)[1].lower() in extensions]
# files = os.listdir(IMG_DIR)
print("既存画像",basefiles)
print("追加画像",sourcefiles)

# 現在の日付と時刻を取得する
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d_%H:%M:%S')

header = ["VirtualGravity_" + now_str]
data = []
data_temp = []
minGrav = 999999
minGravImage = ""
canonGrav = 0

for file0 in sourcefiles:
    header.append(file0)
    data_temp.append(file0)
    gravity = 0
    minDist = 0.0001

    for fileN in basefiles:
        try:
            r = calc_sim(BASE_DIR + fileN, SOURCE_DIR + file0)
            gravity = gravity + 1/(r**2 + minDist)

        except cv2.error:
            ret = "cv2.error"

    canonGrav = math.sqrt( gravity/ len(basefiles) )
    data_temp.append(canonGrav)
    print(file0,":",canonGrav)
    if minGrav > canonGrav:
        minGrav = canonGrav
        minGravImage = file0

    data.append(data_temp)
    data_temp = []

with open('gravity.csv', mode='w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for row in data:
        writer.writerow(row)

print('CSV file created!')
print("最小重力画像", minGravImage,":",minGrav)
