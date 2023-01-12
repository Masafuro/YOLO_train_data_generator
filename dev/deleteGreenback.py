# -*- coding: utf-8 -*-

import pathlib
import cv2
import numpy as np
import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--hl")
parser.add_argument("--sl")
parser.add_argument("--vl")
parser.add_argument("--hh")
parser.add_argument("--sh")
parser.add_argument("--vh")

args = parser.parse_args()

 # mask = cv2.inRange(hsv, (40, 50,50), (86, 255, 255)) #H180 S255 V255 H78~160 Default60:50:50-86:255:255        ksize=15
      
if args.hl:
    hl = int(args.hl)
else:
    hl = 40
if args.sl:
    sl = int(args.sl)
else:
    sl = 30
if args.vl:
    vl = int(args.vl)
else:
    vl = 30

if args.hh:
    hh = int(args.hh)
else:
    hh = 90
if args.sh:
    sh = int(args.sh)
else:
    sh = 255
if args.vh:
    vh = int(args.vh)
else:
    vh = 255

print("hl:",hl,"_sl:",sl,"_vl:",vl)
print("hh:",hh,"_sh:",sh,"_vh:",vh)


#入力画像ディレクトリ
input_dir_base = "object"
output_dir_base = "trimmed"
category = "."

files = os.listdir(input_dir_base)
files_dir = [f for f in files if os.path.isdir(os.path.join(input_dir_base, f))]
print(files_dir)

for j in range(len(files_dir)):
    category = files_dir[j]
    print("category:",category)
    input_dir = input_dir_base + "\\" + category
    input_list = list(pathlib.Path(input_dir).glob('**/*.jpg'))
    output_dir = output_dir_base + "\\" + category

    # 出力フォルダにラベルごとのフォルダが存在していなければ作成
    if not os.path.isdir(output_dir):
            print("INFO:出力フォルダに",category,"のフォルダを作成します。")
            os.mkdir(output_dir)
    else:
        print("INFO:出力フォルダには",category,"フォルダがすでに存在しています。")
    
    for i in range(len(input_list)):
        img_file_name = str(input_list[i])
        print( "IMPORT:",img_file_name )

        ## グリーンバック除去&png出力
        img = cv2.imread( img_file_name , -1)
        imgA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
      #  mask = cv2.inRange(hsv, (40, 50,50), (86, 255, 255)) #H180 S255 V255 H78~160 Default60:50:50-86:255:255        ksize=15
        mask = cv2.inRange(hsv, (hl, sl,vl), (hh, sh, vh)) #H180 S255 V255 H78~160 Default60:50:50-86:255:255        ksize=15
        ksize = 15
        mask = cv2.medianBlur(mask,ksize)
        img2 = cv2.bitwise_not(imgA, imgA, mask=mask)
        
        file_name = os.path.splitext(os.path.basename(img_file_name))[0]
        output_file_name = output_dir + "\\" + category + str(i).zfill(8) + ".png"
        cv2.imwrite( output_file_name ,img2)
        
        # 画像を読み込む
        image = Image.open( output_file_name )
        # 不要な透明画素を除去
        cropped_image = image.crop(image.getbbox())
        # 画像を保存
        cropped_image.save(output_file_name)

        print("EXPORT:",output_file_name)

