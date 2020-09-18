import pygame, random, graph
from math import *
from global_var import *

common_speed = 0.002
ord_enemies = pygame.sprite.Group()
heal_enemies = pygame.sprite.Group()
split_enemies = pygame.sprite.Group()
enemies = pygame.sprite.Group()
YEllOW = (255, 255, 0)
GREEN = (0, 255, 0)

class Enemy(pygame.sprite.Sprite):
        def __init__(self, R):
                super().__init__()
                self.R = R
                self.image = pygame.Surface((2*R, 2*R))
                self.image.set_colorkey((0, 0, 0))
                self.rect = self.image.get_rect()
                self.color = (255,0,0)
                self.speed = 0
                self.angle = 0
                self.x = 0
                self.y = 0
                self.dx = 0
                self.dy = 0
        def update(self):
                if self.x == 0:
                        if self.y >= 0:
                                sita = pi/2
                        elif self.y <0:
                                sita = -pi/2
                else:
                        sita = atan(self.y/self.x)
                        if self.x < 0:
                                sita += pi
                self.dx = - self.speed * common_speed * cos(sita - radians(self.angle))
                self.dy = - self.speed * common_speed * sin(sita - radians(self.angle))
                self.x += self.dx
                self.y += self.dy
                self.rect.centerx = graph.lof(self.x)
                self.rect.centery = graph.tof(self.y)

class TutEne1(Enemy):
        def __init__(self, X, Y):
                super().__init__(12)
                self.color = YEllOW
                self.speed = 0
                self.angle = 0
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                self.rect.center = (graph.lof(X), graph.tof(Y))
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, ord_enemies])

class TutEne2(Enemy):
        def __init__(self, radius):
                super().__init__(12)
                self.color = GREEN
                self.radius = radius
                self.sita = random.randint(0, 360)
                self.add([enemies, ord_enemies])
        def update(self):
                self.sita += 1
                self.x = self.radius * cos(radians(self.sita))
                self.y = self.radius * sin(radians(self.sita))
                self.rect.center = (graph.lof(self.x), graph.tof(self.y))

class OrdinEne(Enemy):
        def __init__(self, direction):
                super().__init__(12)
                self.speed = 5
                self.angle = 20
                self.color = (191,191,191)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                if direction == 'U':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, 0)
                elif direction == 'D':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, HEIGHT)
                elif direction == 'L':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (0, pos)
                elif direction == 'R':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (WIDTH, pos)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, ord_enemies])

class SpikeEne(Enemy):
        def __init__(self, direction):
                super().__init__(10)
                self.speed = 10
                self.angle = 0
                self.color = (255,255,127)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                if direction == 'LU':
                        self.rect.center = (0, 0)
                elif direction == 'LD':
                        self.rect.center = (0, HEIGHT)
                elif direction == 'RU':
                        self.rect.center = (WIDTH, 0)
                elif direction == 'RD':
                        self.rect.center = (WIDTH, HEIGHT)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, ord_enemies])

class WeirdEne(Enemy):
        def __init__(self, direction):
                super().__init__(11)
                self.speed = 30
                self.angle = 75
                self.color = (127,215,255)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                if direction == 'U':
                        self.rect.center = (WIDTH/2, 0)
                elif direction == 'D':
                        self.rect.center = (WIDTH/2, HEIGHT)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, ord_enemies])

class HealEne(Enemy):
        def __init__(self, direction):
                super().__init__(13)
                self.speed = 3        #下面还有一处
                self.angle = 15
                self.color = (0,255,155)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                if direction == 'U':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, 0)
                elif direction == 'D':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, HEIGHT)
                elif direction == 'L':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (0, pos)
                elif direction == 'R':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (WIDTH, pos)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.hit_times = 0
                self.timer = 100
                self.add([enemies, heal_enemies])
        def update(self):
                super().update()
                if self.hit_times == 1:
                        self.timer -= 1
                        self.color = (int(2.55*self.timer),255,155+self.timer)
                        pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                        self.speed = 1
                if self.hit_times == 2:
                        self.kill()
                elif self.timer == 0:
                        self.hit_times = 0
                        self.timer = 100
                        self.speed = 3        #此处

class SplitEne(Enemy):
        def __init__(self, direction):
                super().__init__(11)
                self.speed = 4        #下面还有一处
                self.angle = 60
                self.color = (127,191,255)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                if direction == 'U':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, 0)
                elif direction == 'D':
                        pos = random.randint(0, WIDTH + 1)
                        self.rect.center = (pos, HEIGHT)
                elif direction == 'L':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (0, pos)
                elif direction == 'R':
                        pos = random.randint(0, HEIGHT + 1)
                        self.rect.center = (WIDTH, pos)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, split_enemies])

class PhantEne(Enemy):
        def __init__(self, r, theta):
                super().__init__(11)
                self.speed = 0
                self.angle = 0
                self.color = (255,255,255)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                self.x = r * cos(radians(theta))
                self.y = r * sin(radians(theta))
                self.rect.centerx = graph.lof(self.x)
                self.rect.centery = graph.tof(self.y)
                self.timer = 100
                self.add([enemies, ord_enemies])
        def update(self):
                super().update()
                if self.timer > 0:
                        self.timer -= 1
                        if self.timer >= 50:
                                self.color = (255,159+int(1.92*(self.timer-50)),135+int(2.4*(self.timer-50)))
                                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                elif self.timer <= 0:
                        PartiEne(graph.lof(self.x), graph.tof(self.y), 2, 0)
                        r = pow(self.x*self.x + self.y*self.y, 0.5)
                        theta = random.randint(0, 360)
                        self.x = r * cos(radians(theta))
                        self.y = r * sin(radians(theta))
                        self.rect.centerx = graph.lof(self.x)
                        self.rect.centery = graph.tof(self.y)
                        self.timer = 100
        

class PartiEne(Enemy):
        def __init__(self, posX, posY, spd, ang):
                super().__init__(11)
                self.speed = spd
                self.angle = ang
                self.color = (191,223,255)
                pygame.draw.circle(self.image, self.color, (self.R, self.R), self.R)
                self.rect = self.image.get_rect()
                self.rect.center = (posX, posY)
                self.x = graph.xof(self.rect.centerx)
                self.y = graph.yof(self.rect.centery)
                self.add([enemies, ord_enemies])
