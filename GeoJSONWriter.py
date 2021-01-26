# -----------------------------------------
# GeoJSON出力用クラス 2020.5.24 K.Takamoto(takamoto.biz)
# -----------------------------------------
import numpy as np
# 座標系変換のために追加
from pyproj import Proj ,Transformer ,itransform

class GeoJSONWriter:
    # コンストラクタ
    def __init__( self ,inOutFile ):
        # 出力ファイルのオープン（とりあえず失敗・例外を考慮しない）
        self._jsonfd = open(inOutFile ,'w' ,encoding='utf-8')
        # ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None
        # 世界測地系測地平面直角6系からWGS84への変換器作成
        self._srcproj = Proj(init='epsg:2448', preserve_units=False)
        self._dstproj = Proj(init='epsg:4326', preserve_units=False)
        self._transtky2wgs = Transformer.from_proj(self._srcproj,self._dstproj)

    # デストラクタ
    def __del__(self):
        # フッターを書き込み
        self._jsonfd.write( "\n" + "]}")
        # ファイルのクローズ
        self._jsonfd.close()

    # ジオメトリの設定
    def setGeometry(self ,inFigtype ,inXyList):
        # 座標の変換
        if inFigtype==1:
            # FIGTYPE=1 : 折れ線
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "LineString" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"["
            for Xy in inXyList:
                # 座標変換
                Xy = self._transtky2wgs.transform(Xy[0] ,Xy[1])
                self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
            # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
            self.Geometry = self.Geometry[:-1]
            self.Geometry+="]"
        elif inFigtype==2:
            # FIGTYPE=2 : ポリゴン
            # 座標を逆転させて始終点を一致
            XyList = np.flipud(inXyList)
            XyList = np.append(XyList ,XyList[[0]] ,axis=0)
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "Polygon" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"[["
            for Xy in XyList:
                # 座標変換
                Xy = self._transtky2wgs.transform(Xy[0] ,Xy[1])
                self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
            # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
            self.Geometry = self.Geometry[:-1]
            self.Geometry+="]]"
        elif inFigtype==4:
            # FIGTYPE=4 : 文字
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "Point" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":"
            # 座標変換
            Xy = self._transtky2wgs.transform(inXyList[0] ,inXyList[1])
            self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "]"
        elif inFigtype==6:
            # FIGTYPE=6 : 記号
            pass

    # プロパティの設定
    def setPropertie(self ,inName ,inValue):
        # 2つ目以降か？
        if self.Properties==None:
            # 1つ目
            self.Properties = "\t" + "\"" + "properties"+ "\"" + ":{"
        else:
            # 2つ目以降
            self.Properties+= ","
        if type(inValue) is list:
            # 文字列リスト
            self.Properties+= "\"" + inName + "\""+":" + "\"" + "".join(inValue) + "\""
        else:
            # 文字列項目
            self.Properties+= "\"" + inName + "\""+":" + "\"" + str(inValue) + "\""

    # プロパティの設定
    def setTippecanoe(self ,inValue):
        self.Tippecanoe = "\t" + "\"" + "tippecanoe" + "\"" + ":{" + "\"" + "layer" + "\"" + ":" + "\"" + str(inValue) + "\""

    # ファイルの書き込み
    def Write(self):
        if self._jsonfd.tell()==0 :
            # 最初はヘッダーを書き込み
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            # 最初の書き込み以外
            self._jsonfd.write(",\n")
        self._jsonfd.write(self.Geometry + "}," + "\n")
        self._jsonfd.write(self.Tippecanoe + "}," + "\n")
        self._jsonfd.write(self.Properties + "}"+"}")
        # ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

if __name__ == '__main__':

    from DMFiles import DMFiles
    from DM import DM

    # inKind は地図種別で、下記5種類

    # 
    gjWriter = GeoJSONWriter( r"dm.json" )
    # DMファイルインスタンスの生成
    dmfiles = DMFiles( r"D:\data\dm_osaka\DM" )
    # 存在ファイル分Loop
    for dmfile in dmfiles:
        print('File:[' + dmfile + ']')
        # DATファイル内の全要素を取得（配列）
        dats = DM(dmfile)
        for dat in dats:
            if dat["FIGTYPE"]=='E2':
                # 折れ線
                # 1.ジオメトリの出力
                gjWriter.setGeometry( 1, dat["XYList"] )
                # 2.Tippecanoeタグ出力
                gjWriter.setTippecanoe(dat["LAYER"])
                # 3.プロパティ出力
                gjWriter.setPropertie("Layer" ,dat["LAYER"])
                gjWriter.setPropertie("Elno" ,dat["ELNO"])
                # ファイル出力
                gjWriter.Write()
            elif dat["FIGTYPE"]=='E1':
                # ポリゴン
                # 1.ジオメトリの出力
                gjWriter.setGeometry( 2, dat["XYList"] )
                # 2.Tippecanoeタグ出力
                gjWriter.setTippecanoe(dat["LAYER"])
                # 3.プロパティ出力
                gjWriter.setPropertie("Layer" ,dat["LAYER"])
                gjWriter.setPropertie("Elno" ,dat["ELNO"])
                # ファイル出力
                gjWriter.Write()
            elif dat["FIGTYPE"]=='E7':
                # 文字
                # 1.ジオメトリの出力
                gjWriter.setGeometry( 4, dat["XYList"] )
                # 2.Tippecanoeタグ出力
                gjWriter.setTippecanoe(dat["LAYER"])
                # 3.プロパティ出力
                gjWriter.setPropertie("Layer" ,dat["LAYER"])
                gjWriter.setPropertie("Elno" ,dat["ELNO"])
                gjWriter.setPropertie("Text" ,dat["TEXT"])
                gjWriter.setPropertie("Vnflag" ,dat["VNFLAG"])
                gjWriter.setPropertie("Angle" ,dat["ANGLE"])
                # ファイル出力
                gjWriter.Write()

        # DATオブジェクトの消去
        dats = None
