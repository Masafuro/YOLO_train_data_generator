# -*- coding: utf-8 -*-

import pathlib
import cv2
import numpy as np
import os
from PIL import Image

#入力画像ディレクトリ
input_dir = "object"
output_dir = "trimmed"
category = "chip"
input_list = list(pathlib.Path(input_dir).glob('**/*.jpg'))


files = os.listdir(input_dir)
files_dir = [f for f in files if os.path.isdir(os.path.join(input_dir, f))]
print(files_dir)



for i in range(len(input_list)):
	img_file_name = str(input_list[i])
	print( img_file_name )
#	img_file = input_dir + "\\" + img_file_name
#	print( img_file )

	## グリーンバック除去&png出力
	img = cv2.imread( img_file_name , -1)
	imgA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, (60, 50,50), (86, 255, 255))
	ksize=15
	mask = cv2.medianBlur(mask,ksize)
	img2 = cv2.bitwise_not(imgA, imgA, mask=mask)
	
	file_name = os.path.splitext(os.path.basename(img_file_name))[0]
	# output_file_name = output_dir + "\\" + file_name + ".png"
	output_file_name = output_dir + "\\" + category + str(i).zfill(8) + ".png"
	cv2.imwrite( output_file_name ,img2)
	
	# 画像を読み込む
	image = Image.open( output_file_name )
	# 不要な透明画素を除去
	cropped_image = image.crop(image.getbbox())
	# 画像を保存
	cropped_image.save(output_file_name)


	## cv2.imwrite('overlay.png',img2)
#    img_np = np.fromfile(img_file_name, dtype=np.uint8)
#    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
#    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	print("-------------------------------------------")
	print(output_file_name)

