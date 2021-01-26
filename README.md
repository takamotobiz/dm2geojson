# dm2geojson

## 概要

DMデータをGeoJSON形式に変換します。

機能の概要は、[こちら](https://takamoto.biz/osaka-gis/dm3/)を確認してください。

## 前提条件

- Python3.6以上
- Python拡張モジュール
    - numpy
    - pyproj
    - numpy


## 利用方法

- DMデータを1つのフォルダーにまとめる
- ソース GeoJSONWriter.py の120行目を上記パスに合わせて書き換える
- 以下のイメージでスクリプトを実行
`$ python GeoJSONWriter.py`
- カレントディレクトリに`dm.json`が作成されます

上記ファイルをQGIS塔に読み込ませれば、Shapeなどにも変換できます。

参考までに、大阪市のDMデータは、以下から入手できます。
https://www.geospatial.jp/ckan/dataset/h30-dm-pdf-dxf
