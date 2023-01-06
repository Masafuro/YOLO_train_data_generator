import os
print("START fileFinder.py")

object_path ="./object"
files = os.listdir( object_path )
files_dir = [f for f in files if os.path.isdir(os.path.join( object_path , f))]
labels = files_dir
print("labels:", labels)

path = "./object"
files = os.listdir( path )
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
print(files_file)   # ['file1', 'file2.txt', 'file3.jpg']


'''
# ラベルフォルダからの画像取得
for w in labels:
    print(w + ":" + str(type(w)) )
    img_path = object_path + "/" + w
    print("img_path:" + img_path + ":" + str(type(img_path)))
    img_files_path = os.listdir(img_path)
    img_files = [f for f in img_files_path if os.path.isfile(os.path.join(img_files_path, f))]
    print(img_files)   # ['file1', 'file2.txt', 'file3.jpg']

'''