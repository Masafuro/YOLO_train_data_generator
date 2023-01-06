import cv2
import os
import glob
import numpy as np
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--loop")
args = parser.parse_args()
skip_pad = False

# src_imageの背景画像に対して、overlay_imageのalpha画像を貼り付ける。pos_xとpos_yは貼り付け時の左上の座標
def overlay(src_image, overlay_image, pos_x, pos_y):
    print("def overlay.")
    if skip_pad == False:
        # オーバレイ画像のサイズを取得
        ol_height, ol_width = overlay_image.shape[:2]

        # OpenCVの画像データをPILに変換
        # BGRAからRGBAへ変換
        src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
        overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)

        #　PILに変換
        src_image_PIL=Image.fromarray(src_image_RGBA)
        overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

        # 合成のため、RGBAモードに変更
        src_image_PIL = src_image_PIL.convert('RGBA')
        overlay_image_PIL = overlay_image_PIL.convert('RGBA')

        # 同じ大きさの透過キャンパスを用意
        tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
        # 用意したキャンパスに上書き
        tmp.paste(overlay_image_PIL, (pos_x, pos_y), overlay_image_PIL)
        # オリジナルとキャンパスを合成して保存
        result = Image.alpha_composite(src_image_PIL, tmp)

        return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGRA)
    else:
        return None

# 画像周辺のパディングを削除
def delete_pad(image): 
    orig_h, orig_w = image.shape[:2]
    mask = np.argwhere(image[:, :, 3] > 128) # alphaチャンネルの条件、!= 0 や == 255に調整できる
    # print(len(mask[:, 0]),len(mask[:, 1]))
    if len(mask[:, 0]) or len(mask[:, 1]):
        (min_y, min_x) = (max(min(mask[:, 0])-1, 0), max(min(mask[:, 1])-1, 0))
        (max_y, max_x) = (min(max(mask[:, 0])+1, orig_h), min(max(mask[:, 1])+1, orig_w))
    else:
        (min_y, min_x) = (1, 1)
        (max_y, max_x) = (2, 2)
        global skip_pad
        skip_pad = True
    return image[min_y:max_y, min_x:max_x]

# 画像を指定した角度だけ回転させる
def rotate_image(image, angle):
    orig_h, orig_w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((orig_h/2, orig_w/2), angle, 1)
    return cv2.warpAffine(image, matrix, (orig_h, orig_w))

# 画像をスケーリングする
def scale_image(image, scale):
    orig_h, orig_w = image.shape[:2]
    return cv2.resize(image, (int(orig_w*scale), int(orig_h*scale)))

# 背景画像から、指定したhとwの大きさの領域をランダムで切り抜く
def random_sampling(image, h, w): 
    orig_h, orig_w = image.shape[:2]
    y = np.random.randint(orig_h-h+1)
    x = np.random.randint(orig_w-w+1)
    return image[y:y+h, x:x+w]

# 画像をランダムに回転、スケールしてから返す
def random_rotate_scale_image(image):
    image = rotate_image(image, np.random.randint(360))
    image = scale_image(image, 1 + np.random.rand() * 2) # 1 ~ 3倍
    return delete_pad(image)

# overlay_imageを、src_imageのランダムな場所に合成して、そこのground_truthを返す。
def random_overlay_image(src_image, overlay_image,w,h):
    src_h, src_w = src_image.shape[:2]
    overlay_h, overlay_w = overlay_image.shape[:2]
    # print("sw,sh:",src_w,src_h,":w,h:",w,h,":ow,oh:",overlay_w,overlay_h)
    rh = src_h-overlay_h+1
    rw = src_w-overlay_w+1
    oh = overlay_h
    ow = overlay_w
    if rh > 0 and rw > 0 and h > rh and w > rw:
        y = np.random.randint( rh )
        x = np.random.randint( rw )
        bbox = ((x, y), (x+overlay_w, y+overlay_h))
    else:
        x = 0
        y = 0
        bbox = ((0, 0), (1, 1))
        global skip_pad
        skip_pad = True
    print("x,y,oh,ow,rh,rw:",x,y,oh,ow,rh,rw)
    return overlay(src_image, overlay_image, x, y), bbox

# 4点座標のbboxをyoloフォーマットに変換
def yolo_format_bbox(image, bbox):
    orig_h, orig_w = image.shape[:2]
    center_x = (bbox[1][0] + bbox[0][0]) / 2 / orig_w
    center_y = (bbox[1][1] + bbox[0][1]) / 2 / orig_h
    w = (bbox[1][0] - bbox[0][0]) / orig_w
    h = (bbox[1][1] - bbox[0][1]) / orig_h
    return(center_x, center_y, w, h)

def fileFinder():
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
    return img_array, labels, maxFileNum

    # print(img_array[3][1]) #img_array チェック用

output_path = "./output"
input_path = "trimmed"
background_path = "background"

print("output_path:" + output_path + ":EXIST:" + str(os.path.exists(output_path)) )
# input_path = "orig_images"
input_glob = input_path + "/*"
# fruit_files = glob.glob( input_glob )
fruit_files = glob.glob( input_glob )
print("fruit_files:", fruit_files)
# ここで画像をとりそこねている。


