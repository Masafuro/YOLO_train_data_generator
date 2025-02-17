import cv2
import glob
import argparse
import numpy as np

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
print("file_names:",*file_names)
sample_id = np.random.choice(len(file_names), size=1,replace=False)
print("sample_id:",str(sample_id))

im_id = file_names[ sample_id[0] ].split("/")[-1].split(".")[0].lstrip("images\\")
print("im_id",im_id)
im = cv2.imread("./output/images/%s.jpg" % (im_id))
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

# アノテーション画像を出力する？？
#result = cv2.imwrite(image_path, im)
result = cv2.imwrite( output_path + "/" + im_id +".jpg", im)

print(result)
# ウインドウ出力
# cv2.imshow("window", im)
# cv2.waitKey()
