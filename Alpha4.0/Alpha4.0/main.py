import pygame, sys, copy, random
import comp, func, enemy, graph
import story0, story1, story2
from pygame.locals import *
from global_var import *

FPS = 60
GAMETIME = 60 #  单位:秒
ACTIVE_KEY = ['e', 'w', 's', 'd', 'a', 'u', 'i', 'j', 'k']
REFL_KEY = ['l', 'o']

def main():
        mode = 0        #mode为0代表主界面，1代表战斗界面
        menuopt = 1     #1故事模式，2玩法教程，3关于我们，4退出游戏
        is_pause = False
        is_end = False
        is_attack = False
        story = 0
        storytime = 0
        tut_ret = 0
        
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("赋和韩树(Version:Alpha)")


        bgd_image = pygame.image.load("bgd800.png").convert_alpha(screen)
        sbd_image = pygame.image.load("sbd800.png").convert_alpha(screen)
        pause_image = pygame.image.load("pause800.png").convert_alpha(screen)
        end_image = pygame.image.load("end800.png").convert_alpha(screen)
        about_image = pygame.image.load("abt800.png").convert_alpha(screen)
        mis_image = pygame.image.load("mis800.png").convert_alpha(screen)
        background = pygame.Surface((WIDTH, HEIGHT))
        background.blit(bgd_image,(0,0))
        pauseopts = pygame.Surface((WIDTH, HEIGHT))
        pauseopts.blit(pause_image,(0,0))
        endopts = pygame.Surface((WIDTH, HEIGHT))
        endopts.blit(end_image,(0,0))
        startboard = pygame.Surface((WIDTH, HEIGHT))
        startboard.blit(sbd_image,(0,0))
        screen.blit(startboard,(0,0))
        
        bgdmask = pygame.Surface((WIDTH, HEIGHT))
        bgdmask.fill((0,127,63))
        bgdmask.set_alpha(63)
        tempbgd = pygame.Surface((WIDTH, HEIGHT))

        lastblit = True
        
        opterL = graph.Opter(530-OPTWIDTH,530,278)
        opterR = graph.Opter(660,660+OPTWIDTH,278)
        opting = True
        startboard_option = 1
        pause_option = 1
        end_option = 1

        mistime = 0
        miskey = False

        pygame.mixer.init()
        track = pygame.mixer.music.load("stress.mp3")
        pygame.mixer.music.play(-1)
        track1 = pygame.mixer.Sound("metal.ogg")
        
        while True:
                if mode == -1:  #故事模式剧情
                        mistime += 1
                        pygame.display.flip()
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == KEYDOWN:
                                        miskey = True
                        if miskey == True or mistime == 1000:
                                screen.blit(background,(0,0))
                                FH = comp.Comp()
                                costbar = graph.initialize()
                                mode = 1
                                story = 2
                                graph.HP=graph.FULLHP
                                graph.MP=graph.FULLMP
                                func.stream=[]
                                storytime = 0
                                is_pause = False
                                opting = False
                if mode == 0:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == KEYDOWN:
                                        if event.key == K_SPACE:
                                                if startboard_option == 1:
                                                        screen.blit(mis_image,(0,0))
                                                        mode = -1
                                                        mistime = 0
                                                        miskey = False
                                                elif startboard_option == 2:
                                                        screen.blit(background,(0,0))
                                                        FH = comp.Comp()
                                                        costbar = graph.initialize()
                                                        mode = 1
                                                        story = 1
                                                        graph.HP=graph.FULLHP
                                                        graph.MP=graph.FULLMP
                                                        func.stream=[]
                                                        storytime = 0
                                                        is_pause = False
                                                        opting = False
                                                elif startboard_option == 3:
                                                        screen.blit(about_image,(0,0))
                                                elif startboard_option == 4:
                                                        pygame.quit()
                                                        sys.exit()
                                                track1.play()
                                        elif pygame.key.name(event.key) == 'down':
                                                if startboard_option < 4:
                                                        screen.blit(startboard,(0,0))
                                                        startboard_option += 1
                                                        graph.opt(opterL,opterR,opterL.l2,opterR.l1, 216 + 62*startboard_option)
                                        elif pygame.key.name(event.key) == 'up':
                                                if startboard_option > 1:
                                                        screen.blit(startboard,(0,0))
                                                        startboard_option -= 1
                                                        graph.opt(opterL,opterR,opterL.l2,opterR.l1, 216 + 62*startboard_option)


                        if opting and mode == 0:
                                opterL.color = (0,0,0)
                                opterR.color = (0,0,0)
                                opterL.update(screen, startboard)
                                opterR.update(screen, startboard)
                                
                        pygame.display.flip()
                        
                        FPSCLOCK.tick(FPS)
                
                elif mode == 1:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                elif opting and event.type == KEYDOWN:
                                        if event.key == K_SPACE:
                                                if pause_option == 1:
                                                        background = pygame.Surface.copy(tempbgd)
                                                        screen.blit(background,(0,0))
                                                        is_pause = False
                                                        opting = False
                                                elif pause_option == 2:
                                                        for arbi in enemy.enemies:
                                                                arbi.kill()
                                                        for arbi in graph.bar:
                                                                arbi.kill()
                                                        for arbi in graph.curve:
                                                                arbi.kill()
                                                        graph.dots=[]
                                                        costbar = graph.initialize()
                                                        background.fill((0,0,0))
                                                        background.blit(bgd_image,(0,0))
                                                        screen.blit(background,(0,0))
                                                        graph.HP=graph.FULLHP
                                                        graph.MP=graph.FULLMP
                                                        func.stream=[]
                                                        storytime=0
                                                        is_end = False
                                                        is_pause = False
                                                        opting = False
                                                elif (not is_end and pause_option == 4) or (is_end and pause_option == 3):
                                                        for arbi in enemy.enemies:
                                                                arbi.kill()
                                                        for arbi in graph.bar:
                                                                arbi.kill()
                                                        for arbi in graph.curve:
                                                                arbi.kill()
                                                        graph.dots=[]
                                                        FH.kill()
                                                        mode=0
                                                        graph.HP=graph.FULLHP
                                                        graph.MP=graph.FULLMP
                                                        func.stream=[]
                                                        storytime=0
                                                        background.fill((0,0,0))
                                                        background.blit(bgd_image,(0,0))
                                                        screen.blit(startboard,(0,0))
                                                        is_end = False
                                                        lastblit = True
                                                        startboard_option = 1
                                                        pause_option = 1
                                                        graph.opt(opterL,opterR,530,660, 216 + 62*startboard_option)
                                                track1.play()
                                        elif pygame.key.name(event.key) == 'down':
                                                if (not is_end and pause_option < 4) or (is_end and pause_option < 3):
                                                        pause_option += 1
                                        elif pygame.key.name(event.key) == 'up':
                                                if (not is_end and pause_option > 1) or (is_end and pause_option > 2):
                                                        pause_option -= 1
                                elif event.type == KEYDOWN and story == 1 and event.key == K_RETURN:
                                        if story1.ret != 2 and story1.ret//2 == story1.ret/2: story1.ret += 1
                                elif event.type == KEYDOWN and event.key == K_q:
                                        is_pause = True
                                        tempbgd = pygame.Surface.copy(background)
                                        bgdmask.fill((0,127,63))
                                        background.blit(bgdmask,(0,0))
                                        screen.blit(background,(0,0))
                                        lastblit = False
                                        pause_option = 1
                                elif not is_pause:
                                        if event.type == KEYDOWN:
                                                if event.key == K_b:
                                                        func.clear()
                                                        func.reflect(func.reflx, func.refly)
                                                        graph.reset(costbar)
                                                elif event.key == K_SPACE and (costbar.r-costbar.l)/(WIDTH*0.4) * graph.FULLMP < graph.MP:
                                                        graph.MP -= (costbar.r-costbar.l)/(WIDTH*0.4) * graph.FULLMP
                                                        graph.cast_shadow()
                                                        is_attack = True
                                                        func.clear()
                                                        func.reflect(func.reflx, func.refly)
                                                        graph.reset(costbar)
                                                        track1.play()
                                                elif pygame.key.name(event.key) in ACTIVE_KEY:
                                                        temp = copy.deepcopy(func.stream)
                                                        func.reflect(False, False)
                                                        func.complex(pygame.key.name(event.key))
                                                        func.simp_stream()
                                                        func.reflect(func.reflx, func.refly)
                                                        if func.consume() >= graph.FULLMP:
                                                                func.stream = temp
                                                        graph.reset(costbar)
                                                elif pygame.key.name(event.key) in REFL_KEY:
                                                        if pygame.key.name(event.key) == 'o':
                                                                func.refly = not func.refly
                                                        elif pygame.key.name(event.key) == 'l':
                                                                func.reflx = not func.reflx
                                                        func.simp_stream()
                                                        func.reflect(func.reflx, func.refly)
                                                        graph.reset(costbar)
                        
                        hit_FH = pygame.sprite.spritecollide(FH, enemy.enemies, True)
                        for i in hit_FH:
                                graph.HP -= 18
                                
                        if is_attack == True:
                                hit_ord_enemies = pygame.sprite.groupcollide(enemy.ord_enemies, graph.sights, True, False)
                                hit_heal_enemies = pygame.sprite.groupcollide(enemy.heal_enemies, graph.sights, False, False)
                                for each in hit_heal_enemies:
                                        if len(hit_heal_enemies[each]) > 0:
                                                each.hit_times += 1
                                hit_split_enemies = pygame.sprite.groupcollide(enemy.split_enemies, graph.sights, True, False)
                                for each in hit_split_enemies:
                                        if len(hit_split_enemies[each]) > 0:
                                                for i in range(0,4):
                                                        enemy.PartiEne(graph.lof(each.x), graph.tof(each.y), 6, -45+i*30)
                                                        each.kill()
                                is_attack = False

                        if not is_pause or not lastblit:
                                enemy.enemies.clear(screen, background)
                                graph.expr_clear(screen, background)
                        
                        if not is_pause:
                        
                                if story == 1:        #第一章-教程
                                        story1.happen(storytime, background, screen, costbar)
                                        FST=story1.FULLSTORYTIME
                                elif story == 2:        #第二章-故事模式
                                        story2.happen(storytime, background, screen)
                                        FST=story2.FULLSTORYTIME
                                
                                if graph.HP <= 0 or storytime >= FST:
                                        if graph.HP <= 0:
                                                graph.HP = 0
                                                bgdmask.fill((191,0,0))
                                        elif storytime >= FST:
                                                bgdmask.fill((255,239,127))
                                        background.blit(bgdmask,(0,0))
                                        screen.blit(background,(0,0))
                                        is_pause = True
                                        is_end = True
                                        pause_option = 2
                                        lastblit = False
                                        
                                if story != 1 or (story == 1 and storytime == 0): storytime += 1
                                elif story == 1 and story1.ret >= 9: storytime = FST
                                        
                                graph.percent = storytime/FST
                                
                                graph.status_update(storytime,FST)
                                if graph.graphdelay < graph.FULLGRAPHDELAY:
                                        graph.graphdelay += 1
                                if graph.domaindelay < graph.FULLDOMAINDELAY:
                                        graph.domaindelay += 1
                                for d in graph.dots:
                                        d.update()
                                                                
                                graph.sights.update()
                                graph.shadows.update(screen, background)
                                graph.bar.update()
                                enemy.enemies.update()

                        if not is_pause or not lastblit:
                                graph.plot_curve(screen, background, graph.curve)
                                enemy.enemies.draw(screen)
                                graph.plot_bar(screen, background, graph.bar)
                                graph.expr_draw(screen, background)
                                graph.opt(opterL,opterR,342,458, 197 + 66*pause_option)
                                lastblit = True
                                
                        if mode == 0: screen.blit(startboard,(0,0))
                                
                        if is_pause and not is_end and not opting:
                                screen.blit(pause_image,(0,0))
                                opting = True
                        elif is_pause and is_end and not opting:
                                screen.blit(end_image,(0,0))
                                opting = True

                        if opting and mode == 1:
                                opterL.color = (255,255,255)
                                opterR.color = (255,255,255)
                                graph.opt(opterL,opterR,opterL.l2,opterR.l1, 132 + 66*pause_option)
                                opterL.update(screen, background)
                                opterR.update(screen, background)

                                
                        pygame.display.flip()
                
                        FPSCLOCK.tick(FPS)
                
if __name__ == '__main__':
        main()
