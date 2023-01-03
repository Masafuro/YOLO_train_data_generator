# -*- coding: utf-8 -*-

import pathlib
import cv2
import numpy as np
import os


#入力画像ディレクトリ
input_dir = "gb"
output_dir = "export"
input_list = list(pathlib.Path(input_dir).glob('**/*.jpg'))

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
	output_file_name = output_dir + "\\" + file_name + ".png"
	cv2.imwrite( output_file_name ,img2)
	
	## cv2.imwrite('overlay.png',img2)
#    img_np = np.fromfile(img_file_name, dtype=np.uint8)
#    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
#    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	print("-------------------------------------------")
	print(output_file_name)






