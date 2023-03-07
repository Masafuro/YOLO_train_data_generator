#OpenCVとosをインポート
import cv2
import os
import sys


 
TARGET_FILE = "00001.png"
TARGET_DIR = "images/"
# ファイルが存在するかどうかを調べる
if os.path.isfile(TARGET_DIR + TARGET_FILE):
    print("TARGETファイルが存在します。")
else:
    print("TARGETファイルが存在しません。")
    # プログラムを終了する
    sys.exit()


# IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + 'images/'
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/' + TARGET_DIR
print(IMG_DIR)
print(TARGET_FILE)
IMG_SIZE = (640, 640)

target_img_path = IMG_DIR + TARGET_FILE
#ターゲット画像をグレースケールで読み出し
target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
#ターゲット画像をIMG_SIZEに変換
target_img = cv2.resize(target_img, IMG_SIZE)

# BFMatcherオブジェクトの生成
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# AKAZEを適用、特徴点を検出
detector = cv2.AKAZE_create()
(target_kp, target_des) = detector.detectAndCompute(target_img, None)

print('TARGET_FILE: %s' % (TARGET_FILE))

files = os.listdir(IMG_DIR)
for file in files:
    if file == '.DS_Store' or file == ".gitignore" or file == TARGET_FILE:
        continue
    #比較対象の写真の特徴点を検出
    comparing_img_path = IMG_DIR + file
    try:
        comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
        comparing_img = cv2.resize(comparing_img, IMG_SIZE)
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        # BFMatcherで総当たりマッチングを行う
        matches = bf.match(target_des, comparing_des)
        #特徴量の距離を出し、平均を取る
        dist = [m.distance for m in matches]
        ret = sum(dist) / len(dist)
    except cv2.error:
        # cv2がエラーを吐いた場合の処理
        ret = 100000

    # print(file, ret)
    # float型の数値を文字列に変換し、小数点を「-」に変換する
    # ret_str = "{:.4f}".format(ret).replace(".", "-")
    # print(file, ret_str)  # 出力結果： 3-1415
    print(file, ret)  # 出力結果： 3-1415
    # ファイル名の変更
    '''
    path, ext = os.path.splitext(comparing_img_path)  # 拡張子を取得する
    # new_comparing_img_path = "{}{}{}".format(path, "-" + ret_str, ext)
    new_comparing_img_path = "{}{}{}".format(path, "-" + ret_str, ext)
    os.rename(comparing_img_path, new_comparing_img_path)
    '''
    
    # 新しいファイル名でファイルを保存する
    '''
    filename = os.path.basename(file)
    ext = os.path.splitext(filename)[1][1:]
    print(ext)
    os.rename("images/" + filename, "images/" + ret_str + "." + ext )
    '''