'''
fruits = []
labels = []
for fruit_file in fruit_files:
#    labels.append(fruit_file.split("/")[-1].split(".")[0].lstrip(input_path + "\\"))
    labels.append(fruit_file.split("/")[-1].split(".")[0].replace( input_path +"\\",'',1))
    # ここで画像を取り込んでいる。
    fruits.append(cv2.imread(fruit_file, cv2.IMREAD_UNCHANGED))
'''

fruits, labels, maxFileNum = fileFinder()
print("labels:")
print(labels)

# imgData = [[0 for i in range( maxFileNum )] for j in range( len(labels) )] #配列[ラベル数][最大ファイル数]を宣言
imgData = [[0 for i in range( maxFileNum )] for j in range( len(labels) )]

for j in range( len(labels) ):
    for i in range( len(fruits[j]) ):
        print( j,",",i, end=":")
        print(fruits[j][i])
        imgData[j][i] = cv2.imread(str(fruits[j][i]), cv2.IMREAD_UNCHANGED)

'''
for fruit_file in fruit_files:
#    labels.append(fruit_file.split("/")[-1].split(".")[0].lstrip(input_path + "\\"))
    labels.append(fruit_file.split("/")[-1].split(".")[0].replace( input_path +"\\",'',1))
    # ここで画像を取り込んでいる。
    fruits.append(cv2.imread(fruit_file, cv2.IMREAD_UNCHANGED))
'''


background_image = cv2.imread(background_path + "/background.jpg")
height, width, channels = background_image.shape[:3]
print("height:", height,":width:",width,":channels:",channels)
# write label file
with open("label.txt", "w") as f:
    for label in labels:
        f.write("%s\n" % (label))

background_height, background_width = (height, width)

if args.loop:
    # --loop オプションから引数をゲット
    loop = int(args.loop)
else:
    loop = 10


# train用の画像生成
for k in range(loop):
    for j in range( len(labels) ):
        for i in range( len(fruits[j]) ):
            sampled_background = random_sampling(background_image, background_height, background_width)
            class_id = np.random.randint(len(labels))
            imgData[j][i] = random_rotate_scale_image( imgData[j][i] )
            result, bbox = random_overlay_image(sampled_background, imgData[j][i], width, height)
            if skip_pad == False:
                yolo_bbox = yolo_format_bbox(result, bbox)
                print(k,j,i,":",yolo_bbox)

            if skip_pad == False:
                # 画像ファイルを保存
                # image_path = "%s/images/train_%s_%s.jpg" % (base_path, i, labels[class_id])
                image_path = "%s/images/train_%s_%s.jpg" % (output_path, i, labels[class_id])
                cv2.imwrite(image_path, result)

                # 画像ファイルのパスを追記
                with open("train.txt", "a") as f:
                    f.write("%s\n" % (image_path))

                # ラベルファイルを保存
                # label_path = "%s/labels/train_%s_%s.txt" % (base_path, i, labels[class_id]) 
                # label_path = "%s\\labels\\train_%s_%s.txt" % (base_path, i, labels[class_id])
                label_path = "./output/labels/train_%s_%s.txt" % (i, labels[class_id])
                f = open(label_path, 'w')
                f.write('')  # 何も書き込まなくてファイルは作成されました
                f.close()
        
                with open(label_path, "w") as f:
                    f.write("%s %s %s %s %s" % (class_id, yolo_bbox[0], yolo_bbox[1], yolo_bbox[2], yolo_bbox[3]))
            else:
                print("Skippped frame")
                skip_pad = False
                i = i-1


print("**************I'm now here.****************")

''' # 一旦テスト用画像生成は廃止。
# test用の画像生成
for i in range(test_images):
    sampled_background = random_sampling(background_image, background_height, background_width)

    class_id = np.random.randint(len(labels))
    fruit = fruits[class_id]
    fruit = random_rotate_scale_image(fruit)

    result, bbox = random_overlay_image(sampled_background, fruit)
    yolo_bbox = yolo_format_bbox(result, bbox)

    if skip_pad == False:
        # 画像ファイルを保存
        # image_path = "%s/images/test_%s_%s.jpg" % (base_path, i, labels[class_id])
        image_path = "%s/images/test_%s_%s.jpg" % (output_path, i, labels[class_id])
        cv2.imwrite(image_path, result)

        # 画像ファイルのパスを追記
        with open("test.txt", "a") as f:
            f.write("%s\n" % (image_path))

        # ラベルファイルを保存
    #    label_path = "%s/labels/test_%s_%s.txt" % (base_path, i, labels[class_id]) 
        label_path = "%s/labels/test_%s_%s.txt" % (output_path, i, labels[class_id]) 
        with open(label_path, "w") as f:
            f.write("%s %s %s %s %s" % (class_id, yolo_bbox[0], yolo_bbox[1], yolo_bbox[2], yolo_bbox[3]))
    else:
        print("Skippped frame")
        skip_pad == False
        i = i -1

    print("test image", i, labels[class_id], yolo_bbox)
'''

