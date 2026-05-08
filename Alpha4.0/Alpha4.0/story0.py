import pygame, enemy, random
FULLSTORYTIME=10000

def happen(storytime):
	t = storytime
	if t == 0:
		pass
	elif t != 0:
		if t//100==t/100:
			enemy.SpikeEne(random.choice(['LU', 'LD', 'RU', 'RD']))
