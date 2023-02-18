import argparse

parser = argparse.ArgumentParser(description='Command line argument parser example')
parser.add_argument('--keyword', default="cat", type=str, help='Keyword to search for')
parser.add_argument('--Num', type=int, default=10, help='Number of images to download')
parser.add_argument('--size', type=str,default="small", help='Size of images to download (e.g. "large", "medium", "small")')
parser.add_argument('--resize', type=int, default=320, help='Resize value')

args = parser.parse_args()

print(f"Keyword: {args.keyword}")
print(f"Number of images: {args.Num}")
print(f"Image size: {args.size}")
print(f"Resize: {args.resize}")


import tkinter as tk
from tkinter import filedialog

def select_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory()
    return dir_path

# 関数の実行と出力
selected_dir = select_directory()
print(f"Selected directory: {selected_dir}")

from icrawler.builtin import BingImageCrawler

def download_images(keyword, num_images, size, output_dir):
    # BingImageCrawlerオブジェクトを作成
    crawler = BingImageCrawler(storage={'root_dir': output_dir})

    # クロール対象の設定
    filters = dict(
        size=size
    )

    # クロールを実行
    crawler.crawl(keyword=keyword, filters=filters, max_num=num_images)

# 関数の実行
download_images(args.keyword, args.Num, args.size, selected_dir)

from PIL import Image
import os

def resize_images_in_folder(folder_path, new_size):
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            filepath = os.path.join(folder_path, filename)
            with Image.open(filepath) as im:
                im_resized = im.resize((new_size, new_size))
                im_resized.save(filepath)

resize_images_in_folder(selected_dir, args.resize)