jpgisgmlv4togml-converter
=========================

JPGIS(GML) V4.0形式の基盤地図情報(基本項目)データを、GMLに変換するコンバータです。

使い方
-----

* 基盤地図情報基本項目XMLデータを、GMLに変換する

`cat FG-GML-533946-AdmArea-20140701-0001.xml | python jpgisgml2gml.py > AdmArea.gml`

* GMLを、Shapeに変換する

`ogr2ogr -f "ESRI Shapefile" -lco "ENCODING=UTF-8" AdmArea AdmArea.gml`


制限事項
-----

すべての基盤地図情報基本項目XMLデータを、GMLに変換できるかはまだ検証していません。


Todo
-----

* GMLへの変換検証
* xsdファイルを外部から指定可能なように変更
* テストケース追加
