import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import random

MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

# ★今までに作成したコードからGameクラスをコピー★

class Game:

    def __init__(self, number_of_mines = 10):
        """ ゲームボードの初期化
        
        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        """ ゲーム盤を初期化 """
        # <-- (STEP 1) ここにコードを追加 
        # MS_SIZE x MS_SIZE で初期化
        self.game_board = np.zeros((MS_SIZE, MS_SIZE))

    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """
        # <-- (STEP 2) ここにコードを追加
        # (1)
        # MS_SIZE x MS_SIZE で初期化
        self.mine_map = np.zeros((MS_SIZE, MS_SIZE))
        
        # (2) number_of_mines個のセルをランダムに選択して地雷を設定する
        if number_of_mines > MS_SIZE*MS_SIZE:
            number_of_mines = MS_SIZE*MS_SIZE
        if number_of_mines < 0:
            number_of_mines = 0

        p = [(random.random(), i) for i in range(MS_SIZE**2)]
        p.sort()
        for r, i in p[:number_of_mines]:
            y = i // MS_SIZE
            x = i % MS_SIZE
            self.mine_map[y][x] = -1
    
    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """
        # <-- (STEP 3) ここにコードを追加
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                y_start = max(y-1, 0)
                y_end = min(y+1, MS_SIZE-1)
                x_start = max(x-1, 0)
                x_end = min(x+1, MS_SIZE-1)
                
                if self.mine_map[y][x] >= 0:
                    self.mine_map[y][x] = np.sum(self.mine_map[y_start:y_end+1, x_start:x_end+1] == -1)
    
    def open_cell(self, x, y):
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置
        
        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，既に開いているセルの近傍セルは開けない．
                   地雷セル，FLAGが設定されたセルは開けない．
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        """
        # <-- (STEP 4) ここにコードを追加
        if self.mine_map[y][x] == -1:
            # 地雷を選択した場合、ゲームオーバーにする
            return False
        
        else:
            # 既に開いているセルを開いた場合は、そのままで8近傍は開かない
            if self.game_board[y][x] == OPEN:
                return True
            
            # セルを開く
            self.game_board[y][x] = OPEN
            
            # 8近傍のセルを開く
            for j in range(-1, 2, 1): # -1~1
                for i in range(-1, 2, 1): # -1~1
                    # 範囲内で、FLAGではないとき
                    if y+j>=0 and x+i>=0 and y+j<=MS_SIZE-1 and x+i<=MS_SIZE-1 and self.game_board[y+j][x+i]!=FLAG:
                        if self.mine_map[y+j][x+i] != -1:
                            # 地雷がなければ開く
                            self.game_board[y+j][x+i] = OPEN
            return True
    
    def flag_cell(self, x, y):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        # <-- (STEP 5) ここにコードを追加
        if self.game_board[y][x] == CLOSE:
            self.game_board[y][x] = FLAG
        
        # すでにフラグが立っていたら、フラグを解除してCLOSE状態に戻す
        elif self.game_board[y][x] == FLAG:
            self.game_board[y][x] = CLOSE
            
        # 開いているセルを指定した場合は何もしない
            
    def is_finished(self):
        """ 地雷セル以外のすべてのセルが開かれたかチェック """
        # <-- (STEP 6) ここにコードを追加      
        return not np.any((self.game_board != OPEN) & (self.mine_map != -1))

class MyPushButton(QPushButton):
    
    def __init__(self, text, x, y, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding)
        
    def set_bg_color(self, colorname):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))
        
    def on_click(self):
        """ セルをクリックしたときの動作 """
        # ★以下，コードを追加★
        # キーを取得
        key = QApplication.keyboardModifiers()
        # shiftキーが押されているとき
        if key==Qt.ShiftModifier:
            # フラグを立てる
            self.parent.game.flag_cell(self.y, self.x)
            
        # shiftキーが押されていなく、フラグが立っていたら何もしない
        elif self.parent.game.game_board[self.x][self.y]==FLAG:
            pass
        
        # 地雷セルを開けたら、ゲームオーバーにする
        elif self.parent.game.mine_map[self.x][self.y]==-1:
            # メッセージを出して、プログラム終了
            QMessageBox.information(self,"","ゲームオーバー!")
            QCoreApplication.exit(0)
    
        # それ以外ならセルを開く
        else:
            self.parent.game.open_cell(self.y, self.x)
        
        # セルの表示を更新する
        self.parent.show_cell_status()
        
        # ゲームが終了していればメッセージを出して、プログラム終了
        if self.parent.game.is_finished():
            QMessageBox.information(self,"","ゲームクリア!")
            QCoreApplication.exit(0)
        
        pass
            
class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(100, 100) 
        self.setWindowTitle('Minesweeper')
        
        # ★以下，コードを追加★
        # ステータスバーに文字列を表示する
        self.statusBar().showMessage("Shift+クリックでフラグをセット")
        
        # ボタンを入れる配列を初期化する
        self.button = [[None for i in range(MS_SIZE)] for j in range(MS_SIZE)]
        
        # ボタンを配置する
        layout = QGridLayout() # 格子状に配置する

        for i in range(8):
            for j in range(8):
                self.button[i][j] = MyPushButton('x', i, j, parent=self)
                self.button[i][j].clicked.connect(self.button[i][j].on_click)
                layout.addWidget(self.button[i][j], i, j)
                self.button[i][j].set_bg_color("gray") # 灰色にする
            
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        layout.setSpacing(0) # ボタン同士の隙間をなくす        
        
        self.show()
    
    def show_cell_status(self):
        """ ゲームボードを表示 """
        # ★以下，コードを追加★
        for i in range(MS_SIZE):
            for j in range(MS_SIZE):
                if self.game.game_board[i][j]==CLOSE:
                    self.button[i][j].setText("x")
                    self.button[i][j].set_bg_color("gray")
                elif self.game.game_board[i][j]==FLAG:
                    self.button[i][j].setText("P")
                    self.button[i][j].set_bg_color("yellow")
                else:
                    if self.game.mine_map[i][j]==0:
                        self.button[i][j].setText("")
                    else:
                        self.button[i][j].setText(str(int(self.game.mine_map[i][j])))
                    self.button[i][j].set_bg_color("blue")
                 
def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()
            
if __name__ == '__main__':
    main()