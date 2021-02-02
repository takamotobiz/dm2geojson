# dm2geojson

## 概要

DMデータをGeoJSON形式に変換します。

機能の概要は、[私のブログ記事](https://takamoto.biz/osaka-gis/dm3/)を参照してください。

## 前提条件

- Python3.6以上
- Python拡張モジュール
    - numpy
    - pyproj

## 利用方法

- DMデータを1つのフォルダーにまとめます。
- ソース GeoJSONWriter.py を以下のように修正します。
    - 18行目のEPSGコードを任意のものに書き換え（デフォルトはEPSG2448（JGD2000の平面直角６系））
    - 120行目をDMデータをまとめたフォルダーに書き換え
- 以下のイメージでスクリプトを実行します。  
```$ python GeoJSONWriter.py```
- カレントディレクトリにGeoJSONファイル`dm.json`が作成されます。

上記ファイルをQGIS等に読み込ませれば、地図表示ができシェープファイルなどにも変換できます。

## その他

このリポジトリは、ブログ執筆時のソースを急遽をアップしたものですので、直書き部分が多くて荒っぽい状態となっています。
リクエストがあれば、Issueや私のブログに意見投稿してください。
Docker化とDMデータから直接シェープに変換する機能はいずれ実現したいと思っています。

## 参考情報

- EPSGコードは、以下に一覧があります。  
https://tmizu23.hatenablog.com/entry/20091215/1260868350

- 大阪市のDMデータは、以下から入手できます。  
https://www.geospatial.jp/ckan/dataset/h30-dm-pdf-dxf

<!--
- 大阪市のDMデータの変換データサンプルは以下となります。  
https://takamotobiz.github.io/dm2geojson/osakadm.html
--!>