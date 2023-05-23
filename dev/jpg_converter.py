import os
from PIL import Image
import PySimpleGUI as sg

# このプログラムは、指定したフォルダ内の画像をリサイズしてPNG形式に変換し、指定したフォルダに保存するものです。

# フォルダ選択ダイアログを表示し、ユーザーが任意のフォルダを選択できるようにする
folder_path = sg.popup_get_folder('フォルダを選択してください')

# 幅と高さの入力ボックスを表示し、ユーザーが値を入力できるようにする
layout = [
    [sg.Text('幅:'), sg.Input(key='-WIDTH-')],
    [sg.Text('高さ:'), sg.Input(key='-HEIGHT-')],
    [sg.Button('実行')]
]

window = sg.Window('画像処理プログラム', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == '実行':
        width = int(values['-WIDTH-'])
        height = int(values['-HEIGHT-'])
        break

window.close()

# フォルダが存在しなければ作成する
export_folder = os.path.join(folder_path, 'export')
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

# フォルダ内のjpg画像を読み込んでリサイズし、PNG形式で保存する
for filename in os.listdir(folder_path):
    if filename.lower().endswith('.jpg'):
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        resized_image = image.resize((width, height))
        new_filename = os.path.splitext(filename)[0] + '.png'
        export_path = os.path.join(export_folder, new_filename)
        resized_image.save(export_path, 'PNG')

# 処理が完了したことを通知する
sg.popup('処理が完了しました')
