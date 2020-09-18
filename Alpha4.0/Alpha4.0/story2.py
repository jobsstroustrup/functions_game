import pygame, enemy, random, graph
FULLSTORYTIME=10000


def happen(storytime, surface, scr):
        t = storytime
        if t == 0:
                FULLSTORYTIME=12000
                graph.dMP = 0.2
        elif t <= 1000:
                if t//200 == t/200: enemy.OrdinEne(random.choice(['L', 'R', 'U', 'D']))
        elif t <= 2000:
                if t == 1100: enemy.SpikeEne(random.choice(['LU', 'LD', 'RU', 'RD']))
                if t == 1300: enemy.HealEne(random.choice(['L', 'R', 'U', 'D']))
                if t == 1500: enemy.WeirdEne(random.choice(['U', 'D']))
                if t == 1700: enemy.SplitEne(random.choice(['L', 'R', 'U', 'D']))
                if t == 1900: enemy.PhantEne(4, random.randint(0, 360))
        elif t <= 4000:
                if t//200 == t/200: enemy.OrdinEne(random.choice(['L', 'R', 'U', 'D']))
                if t//300 == t/300:
                        decision = random.randint(0,3)
                        if decision == 0: enemy.SpikeEne(random.choice(['LU', 'LD', 'RU', 'RD']))
                        elif decision == 1: enemy.HealEne(random.choice(['L', 'R', 'U', 'D']))
                        elif decision == 2: enemy.WeirdEne(random.choice(['U', 'D']))
        elif t <= 5000:
                if t//150 == t/150: enemy.SplitEne(random.choice(['L', 'R', 'U', 'D']))
        elif t <= 5500:
                pass
        elif t <= 7500:
                if t//200 == t/200: enemy.OrdinEne(random.choice(['L', 'R', 'U', 'D']))
                if t//250 == t/250:
                        decision = random.randint(0,5)
                        if decision == 0: enemy.SpikeEne(random.choice(['LU', 'LD', 'RU', 'RD']))
                        elif decision == 1: enemy.HealEne(random.choice(['L', 'R', 'U', 'D']))
                        elif decision == 2: enemy.WeirdEne(random.choice(['U', 'D']))
                        elif decision == 3: enemy.SplitEne(random.choice(['L', 'R', 'U', 'D']))
                        elif decision == 4: enemy.PhantEne(4, random.randint(0, 360))
        elif t <= 8750:
                if t == 8000:
                        enemy.PhantEne(5, 30)
                        enemy.PhantEne(5, 150)
                        enemy.PhantEne(5, 270)
        elif t <= 9500:
                if t == 9000:
                        enemy.SpikeEne('LU')
                        enemy.SpikeEne('LD')
                        enemy.SpikeEne('RU')
                        enemy.SpikeEne('RD')
                if t//200 == t/200:
                        enemy.WeirdEne('U')
                        enemy.WeirdEne('D')
                        enemy.PhantEne(3, random.randint(0, 360))
        else:
                if len(enemy.enemies)==0:
                        FULLSTORYTIME = t
                
