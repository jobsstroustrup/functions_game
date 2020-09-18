import pygame, enemy, random, graph, func, copy
from math import *
from global_var import *
from pygame.locals import *
FULLSTORYTIME=100    #不限时

ret = 0
image_rect = pygame.Rect(0, 0, WIDTH ,HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tut00 = pygame.image.load("tut00.png").convert_alpha(screen)
tut0 = pygame.image.load("tut0.png").convert_alpha(screen)
tut1 = pygame.image.load("tut1.png").convert_alpha(screen)
tut2 = pygame.image.load("tut2.png").convert_alpha(screen)
tut3 = pygame.image.load("tut3.png").convert_alpha(screen)
tut4 = pygame.image.load("tut4.png").convert_alpha(screen)
tut5 = pygame.image.load("tut5.png").convert_alpha(screen)
tut6 = pygame.image.load("tut6.png").convert_alpha(screen)
tut7 = pygame.image.load("tut7.png").convert_alpha(screen)
tut8 = pygame.image.load("tut8.png").convert_alpha(screen)
tut9 = pygame.image.load("tut9.png").convert_alpha(screen)
tut10= pygame.image.load("tut10.png").convert_alpha(screen)
tut11= pygame.image.load("tut11.png").convert_alpha(screen)
tut12= pygame.image.load("tut12.png").convert_alpha(screen)
tut13= pygame.image.load("tut13.png").convert_alpha(screen)      #打字那个我不会换行，就把字和背景做成一张图片作为背景
tut14 = pygame.image.load("tut14.png").convert_alpha(screen)     # 每过一关换一个背景

big=[[tut0,'l',';',0,-4,1,0,3,1,7,2],
         [tut1,'e',';',-6,0,0,1,1,3,1.8,5],
         [tut2,'a',';',1,1],
         [tut3,'s',';',-7,-1,-6,0,-5,1,-3,0,-1,-1,2,1,4,-1,6.5,0,5],
         [tut4,'d',';',-6,0,-1,-1,0,-5,0.5,3,3,0.5,7,0],
         [tut5,'s','*',';',-7.7,-2,-5.5,1,-3,-0.25,-1.5,-1.9,0.25,1,3.5,-1,6.5,0.75],
         [tut6,'s','*',';',-7,-1,-4.5,0,-1.5,-0.5,0.5,0.5,3,-0.75,6,-0.5,7.7,0.5],
         [tut7,'s','/',';',-7,-0.4,-4,0.4,-1,-0.5,3,0,5,-0.6],
         [tut8,'s','/',';',-6,0,-3.5,-1,1,0.5,7,-0.5],
         [tut9,'e',';',6,0,0,-1,-1,-3,-1.8,-5]]        #这个是前十关的设置，第一个是背景图片，然后是按键，然后是分隔符号，
                                                           # 然后是怪的坐标

def tutorial (surface, scr, num, cbar):
        global iii, xx
        mid = big[num]
        temp = copy.deepcopy(func.stream)
        func.stream = []
        while iii<len(mid):
                j=mid.index(';')
                if iii == 0:
                        surface.blit(mid[iii], image_rect)        #贴背景
                        scr.blit(surface,(0,0))
                elif iii>0 and iii<j:
                        func.stream.append(mid[iii])              #根据按键设置蓝
                elif iii==j:
                        graph.MP = func.consume()+0.1
                        func.stream = temp                      #分隔符号
                        func.reflect(False, False)
                        func.reflx = False
                        func.refly = False
                        graph.reset(cbar)
                elif iii>j:
                        if (iii-j)%2==1:
                                xx=mid[iii]
                        else:
                                y=mid[iii]
                                enemy.TutEne1(xx,y)                  #设置怪的位置
                iii += 1

def judge (surface, scr):                                       #判断怪是否死光的函数
        if len(enemy.enemies)==0:
                return 0
        elif graph.MP <= func.bas_cons:                      #这行类型出问题
                return 1
        else: return 2

def happen (storytime, surface, scr, cbar):
        global ii, iii, xx, jud, ret
        t=storytime
        if t==0:
                print("i")
                ii = -1
                ret = 0
                jud = 0
                graph.dMP = 0
                graph.MP=0
                surface.blit(tut00,image_rect)         #先贴第一张图简介
                scr.blit(surface,(0,0))
        if ret == 1:    #回车继续
                ret += 1
        if ret == 2:
                if jud == 1:
                        iii = 0
                        tutorial(surface, scr, ii, cbar)
                jud = judge(surface, scr)
                if jud == 0:
                        if ii<len(big)-1:
                                ii += 1                #前十关基本按键操作
                                iii = 0
                                tutorial(surface, scr, ii, cbar)
                        elif ii>=len(big)-1:
                                ret += 1
                                surface.blit(tut10,image_rect)        #介绍arc的妙用，玩家自己感受，回车继续
                                scr.blit(surface,(0,0))
                elif jud == 1:
                        surface.blit(tut14,image_rect)
                        scr.blit(surface,(0,0))
                        ret = 0
        elif ret == 3:
                graph.dMP = 1
                ret += 1.5
                surface.blit(tut11,image_rect)     #介绍e,ln,1/x配合uijk的用法，回车继续
                scr.blit(surface,(0,0))
                for i in range(1,8):
                        for j in range(1,6):
                                enemy.TutEne1(i,j)
                                enemy.TutEne1(i,-j)
                                enemy.TutEne1(-i,-j)
        elif ret == 4.5:
                if len(enemy.enemies)==0: ret+= 0.5
        elif ret == 5:
                ret += 1
                surface.blit(tut12,image_rect)     #介绍一些杀伤力强的复合函数，回车继续
                scr.blit(surface,(0,0))
        elif ret == 7:
                ret += 1
                surface.blit(tut13,image_rect)     #介绍怪
                scr.blit(surface,(0,0))


'''
以下是修改之前的代码
pygame.font.init()
text = pygame.font.Font("STHeiti Medium.ttc", int(HEIGHT * 0.03))
text_rect = pygame.Rect(WIDTH*0.05, HEIGHT*0.15, WIDTH*0.8 ,HEIGHT*0.8)
def happen(storytime, surface, bgd):
        t = storytime
        if t == 0:
                graph.dMP = 1
        elif t//200==t/200:
                enemy.TutEne1(random.choice([-3,-2,-1,1,2,3]),random.choice([-2,-1,1,2]))
        
        
        surface.blit(bgd,text_rect,text_rect)
        text_surf = text.render("教程", True, (255,255,255))
        surface.blit(text_surf, text_rect)
'''
