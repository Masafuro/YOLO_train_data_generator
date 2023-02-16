import tkinter as tk
from tkinter import filedialog

# ルートウィンドウを作成
root = tk.Tk()
root.withdraw()

# フォルダを選択させるダイアログを表示
folder_path = filedialog.askdirectory()

# フォルダが選択された場合は、フォルダのパスを表示する
if folder_path:
    print("Selected folder:", folder_path)

import os
from PIL import Image

# フォルダをユーザーに指定してもらう

# 幅の閾値
min_width = 10
min_height = 10

# フォルダ内のファイルを処理する
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        # 画像ファイルを開く
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r'):
                pass
            image = Image.open(file_path)
        except:
            print(f"Failed to open {file_name}")
            continue

        # 画像の幅を取得
        width, height = image.size
        del image
        # 幅が閾値未満の場合は、画像を削除
        if width < min_width or height < min_height:
            os.remove(file_path)
            print(f"Deleted {file_name}")
