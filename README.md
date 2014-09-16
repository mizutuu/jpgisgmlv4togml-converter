jpgisgmlv4togml-converter
=========================

国土地理院 基盤地図情報基本項目 JPGIS(GML) V4.0形式のデータを、GMLに変換するコンバータです。

基盤地図情報：[http://www.gsi.go.jp/kiban/](http://www.gsi.go.jp/kiban/)


## 使い方

* 基盤地図情報基本項目XMLデータを、GMLに変換する

`$ cat FG-GML-533946-AdmArea-20140701-0001.xml | python jpgisgml2gml.py > AdmArea.gml`

* GMLを、Shapeに変換する

`$ ogr2ogr -f "ESRI Shapefile" -lco "ENCODING=UTF-8" AdmArea AdmArea.gml`


## GMLへの変換結果

[GMLへの変換詳細](https://github.com/mizutuu/jpgisgmlv4togml-converter/wiki)に、変換前後の比較をまとめました。


## 制限事項

本スクリプトで変換可能な基盤地図情報基本項目のXMLデータは、以下表に記載のクラスに限られます。

### 動作検証済み項目

| データ項目        | クラス名    |
| --------------- | ---------- |
| 標高点           | ElevPt     |
| 等高線           | Cntr       |
| 行政区画         | AdmArea    |
| 行政区画界線      | AdmBdry    |
| 町字界線         | CommBdry   |
| 行政区画代表点    | AdmPt      |
| 町字の代表点      | CommPt     |
| 街区線           | SBBdry     |
| 街区の代表点      | SBAPt      |
| 水域             | WA         |
| 水涯線           | WL         |
| 海岸線           | Cstline    |
| 水部構造物線      | WStrL      |
| 水部構造物面      | WStrA      |
| 建築物           | BldA       |
| 建築物の外周線    | BldL       |
| 道路縁           | RdEdg      |
| 道路構成線        | RdCompt    |
| 軌道の中心線      | RailCL     |

* 幾つかのXMLデータで変換できることを確認済みの状態です。但し、日本全国の範囲では未確認です。
* 検証は"変換できる" / "変換できない" を元に判断しており、変換後のGMLにデータ欠損があるかどうかは確認できていません。


### 未チェック項目

| データ項目        | クラス名    |
| --------------- | ---------- |
| 街区域           | SBArea     |
| 河川堤防表法肩法線 | LeveeEdge  |
| 河川区域界線      | RvrMgtBdry |
| 道路域分割線      | RdASL      |
| 道路域域         | RdArea      |
| 道路区分面        | RdSgmtA    |
| 道路区域界線      | RdMgtBdry  |

* まだ確認していない項目です。順次検証しているので、XMLデータ発見時に検証します。


## Todo

* GMLへの変換検証
* エラートラップ/Usage
* テストケース追加
