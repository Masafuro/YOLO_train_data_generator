# YOLO用画像合成スクリプト
フォーク：[Ieetenkiさん](https://github.com/leetenki/YOLO_train_data_generator)
をベースにグリーンバックで撮影した画像と背景画像を元に学習用画像とアノテーションを生成するスクリプト

##　フォルダ構造

アノテーションの出力はYOLO形式（のハズ）です。
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

## スクリプト
2023/01/04 現在
- **目下、開発中でところどころ動いていません。**
- deleteGreenback1.py:object画像からグリーンバック背景を除去、トリミングし、物体だけの背景が透過された画像を生成する。
- generatesample4.py:deleteGreenback1.pyで作った画像を背景をランダムに合成し、アノテーションと画像を出力する。
  - '--loop 10' で10回ループさせるのオプションコマンド


