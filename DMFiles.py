import glob
import os

# -----------------------------------------
# DMファイルリスト管理クラス 
# 2020.05.23 K.Takamoto(takamoto.biz)
# -----------------------------------------
class DMFiles:
    #============================================================
    # コンストラクタ
    # out: self._MAPPath、self._MAPList
    #============================================================
    def __init__( self ,inPath ):
        # パスを保存
        self._MAPPath = inPath

        # ディレクトリの存在確認しdmファイルのリストを作成
        if os.path.exists(self._MAPPath):
            self._MAPList = glob.glob( self._MAPPath + "/*.dm")
        else:
            self._MAPList = None

    #============================================================
    # Function : イテレータ開始処理：イテレータの初期化
    #============================================================
    def __iter__(self):
        # イテレータ用カウンタ初期化
        self._i=0
        # それ以外の処理はコンストラクタで済んでいる。（self._MAPListへのファイルリスト作成）
        return self
    #============================================================
    # Function : イテレータ取得処理：指定ファイルの形状情報を順次読みだす。
    # out: _MAPListのメンバー（DATファイルのフルパス）
    #============================================================
    def __next__(self):
        # データなしの場合は終了
        if self._MAPList == None:
            raise StopIteration()
        # データありの場合は次データ取得
        if self._i >= len(self._MAPList):
            raise StopIteration()
        value = self._MAPList[self._i]
        self._i+=1
        return value
