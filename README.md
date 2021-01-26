# dm2geojson

## 概要

DMデータをGeoJSON形式に変換します。

機能の概要は、[こちら](https://takamoto.biz/osaka-gis/dm3/)を確認してください。

とりあえず素材をアップした状態ですので、徐々に使いやすくしていこうと思っています。

## 前提条件

- Python3.6以上
- Python拡張モジュール
    - numpy
    - pyproj

## 利用方法

- DMデータを1つのフォルダーにまとめる
- ソース GeoJSONWriter.py 
    - 18行目のEPSGコードを任意のものに書き換える（デフォルトはEPSG2448（JGD2000の平面直角６系））
    - 120行目をDMデータをまとめたフォルダーに書き換える
- 以下のイメージでスクリプトを実行
`$ python GeoJSONWriter.py`
- カレントディレクトリに`dm.json`が作成されます

上記ファイルをQGIS等に読み込ませれば、地図表示ができシェープファイルなどにも変換できます。

## 参考情報

- 大阪市のDMデータは、以下から入手できます。
https://www.geospatial.jp/ckan/dataset/h30-dm-pdf-dxf

- 大阪市のDMデータの変換データサンプルは以下となります。
https://labo.takamoto.biz/osakadm

