import pyxel

#ボタンの表示と管理
class Buttons:

    def __init__(self):
        self.radius = -4
        self.speed = 1

    def move(self):
        if (self.radius < -4):
            self.speed = -self.speed
        elif (self.radius > 4):
            self.speed = -self.speed

        self.radius += self.speed / 3

class Statuscount:

    def __init__(self):
        self.sta = 0
        self.stacha = 0

    def stcon(self,hp):
        self.stacha = 0

        if self.sta >= 100:
            self.sta = 100
            return 0

        if pyxel.rndi(0, 70) <= hp + 20:
            self.stacha += pyxel.rndi(18, 24)
            self.sta += self.stacha
            if self.sta >= 100:
                self.sta = 100
            return self.stacha
        else:
            return 0


class CatMove:
    def __init__(self):
        self.x = 230
        self.y = 40

    def moving(self,sec):
        if sec <= 30:
            self.x -= 1
            self.y += 1
        else:
            self.x += 1
            self.y -= 1

class App:

    def __init__(self):
        pyxel.init(600,450)
        pyxel.cls(6)

        pyxel.image(0).load(0, 0, "cat1.png")
        pyxel.image(1).load(0, 0, "numbers.png")
        pyxel.image(2).load(0, 0, "cat2.png")

        pyxel.sound(0).set(notes='A3C4F4A4', tones='TTTT', volumes='3333', effects='NNNN', speed=10)
        pyxel.sound(1).set(notes='A3RB3', tones='PPP', volumes='222', effects='NNN', speed=10)
        pyxel.sound(2).set(notes='A4F4C4A3', tones='TTTT', volumes='3333', effects='NNNV', speed=10)
        pyxel.sound(3).set(notes='F4C4A3', tones='TTTT', volumes='3333', effects='NNNV', speed=10)
        pyxel.sound(4).set(notes='A3C4F4A4C4E4G4B4', tones='TTTTTTTT', volumes='33333333', effects='NNNNNNNV', speed=10)

        self.hp = 100
        self.day = 0
        self.gamestatus = 0#画面遷移
        self.catstatus = 0#猫の顔変化
        self.clickflag = True#クリック受けつけ判定
        self.sec = 0#時間経過
        self.change = 0#ステータスの増加量
        self.log = ["start!"]


        self.command = [Buttons(),Buttons(),Buttons(),Buttons()]#ボタンクラスの格納
        self.status =  [Statuscount(),Statuscount(),Statuscount()]#ステータス　順番に活発美しさ賢さ
        self.itemmove = CatMove()

        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)

        if self.gamestatus == 0:
            if pyxel.btnp(pyxel.KEY_SPACE):
                pyxel.play(0, 0)
                self.gamestatus = 1

        elif self.gamestatus == 1:
            #クリック箇所の判定とステータス増減
            if self.clickflag == True:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    if ((150-pyxel.mouse_x)*(150-pyxel.mouse_x)+(390-pyxel.mouse_y)*(390-pyxel.mouse_y)) < 300:
                        if self.hp < 100:
                            self.change += pyxel.rndi(30, 45)
                            self.hp += self.change
                            self.log.append("HP increased by " + str(self.change))
                            self.clickflag = False
                            self.catstatus = 1
                            pyxel.play(0, 1)
                    elif ((250-pyxel.mouse_x)*(250-pyxel.mouse_x)+(390-pyxel.mouse_y)*(390-pyxel.mouse_y)) < 300:
                        self.hp -= pyxel.rndi(7, 17)
                        self.change = self.status[0].stcon(self.hp)
                        self.log.append("active increased by " + str(self.change))
                        self.clickflag = False
                        self.catstatus = 2
                        pyxel.play(0, 1)
                    elif ((350-pyxel.mouse_x)*(350-pyxel.mouse_x)+(390-pyxel.mouse_y)*(390-pyxel.mouse_y)) < 300:
                        self.hp -= pyxel.rndi(7, 17)
                        self.change = self.status[1].stcon(self.hp)
                        self.log.append("beauty increased by " + str(self.change))
                        self.clickflag = False
                        self.catstatus = 3
                        pyxel.play(0, 1)
                    elif ((450-pyxel.mouse_x)*(450-pyxel.mouse_x)+(390-pyxel.mouse_y)*(390-pyxel.mouse_y)) < 300:
                        self.hp -= pyxel.rndi(7, 17)
                        self.change = self.status[2].stcon(self.hp)
                        self.log.append("intelligence increased by " + str(self.change))
                        self.clickflag = False
                        self.catstatus = 4
                        pyxel.play(0, 1)

            if self.hp < 0:
                self.hp = 0
            elif self.hp > 100:
                self.hp = 100

            #クリックの受けつけを判定する場所
            if  self.clickflag == False:
                self.sec += 1
                self.itemmove.moving(self.sec)

            if self.sec >= 60:
                self.day += 1
                self.change = 0
                self.clickflag = True
                self.sec = 0
                self.catstatus = 0

            #ボタンのアニメーション
            for i in range(0, len(self.command)):
                self.command[i].move()

            if self.day == 10:
                if self.status[0].sta+self.status[1].sta+self.status[2].sta > 186:
                    pyxel.play(0, 4)
                else:
                    pyxel.play(0, 2)
                self.gamestatus = 2


        elif self.gamestatus == 2:
            if pyxel.btnp(pyxel.KEY_SPACE):
                #初期化する
                pyxel.play(0, 3)
                self.day = 0
                self.hp = 100
                self.log = ["start!"]
                for i in range(0, len(self.status)):
                    self.status[i].sta = 0
                self.gamestatus = 0


    def draw(self):
        pyxel.cls(6)
        if self.gamestatus == 0:
            pyxel.blt(100,80,0,0,0,205,255)
            pyxel.blt(165,120,0,215,5,11,24)
            pyxel.blt(195,120,0,215,5,11,24)

            pyxel.blt(205,40,1,63,160,190,31)

            pyxel.blt(340,85,1,160,48,93,24)
            for j in range(0, 3):
                pyxel.circ(374 + j * 80, 154, 35, 7)
                pyxel.blt(350 + j * 80,130,1,48 + 48 * j,192,48,48)
            pyxel.blt(340,192,1,0,112,136,16)

            pyxel.circ(374, 262, 35, 7)
            pyxel.blt(350,240,1,0,192,48,48)
            pyxel.blt(340,300,1,145,112,104,16)
            pyxel.blt(338,320,2,138,0,115,32)
            pyxel.text(250,400,"PRESS SPACE TO START",0)

        elif self.gamestatus == 1:
            #ボタンの描画
            for i in range(0, len(self.command)):
                pyxel.circ(150 + i * 100, 390, 40 + self.command[i].radius, 7)
            #HPの表示
            pyxel.rect(19,169,102,32,7)
            pyxel.rect(20,170,self.hp,30,11)
            #ステータスの表示
            for j in range(0, len(self.status)):
                pyxel.rect(459,59  + j * 80,102,37,7)
                pyxel.rect(460,60 + j * 80,self.status[j].sta,35,3)

            #猫の描写
            pyxel.blt(200,80,0,0,0,205,255)
            pyxel.blt(265,120,0,215,5,11,24)
            pyxel.blt(295,120,0,215,5,11,24)


            if self.catstatus == 1:
                pyxel.blt(self.itemmove.x,self.itemmove.y,2,96,0,32,32)
            elif self.catstatus == 2:
                pyxel.blt(self.itemmove.x,self.itemmove.y,2,0,0,32,32)
            elif self.catstatus == 3:
                pyxel.blt(self.itemmove.x,self.itemmove.y,2,32,0,32,32)
            elif self.catstatus == 4:
                pyxel.blt(self.itemmove.x,self.itemmove.y,2,64,0,32,32)

            #日数の描写
            if self.day <= 5:
                pyxel.blt(20,50,1,0 + self.day * 40,0,40,40)
            else:
                pyxel.blt(20,50,1,0 + (self.day - 6) * 40,40,40,40)
            pyxel.blt(70,60,1,0,161,64,30)

            #ステータス欄とコマンドの描写
            pyxel.blt(18,123,1,129,128,104,32)
            pyxel.blt(460,27,1,0,80,100,30)
            pyxel.blt(460,107,1,105,80,100,30)
            pyxel.blt(460,187,1,0,128,96,30)
            for j in range(0, 4):
                pyxel.blt(125 + j * 100,367,1,0 + 48 * j,192,48,48)

            #ログの表示
            for h in range(0, len(self.log)):
                pyxel.text(20,220 + h * 7,self.log[h],0)

        elif self.gamestatus == 2:
            pyxel.text(280,100,"END",0)
            pyxel.blt(100,80,0,0,0,205,255)

            if self.status[0].sta+self.status[1].sta+self.status[2].sta < 108:
                pyxel.blt(160,127,0,207,96,24,24)
                pyxel.blt(195,127,0,207,64,24,32)
                pyxel.blt(380,60,2,0,32,104,40)
                pyxel.text(410,150,"MOVE SOME MORE",0)
            elif (self.status[0].sta == 100):
                pyxel.blt(197,130,0,207,29,24,15)
                pyxel.blt(157,130,0,207,45,24,15)
                pyxel.blt(360,60,2,0,72,200,40)
                pyxel.text(410,150,"VERY STRONG CAT",0)
            elif (self.status[1].sta == 100):
                pyxel.blt(197,130,0,207,29,24,15)
                pyxel.blt(157,130,0,207,45,24,15)
                pyxel.blt(370,60,2,0,112,168,40)
                pyxel.text(410,150,"VERY BEAUTIFUL CAT",0)
            elif (self.status[2].sta == 100):
                pyxel.blt(197,130,0,207,29,24,15)
                pyxel.blt(157,130,0,207,45,24,15)
                pyxel.blt(360,60,2,0,152,200,40)
                pyxel.text(410,150,"VERY CLEVER CAT",0)
            elif self.status[0].sta+self.status[1].sta+self.status[2].sta > 186:
                pyxel.blt(197,130,0,207,29,24,15)
                pyxel.blt(157,130,0,207,45,24,15)
                pyxel.blt(370,60,2,0,192,208,40)
                pyxel.text(410,150,"THE VERSATILE CAT",0)
            else:
                pyxel.blt(165,120,0,215,5,11,24)
                pyxel.blt(195,120,0,215,5,11,24)
                pyxel.blt(370,60,2,128,32,120,40)
                pyxel.text(410,150,"TAKE IT EASY",0)

            pyxel.text(250,400,"PRESS SPACE TO RESTART",0)

App()
