# 開発マップ

2023/01/03

### 開発メモ
| 日付 | 内容 |
----|----
| 2023/01/04 12:30 | deleteGreenback.pyでラベル名のフォルダ構造から画像を取得し、trimmedフォルダにラベル名フォルダで背景を透過、トリミングした画像を出力 |
| 2023/01/06 14:23 | fileFinder.pyが完成。画像アドレスを取得するプログラム。 |
| 2023/01/06 21:43 | generate_sample.pyで画像を生成できるようになった。 |
| 2023/01/07 9:26 | generate_sample.pyに使用メモリ量や経過時間などを表示。 |
| 2023/01/07 10:03 | 背景画像をbachgroundフォルダからランダムで読み取りできるようにした。 |
| 2023/01/07 10:50 | annotateionTest.pyで生成した画像をフォルダに保存できるようになった。 |
| 2023/01/07 11:05 | annotationTest.pyで重複なしランダム抽出を実装。 |
| 2023/01/07 11:57 | annotationTest.pyを'--sample'でループ実行できるようになった。ただし、ランダム抽出がうまくいってない。|
| 2023/01/07 12:07 | annotationTest.pyが速くまわるようになった。ただし、必要なサンプリング数よりなんか少なくなる。 |
| 2023/01/07 18:08 | 一旦一通りの動作を確認。途中でハングしたものの278個生成できた。 |
| 実験中の問題 | deleteGreenback.pｙでHSVの範囲をオプションで指定したい。generate_sample.pyが途中でハングする時がある。 また画像の縮尺最大最小もオプションで指定したい。切り抜き方も気になる。|
| 2023/01/07 18:48 | 長く回しているとメモリエラーっぽいのがでる。numpy.core._exceptions.MemoryError: Unable to allocate 12.4 GiB for an array with shape (2, 833586601) and data type int64 |
| 課題 | グリーンバック物撮り撮影の課題：照り返し、影、撮影方法 |
| 次の目標 | 実際に使えるかどうか実験してみる。 |
| 課題 | コードの整形、 また単純なfor文で回しているため、ラベルの画像数に偏りがあると無駄な時間が多い|

---

### プログラム

#### deleteGreenback.py
実行するとobjectフォルダのグリーンバック画像からグリーンバック背景を削除した画像をtrimmedフォルダに出力する。

#### generate_sample.py
オプション
> --loop 10
で10回ループさせるの意味。初期値は10

最後に稼働結果を出力
- loop:ループ数
- label:ラベル数
- genImg:生成画像数
- maxRam:最大使用メモリ量
- genTime:生成にかかった時間

#### annotationTest.py
オプション
> --sample 10
で10個のサンプル画像を作る。画像はアノテーションデータから短径で囲む線を追加したもの。
アノテーションが正しくできているかを確認するよう。


#### fielFinder.py
trimmedフォルダからラベルフォルダごとに画像アドレスを取得する。
> --importInfo
を指定した場合、取得した画像一覧をコンソールに表示する。


generate_sample.pyに組み込み済みの副産物


## フォルダ構造
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
│  └─trimmed：グリーンバック画像をトリミングした画像を保存する場所
│  └─annotated：output/images内からアノテーションテストをした画像が保存される場所
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

コマンドプロンプトの簡易編集モード
> オフにする
> https://tsurezure.info/arbitrage/index.php/2020/05/24/post-506/
よかったっぽい。

# memo
- [pythonで引数指定](https://qiita.com/stkdev/items/e262dada7b68ea91aa0c)
- [pythonでフォルダ内画像の一括処理](https://zenn.dev/k_neko3/articles/8b89b0ab1c29f8)
- [pythonによるグリーンバック透過](https://teratail.com/questions/355396?link=qa_related_sp)
- [pythonでメモリヒープサイズを指定](https://blog.imind.jp/entry/2019/08/10/022501)


