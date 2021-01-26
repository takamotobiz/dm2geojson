import struct
import numpy

# -----------------------------------------
# DM DATファイル読み込みクラス 
# 2020.05.23 K.Takamoto(takamoto.biz)
# -----------------------------------------
class DM:
    #============================================================
    # コンストラクタ
    # out: self._DATFile
    #============================================================
    def __init__(self ,inDMFile ):
        # 入力ファイルをクラス変数に保存
        self._DMFile = inDMFile
        # 図形情報出力用ディクショナリ配列の宣言（0始まり）
        self._elementDict = {}

    #============================================================
    # Function : イテレータ開始処理：指定ファイルの形状情報をすべて読みだす。
    # in       : None（コンストラクタの引数 inATRFile）
    # out      : 図形情報の配列(self.elementDict)
    #============================================================
    def __iter__(self):
        # DATファイルの読み込み
        with open(self._DMFile ,mode='rb') as dmfd:
            # 全レコードの読み込み（バイナリでも行として取得できる模様）
            # DMファイルの1レコードは87バイト（CR+LFの2バイトを含む）
            # DMファイルの最後のEOF（0x1A）の明示的な取得は不要
            self._reclist = dmfd.readlines()
            # レコードカウンタ初期化
            dictSeqno = recno = 0
            while recno < len(self._reclist)-1:
                # レコードの取得
                record = self._reclist[recno]
                # レコードタイプの取得
                rectype = str(record[0:2].decode('cp932'))
                # レコード判定
                if rectype[0]=='M':
                    # 図郭レコード(a) 図郭ごとに1レコード群のみ
                    # 図郭識別番号
                    self.unitcode = str(record[2:10].decode('cp932')).rstrip()
                    # 修正回数取得
                    editcnt = int(record[65:67].decode('cp932'))
                    recno+=1
                    # 図郭レコード(b)の取得（単位はメートル）
                    record = self._reclist[recno]
                    self.ldx = float(record[0:7].decode('cp932'))
                    self.ldy = float(record[7:14].decode('cp932'))
                    # 図郭レコード(d)までシーク
                    recno += 2
                    cnt = 0
                    while cnt < editcnt+1:
                        # 図郭レコード(d)の取得（捨て）
                        record = self._reclist[recno]
                        reccnt = int(record[9:10].decode('cp932'))
                        recno += reccnt+2
                        cnt += 1
                elif rectype[0]=='E':
                    # 要素レコード（"E1"～"E8"）
                    # 分類コード
                    layercode = str(record[2:6].decode('cp932'))
                    # 要素識別番号
                    elementno = int(record[12:16].decode('cp932'))
                    # レコード数
                    recordcnt = int(record[31:35].decode('cp932'))
                    # 実データ区分（0,1：データなし、2：二次元、4：注記）
                    datakind = str(record[20:21].decode('cp932'))
                    # データ数（座標点数、文字数）
                    datacnt = int(record[27:31].decode('cp932'))
                    if rectype=='E1' or rectype=='E2':
                        # 線（E2）と面（E1）
                        # 実データレコード取得Loop
                        pointcnt = cnt = 0
                        xy = []
                        # 座標情報の取得
                        while pointcnt < datacnt:
                            if ( pointcnt % 6 )==0:
                                # 二次元座標レコード(8)の取得
                                recno += 1
                                record = self._reclist[recno]
                            start = ( pointcnt * 14 ) % 84
                            # 座標をミリメートルからメートルに変換
                            xy.append( [ self.ldy + float(record[start+7:start+14].decode('cp932'))/1000, \
                                         self.ldx + float(record[start:start+7].decode('cp932'))/1000 ] )
                            #print(float(record[start:start+7].decode('cp932')) ,float(record[start+7:start+14].decode('cp932')))
                            pointcnt += 1
                        # 始終点が一致していれば面化する
                        if xy[0]==xy[len(xy)-1]:
                            rectype = 'E1'
                        # ディクショナリへのデータ設定
                        self._elementDict[dictSeqno] = {"FIGTYPE":rectype,"LAYER":layercode, \
                                                        "ELNO":self.unitcode + '-' + layercode + '-' + str(elementno).zfill(4),\
                                                        "XYList":xy}
                        #print(self._elementDict[dictSeqno])
                        # ディクショナリカウンタの加算
                        dictSeqno += 1
                        # レコードカウンタの加算
                        recno += 1
                    elif rectype=='E7':
                        # 注記（E7）
                        # 代表点座標（ミリメートルからメートルに変換）
                        pointxy = [ self.ldy + float(record[42:49].decode('cp932'))/1000 , \
                                    self.ldx + float(record[35:42].decode('cp932'))/1000 ]
                        # 二次元座標レコード(8)の取得
                        record = self._reclist[recno+1]
                        # 縦横フラグ（0:横書き、1:縦書き）
                        vnflag = str(record[0:1].decode('cp932'))
                        # 角度（横書き:-45～45、縦書き:-135～-45）
                        angle = int(record[1:8].decode('cp932'))
                        # 注記文字：今回は1レコード目まで。2レコード目以降は捨てる
                        text = str(record[20:84].decode('cp932')).rstrip()
                        #print(str(elementno) +':' + text)
                        # ディクショナリへのデータ設定
                        self._elementDict[dictSeqno] = {"FIGTYPE":rectype,"LAYER":layercode, \
                                                        "ELNO":self.unitcode + '-' + layercode + '-' + str(elementno).zfill(4),\
                                                        "XYList":pointxy ,"ANGLE":angle ,"VNFLAG":vnflag ,"TEXT":text}
                        #print(self._elementDict[dictSeqno])
                        # ディクショナリカウンタの加算
                        dictSeqno += 1
                        # レコード数分シーク
                        recno += recordcnt+1
                    else:
                        # レコード数分シーク
                        recno += recordcnt+1
                elif rectype[0]=='H':
                    # グループヘッダレコード
                    recno += 1
                elif rectype[0]=='G' or rectype[0]=='T':
                    # グリッドヘッダ、TINレコード
                    # レコード数
                    recordcnt = int(record[31:35].decode('cp932'))
                    recno += recordcnt+1

        # イテレータ用カウンタ初期化
        self._i=0
        return self

    #============================================================
    # Function : イテレータ取得処理：指定ファイルの形状情報を順次読みだす。
    # in       : 図形情報の配列(self.elementDict)
    # out      : 図形情報(self.elementDictのメンバ)
    #============================================================
    def __next__(self):
        if self._i >= len(self._elementDict):
            raise StopIteration()
        value = self._elementDict[self._i]
        self._i+=1
        return value

    # デストラクタ
    def __del__(self):
        pass
