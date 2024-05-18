import pygame
from api.util import *
from weapon.shot import *
from weapon import Weapon
def Shot2(pos):
    Shot2a(pos,True)
    Shot2a(pos,False)
class Shot2a(pygame.sprite.Sprite):
    """プレイヤーが発射するミサイル"""
    speed = 9  # 移動速度
    def __init__(self, pos, xv=True):
        self.image = Shot.image
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, Weapon.containers)
        self.rect = self.image.get_rect()
        self.xv = (1 if xv else -1) * 8
        self.rect.center = (pos[0]+self.xv,pos[1])  # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()
Weapon.add_weapon("shot2",Shot2)
