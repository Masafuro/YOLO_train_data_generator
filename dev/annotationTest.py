import cv2
import glob
import argparse
import numpy as np
import os
import random

random.seed(0)
print("******START annotationTest.py*****")

parser = argparse.ArgumentParser()
parser.add_argument("--sample")
parser.add_argument("--all", help="optional", action="store_true")
args = parser.parse_args()

# サンプリング数を取得　デフォルトは10
if args.sample:
    # --loop オプションから引数をゲット
    sample = int(args.sample)
else:
    sample = 10

output_path = "./annotated"

file_names = glob.glob("./output/images/*")
# print("file_names:",*file_names)
randomFileNames = random.sample(file_names, sample)

i = 0
imgNum = 0
for i in range(len(randomFileNames)):

    im_id = randomFileNames[i].split("/")[-1].split(".")[0].lstrip("images\\")
    print("im_id",im_id)
    im = cv2.imread("./output/images/%s.jpg" % (im_id))

    if im is None:
        print("Skip by no image.")
    else:
        i = i + 1
        (im_h, im_w) = im.shape[:2] # imがNoneTypeの時がある。


        in_file = open("./output/labels/%s.txt" % (im_id))
        (label, x, y, w, h) = in_file.readline().split()
        x = float(x) * im_w
        y = float(y) * im_h
        w = float(w) * im_w
        h = float(h) * im_h

        half_w = w / 2
        half_h = h / 2
        cv2.rectangle(im, (int(x-half_w), int(y-half_h)), (int(x+half_w), int(y+half_h)), (255, 0, 0), 5)

        # アノテーション画像を出力する
        #result = cv2.imwrite(image_path, im)
        export_path = output_path + "/" + im_id +".jpg"
        is_file = os.path.isfile(export_path)
        if is_file:
            print("The file exsist.")
            i = i - 1
        else:
            result = cv2.imwrite( export_path , im)
            imgNum = imgNum + 1
            print("New Image Generated.")

        


print("imgNum:",str(imgNum))
print("******END annotationTest.py*****")
# ウインドウ出力
# cv2.imshow("window", im)
# cv2.waitKey()
