import os
import pathlib
from tabulate import tabulate

import argparse
parser = argparse.ArgumentParser()

# "--info" 指定でインポートした画像をprintで出力
parser.add_argument("--importInfo", help="optional", action="store_true")
args = parser.parse_args()

print("\n")
print("START fileFinder.py")
print("\n*************************\n")

object_path ="./trimmed"

files = os.listdir( object_path )
files_dir = [f for f in files if os.path.isdir(os.path.join( object_path , f))]
labels = files_dir
print("labels:", labels)

maxFileNum = 0
maxLabelNum = len(labels)

# ラベルフォルダからの画像取得
for w in labels:
    img_path = object_path + "/" + w
    img_list = list(pathlib.Path( img_path ).glob('**/*.png'))
    if maxFileNum < len(img_list):
        maxFileNum = len(img_list)

# ラベルの総数、ラベルフォルダ内の画像のうち、最大数を取得
print( "maxFileNum:"+ str(maxFileNum) )
print( "maxLabelNum:" + str(maxLabelNum) )

img_array = [[0 for i in range( maxFileNum )] for j in range( maxLabelNum )] #配列[ラベル数][最大ファイル数]を宣言

for j in range( maxLabelNum ):
    # for i in range( maxFileNum ):
    img_array_path = object_path + "/" + labels[j]
    img_array[j] = list(pathlib.Path( img_array_path ).glob('**/*.png'))

print( "Images imported." )

if args.importInfo:
    print( tabulate( img_array ) )

print("\n*************************\n")
print("END fileFinder.py")

# print(img_array[3][1]) #img_array チェック用