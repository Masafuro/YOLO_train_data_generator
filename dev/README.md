# 開発マップ

2023/01/03

### 開発メモ
| 日付 | 内容 |
----|----
| 2023/01/04 12:30 | deleteGreenback.pyでラベル名のフォルダ構造から画像を取得し、trimmedフォルダにラベル名フォルダで背景を透過、トリミングした画像を出力 |
| 2023/01/06 14:23 | fileFinder.pyが完成。画像アドレスを取得するプログラム。 |

---

### プログラム

#### fielFinder.py
trimmedフォルダからラベルフォルダごとに画像アドレスを取得する。
> --info
を指定した場合、取得した画像一覧をコンソールに表示する。

##　フォルダ構造

<pre>
├─dev：開発中のフォルダ
│  ├─background
│  │  └─：合成する背景画像を入れる。
│  ├─object
│  │  ├─(ラベル名のフォルダ1)：グリーンバックで撮影した画像を入れる。
│  │  └─(ラベル名のフォルダ2)：複数のラベルフォルダを持つことができる。
│  ├─old：開発用の過去データ保管庫
│  ├─output：最終出力先
│  │  ├─images：合成された画像の出力先
│  │  └─labels：生成されたラベルの出力先
│  └─trimmed：グリーンバック画像をトリミングした画像を保管する場所
</pre>


# 過去ログ
## 動作試験
YOLO_train_data_generatorの動作を確認する。

## 遠し動作試験
グリーンバック撮影とIrfanviewを使い、透過pngを生成し、YOLO_train_data_generatorにて所定のタグを得られるか確認する。

## YTDG修正
- ラベル名称のつけ方
- 複数背景画像への対応
- 出力画像の引数指定

### コメント
まずpythonによるグリーンバック透過からやった方がいいかも？？

### グリーンバック透過
cv2のインストール
- [openSSLエラー対策 DL v1.1.1s light](https://qiita.com/SatoshiGachiFujimoto/items/6362de71b8756d8341e7)

cv2のインストール
> conda install -c conda-forge opencv

DLL Load failed
https://qiita.com/nn_tok/items/e3a6b244e29c5a0510b0

pathlib : python >= 3.4

PILのインストール
> pip install pillow

# memo
- [pythonで引数指定](https://qiita.com/stkdev/items/e262dada7b68ea91aa0c)
- [pythonでフォルダ内画像の一括処理](https://zenn.dev/k_neko3/articles/8b89b0ab1c29f8)
- [pythonによるグリーンバック透過](https://teratail.com/questions/355396?link=qa_related_sp)


