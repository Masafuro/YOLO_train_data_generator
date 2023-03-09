import cv2

# 画像の読み込み
img = cv2.imread('00000.png')

# リサイズ前のサイズを表示
print('Original Image Shape:', img.shape)

# リサイズするサイズを指定
new_size = (400, 300)

# リサイズを実行
resized_image = cv2.resize(img, new_size)

# リサイズ後のサイズを表示
print('Resized Image Shape:', resized_image.shape)
