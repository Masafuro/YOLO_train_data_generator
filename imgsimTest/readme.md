# 開発
> conda activate imgsim
> cd -> 所定のimgsimTestまで移動


# 画像の類似度を判別する
featureMatching.pyでimagesフォルダ内の画像で全ての距離を測定し、export.csvを出力できるようになった。

'''mermaid
sequenceDiagram
    participant A as エージェントA
    participant B as エージェントB
    A->>B: リクエスト
    B-->>A: レスポンス

'''


imagesフォルダに入っている画像
比較元にする画像　001.pngにする

> python calcImageSim.py
として実行
images内の画像の類似度が判定され、類似度名のファイルに変更される。

