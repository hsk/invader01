import pygame
from api.util import *
from weapon.shot import *
from weapon import Weapon
def Way2(pos):
    Way2a(pos,True)
    Way2a(pos,False)
class Way2a(pygame.sprite.Sprite):
    """プレイヤーが発射するミサイル"""
    speed = 9  # 移動速度
    speed2 = 2
    def __init__(self, pos, xv=True):
        self.image = Shot.image
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, Weapon.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
        self.xv = (1 if xv else -1) * self.speed2
    def update(self):
        self.rect.move_ip(self.xv, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()
Weapon.add_weapon("Way2",Way2)
