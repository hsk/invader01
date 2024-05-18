#!/usr/bin/env python
#coding: utf-8
import pygame,os,random,sys
from pygame.locals import *
from api.util import *
from weapon import *

SCR_RECT = Rect(0, 0, 640, 480)
class App:
    def __init__(self,caption,scene,inits=[]):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(caption)
        # 素材のロード
        for p in inits: p.init()
        # ゲームオブジェクトを初期化
        self.init_scene = scene
        self.init_game()
        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            scene = self.scene
            scene.update(self)
            screen.fill((0, 0, 0))
            scene.draw(self, screen)
            pygame.display.update()
            self.key_handler()
    def init_game(self,scene=None):
        """ゲームオブジェクトを初期化"""
        # ゲーム状態
        self.scene = self.init_scene
    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                self.scene.keydown(self,event)
class Invader(App):
    def init_game(self):
        """ゲームオブジェクトを初期化"""
        # ゲーム状態
        self.scene = self.init_scene
        # スプライトグループを作成して登録
        self.all = pygame.sprite.RenderUpdates()
        self.aliens = pygame.sprite.Group()  # エイリアングループ
        self.shots = pygame.sprite.Group()   # ミサイルグループ
        self.beams = pygame.sprite.Group()   # ビームグループ
        # デフォルトスプライトグループを登録
        Player.containers = self.all
        Weapon.containers = self.all, self.shots
        Alien.containers = self.all, self.aliens
        Beam.containers = self.all, self.beams
        Explosion.containers = self.all
        # 自機を作成
        self.player = Player()
        # エイリアンを作成
        for i in range(0, 50):
            x = 20 + (i % 10) * 40
            y = 20 + int(i / 10) * 40
            Alien((x,y))

# ゲーム状態
class Start:
    def update(g):
        pass
    def keydown(g,event):
        if event.key == K_SPACE:
            g.scene = Play
    def draw(g,screen):
        # タイトルを描画
        title_font = pygame.font.SysFont(None, 80)
        title = title_font.render("INVADER GAME", False, (255,0,0))
        screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 100))
        # エイリアンを描画
        alien_image = Alien.images[0]
        screen.blit(alien_image, ((SCR_RECT.width-alien_image.get_width())/2, 200))
        # PUSH STARTを描画
        push_font = pygame.font.SysFont(None, 40)
        push_space = push_font.render("PUSH SPACE KEY", False, (255,255,255))
        screen.blit(push_space, ((SCR_RECT.width-push_space.get_width())/2, 300))
        # クレジットを描画
        credit_font = pygame.font.SysFont(None, 20)
        credit = credit_font.render(u"2008 http://pygame.skr.jp", False, (255,255,255))
        screen.blit(credit, ((SCR_RECT.width-credit.get_width())/2, 380))

class Play:
    def update(g):
        g.all.update()
        # ミサイルとエイリアンの衝突判定
        Play.collision(g)
        # エイリアンをすべて倒したらゲームオーバー
        if len(g.aliens.sprites()) == 0:
            g.scene = Gameover
    def collision(g):
        """衝突判定"""
        # エイリアンとミサイルの衝突判定
        alien_collided = pygame.sprite.groupcollide(g.aliens, g.shots, True, True)
        for alien in alien_collided.keys():
            Alien.kill_sound.play()
            Explosion(alien.rect.center)  # エイリアンの中心で爆発
        # プレイヤーとビームの衝突判定
        beam_collided = pygame.sprite.spritecollide(g.player, g.beams, True)
        if beam_collided:  # プレイヤーと衝突したビームがあれば
            Player.bomb_sound.play()
            g.scene = Gameover  # ゲームオーバー！
    def keydown(g,event):
        pass
    def draw(g,screen):
        g.all.draw(screen)

class Gameover:
    def update(g):
        pass
    def keydown(g,event):
        if event.key == K_SPACE:
            g.init_game()  # ゲームを初期化して再開
            g.scene = Start
    def draw(g,screen):
        # GAME OVERを描画
        gameover_font = pygame.font.SysFont(None, 80)
        gameover = gameover_font.render("GAME OVER", False, (255,0,0))
        screen.blit(gameover, ((SCR_RECT.width-gameover.get_width())/2, 100))
        # エイリアンを描画
        alien_image = Alien.images[0]
        screen.blit(alien_image, ((SCR_RECT.width-alien_image.get_width())/2, 200))
        # PUSH STARTを描画
        push_font = pygame.font.SysFont(None, 40)
        push_space = push_font.render("PUSH SPACE KEY", False, (255,255,255))
        screen.blit(push_space, ((SCR_RECT.width-push_space.get_width())/2, 300))
   
class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 5  # 移動速度
    reload_time = 15  # リロード時間
    def init():
        Player.image = load_image("player.png")
        Player.shot_sound = load_sound("shot.wav")
        Player.bomb_sound = load_sound("bomb.wav")
    def __init__(self):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom  # プレイヤーが画面の一番下
        self.reload_timer = 0
        self.shot = 0
        self.reload_shot = 0
    def update(self):
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if self.reload_shot > 0:
            self.reload_shot -= 1
        elif pressed_keys[K_x]:
            self.shot += 1
            self.reload_shot = self.reload_time
            if self.shot >= len(Weapon.shots):
                self.shot = 0
        self.rect.clamp_ip(SCR_RECT)
        # ミサイルの発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                Player.shot_sound.play()
                Weapon.create(Weapon.shots[self.shot], self.rect.center)  # 作成すると同時にallに追加される
                self.reload_timer = self.reload_time

class Alien(pygame.sprite.Sprite):
    """エイリアン"""
    speed = 2  # 移動速度
    animcycle = 18  # アニメーション速度
    frame = 0
    move_width = 230  # 横方向の移動範囲
    prob_beam = 0.005  # ビームを発射する確率
    def init():
        Alien.images = split_image(load_image("alien.png"), 2)
        Alien.kill_sound = load_sound("kill.wav")
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]  # 移動できる左端
        self.right = self.left + self.move_width  # 移動できる右端
    def update(self):
        # 横方向への移動
        self.rect.move_ip(self.speed, 0)
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed
        # ビームを発射
        if random.random() < self.prob_beam:
            Beam(self.rect.center)
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle)%2]


class Beam(pygame.sprite.Sprite):
    """エイリアンが発射するビーム"""
    speed = 5  # 移動速度
    def init():
        Beam.image = load_image("beam.png")
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(0, self.speed)  # 下へ移動
        if self.rect.bottom > SCR_RECT.height:  # 下端に達したら除去
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """爆発エフェクト"""
    animcycle = 2  # アニメーション速度
    frame = 0
    def init():
        Explosion.images = load_images("explosion.png",16)
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle  # 消滅するフレーム
    def update(self):
        # キャラクターアニメーション
        self.image = self.images[int(self.frame/self.animcycle)]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()  # 消滅

if __name__ == "__main__":
    Invader("Invader",Start,[Player,Alien,Beam,Explosion,Weapon])
