#graph的用途：控制并记录MP、HP、percent、cost、以及所有非enemy的绘图
import pygame, func, random, comp
from global_var import *

FULLGRAPHDELAY = 10
FULLDOMAINDELAY = 10
graphdelay = FULLGRAPHDELAY
domaindelay = FULLDOMAINDELAY

dots = []
NUMDOT = 100	#原点左右各设置100个Dot

FULLMP=100
FULLHP=100
MP=100
dMP=0
HP=100
percent=0

FULLLAST = 100	#残影时间为50帧

sight_color=(191,191,191)
mpbar_color=(63,191,239)
hpbar_color=(239,0,0)
percbar_color=(127,239,239)
costbar_color=(191,239,255)
expr_color=(255,63,63)
opter_color=(0,0,0)
class good_color():
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
shadow_attack_color=good_color(63,207,255)
shadow_transit_color=good_color(255,255,127)
shadow_fade_color=good_color(223,0,0)
shadow_appear_color=good_color(255,127,127)
def color_of(good_color):
	return (good_color.r, good_color.g, good_color.b)

curve = pygame.sprite.Group()
bar = pygame.sprite.Group()
sights = pygame.sprite.Group()
shadows = pygame.sprite.Group()
opters = pygame.sprite.Group()
optshadows = pygame.sprite.Group()

pygame.font.init()
expr = pygame.font.Font("Futura.ttc", int(HEIGHT * 0.03))
expr_rect = pygame.Rect(WIDTH*0.55, HEIGHT*0.08125, WIDTH*0.45 ,HEIGHT*0.05)

class closer_0(Exception):	#定义错误类型
	pass
class Dot_not_exist(Exception):
	pass

#数学实现
def lof(x):
	return (8+x)/16 * WIDTH
def tof(y):
	return (6-y)/12 * HEIGHT
def xof(l):
	return l/WIDTH * 16 - 8
def yof(t):
	return 6 - t/HEIGHT * 12
def sgn(d):
	if d>0:
		return 1
	elif d<0:
		return -1
	elif d==0:
		return 0
def closer(n):
	if n==0:
		raise closer_0	#抛出错误
	return sgn(n) * (abs(n)-1)

def randcolor(is_good):
	randpos = [0,0,0]
	gcolor = good_color(0,0,0)
	while randpos[0] == randpos[1]:
		randpos = [random.randint(1,3),random.randint(1,3),random.randint(1,3)]
	if randpos[0] == 1: gcolor.r = 255
	elif randpos[0] == 2: gcolor.g = 255
	elif randpos[0] == 3: gcolor.b = 255
	if randpos[1] == 1: gcolor.r = random.randint(0,255)
	elif randpos[1] == 2: gcolor.g = random.randint(0,255)
	elif randpos[1] == 3: gcolor.b = random.randint(0,255)
	if randpos[2] == 1: gcolor.r = 0
	elif randpos[2] == 2: gcolor.g = 0
	elif randpos[2] == 3: gcolor.b = 0
	if is_good:
		return gcolor
	elif not is_good:
		return color_of(gcolor)
		
#控制MP、HP、percent、cost
def status_update(t,FST):
	global MP
	if MP+dMP<FULLMP:
		MP += dMP
	percent = t/FST

#绘图与创建攻击判定for s in sights: s.rect
class Dot():
	def __init__(self, index):
		self.index = index	#从-NUMDOT到NUMDOT的整数
		self.l = lof(10*pow(abs(index/NUMDOT),1.5)*sgn(index))
		self.t = tof(xof(self.l))
		self.exist = True
		self.depa = self.t
		self.dest = self.t
	def reset(self):
		try:	#不知道try怎么写
			if not self.exist:
				self.t = tof(func.calc(xof(self.l)))
				self.exist = True
				self.depa = self.t
				self.dest = self.t
			elif self.exist:
				self.depa = self.t
				self.dest = tof(func.calc(xof(self.l)))				
		except func.out_of_domain:	#不知道catch怎么写
			self.exist = False
			self.dest = self.depa
	def update(self):
		self.t = (1-graphdelay/FULLGRAPHDELAY) * self.depa + graphdelay/FULLGRAPHDELAY * self.dest
		if self.t <= -5000:
			self.t = -5000
		elif self.t >= HEIGHT+5000:
			self.t = HEIGHT+5000
	def at(index):		#不知道能不能这么写
		for d in dots:
			if d.index==index:
				return d
		raise Dot_not_exist	#抛出

class Plotter(pygame.sprite.Sprite):
	def __init__(self, l1, t1, l2, t2, w, color, groups):
		self.l1 = l1
		self.t1 = t1
		self.l2 = l2
		self.t2 = t2
		self.w = w
		self.color = color
		self.rect = pygame.Rect(min(l1,l2)-6, min(t1,t2)-6, abs(l2-l1)+12, abs(t2-t1)+12)
		super(Plotter, self).__init__()
		self.add(groups)

class Sight(Plotter):
	def __init__(self, index):
		self.color = sight_color
		super(Sight, self).__init__(Dot.at(index).l, Dot.at(index).t, Dot.at(closer(index)).l, Dot.at(closer(index)).t, 6, self.color, [curve, sights])
		self.index = index
		self.exist = True
		self.harmful = True
	def update(self):
		self.exist = Dot.at(self.index).exist and Dot.at(closer(self.index)).exist
		if self.harmful != self.exist:
			if (not self.harmful and abs(self.index) >= (1 - domaindelay/FULLDOMAINDELAY) * NUMDOT) or (self.harmful and abs(self.index) <= domaindelay/FULLDOMAINDELAY * NUMDOT):
				self.harmful = self.exist
				if not self.harmful:
					if abs(self.t1-self.t2) <= 100:
						Shadow(self, shadow_fade_color)
					self.t1 = -200
					self.t2 = -200
				elif self.harmful:
					self.t1 = Dot.at(self.index).t
					self.t2 = Dot.at(closer(self.index)).t
					if abs(self.t1-self.t2) <= 100:
						Shadow(self, shadow_appear_color)
		if self.harmful:
			self.t1 = Dot.at(self.index).t
			self.t2 = Dot.at(closer(self.index)).t
			
class Bar(pygame.sprite.Sprite):
	def __init__(self, l, t, r, b, color, groups):
		self.l = l
		self.t = t
		self.r = r
		self.b = b
		self.color = color
		super(Bar, self).__init__()
		self.rect =  pygame.Rect(l, t, r-l, b-t)
		self.add(groups)
		
class MpBar(Bar):
	def __init__(self):
		super(MpBar, self).__init__(WIDTH*0.05, HEIGHT*0.05, WIDTH*0.45, HEIGHT*0.075, mpbar_color, [bar])
	def update(self):
		self.l = self.r - WIDTH*0.4 * MP/FULLMP

class HpBar(Bar):
	def __init__(self):
		super(HpBar, self).__init__(WIDTH*0.55, HEIGHT*0.05, WIDTH*0.95, HEIGHT*0.075, hpbar_color, [bar])
	def update(self):
		self.r = self.l + WIDTH*0.4 * HP/FULLHP

class PercBar(Bar):
	def __init__(self):
		super(PercBar, self).__init__(WIDTH*0.05, HEIGHT*0.9375, WIDTH*0.95, HEIGHT*0.95, percbar_color, [bar])
	def update(self):
		self.r = self.l + WIDTH*0.9 * percent

class CostBar(Bar):
	def __init__(self):
		self.color = costbar_color
		super(CostBar, self).__init__(WIDTH*0.45 - func.bas_cons/FULLMP * WIDTH*0.4, HEIGHT*0.0875, WIDTH*0.45 , HEIGHT*0.1, self.color, [bar])
		self.depawidth =func.consume()/FULLMP * WIDTH*0.4
		self.destwidth =func.consume()/FULLMP * WIDTH*0.4
	def reset(self):
		self.depawidth = self.r - self.l
		self.destwidth = func.consume()/FULLMP * WIDTH*0.4
	def update(self):
		self.l = self.r - (1-graphdelay/FULLGRAPHDELAY) * self.depawidth - graphdelay/FULLGRAPHDELAY * self.destwidth

class Shadow(Plotter):
	def __init__(self, father, init_color):
		self.init_color = init_color
		self.color = (init_color.r, init_color.g, init_color.b)
		super(Shadow, self).__init__(father.l1, father.t1, father.l2, father.t2, 5, self.color, [curve, shadows])
		self.last = 0
		self.fade = random.choice([1,2,3])
		self.vc = random.choice([0,1,-1,2,-2])
	def update(self, surface, bgd):
		self.last = self.last + self.fade + random.choice([1,3,5])
		self.w = int(2 + 4 * (1 - self.last/FULLLAST))
		if self.last > FULLLAST:
			self.rect = pygame.Rect(self.rect.left-6, self.rect.top-6, self.rect.width+12, self.rect.height+12)
			surface.blit(bgd, self.rect, self.rect)
			self.kill()
			return
		vctemp = random.randint(-3,3)
		self.t1 = self.t1 + self.vc + vctemp + random.randint(-1,1)
		self.t2 = self.t2 + self.vc + vctemp + random.randint(-1,1)
		self.color = ( (1-self.last/FULLLAST) * self.init_color.r + self.last/FULLLAST * 255 , (1-self.last/FULLLAST) * self.init_color.g + self.last/FULLLAST * 255 , (1-self.last/FULLLAST) * self.init_color.b + self.last/FULLLAST * 255 )
def initialize():
	mpbar = MpBar()
	hpbar = HpBar()
	percbar = PercBar()
	costbar = CostBar()
	graphdelay = 0
	domaindelay = 0
	for i in range(-NUMDOT,NUMDOT+1):
		d=Dot(i)
		dots.append(d)
	for i in range(-NUMDOT,NUMDOT+1):
		if i != 0:
			Sight(i)
	return costbar

def reset(cbar):
	global graphdelay
	global domaindelay
	graphdelay = 0
	domaindelay = 0
	for d in dots:
		d.reset()
	cbar.reset()

def cast_shadow():
	is_static = True
	for d in dots:
		if d.exist and d.dest != d.depa:
			is_static = False
	if graphdelay == FULLGRAPHDELAY or is_static:
		for s in sights:
			if s.harmful:
				Shadow(s, shadow_attack_color)	
	elif graphdelay != FULLGRAPHDELAY and not is_static:
		for s in sights:
			if s.harmful:
				Shadow(s, shadow_transit_color)

def plot_curve(surface, bgd, plotter_group):
	for p in plotter_group:
		p.rect = pygame.Rect(p.rect.left-6, p.rect.top-6, p.rect.width+12, p.rect.height+12)
		surface.blit(bgd, p.rect, p.rect)
		p.rect = pygame.Rect(min(p.l1,p.l2), min(p.t1,p.t2), abs(p.l2-p.l1), abs(p.t2-p.t1))
	comp.fhs.clear(surface, bgd)
	for p in plotter_group:
		if p in sights:
			if p.harmful:
				pygame.draw.line(surface, p.color, (p.l1,p.t1), (p.l2,p.t2), p.w)
		elif p in shadows:
			pygame.draw.line(surface, p.color, (p.l1,p.t1), (p.l2,p.t2), p.w)
	comp.fhs.draw(surface)	

def plot_bar(surface, bgd, plotter_group):
	for p in plotter_group:
		surface.blit(bgd, p.rect, p.rect)
		p.rect = pygame.Rect(p.l, p.t, p.r-p.l, p.b-p.t)
	for p in plotter_group:
		pygame.draw.rect(surface, p.color, (p.l,p.t,p.r-p.l,p.b-p.t), 0)

def expr_clear(surface, bgd):
	surface.blit(bgd, expr_rect, expr_rect)

def expr_draw(surface, bgd):
	expr_surf = expr.render(func.make_expr(), True, expr_color)
	surface.blit(expr_surf, expr_rect)

class Opter(Plotter):
	def __init__(self, l, r, t):
		self.color = opter_color
		super(Opter, self).__init__(l, t, r, t, 4, self.color, [opters])
		self.rect = pygame.Rect(self.l1-4, self.t1-4, self.l2-self.l1+8, 8)
	def update(self, surface, bgd):
		surface.blit(bgd, self.rect, self.rect)
		self.rect = pygame.Rect(self.l1-4, self.t1-4, self.l2-self.l1+8, 8)
		pygame.draw.line(surface, self.color, (self.l1, self.t1), (self.l2, self.t2), 4)

def opt(oL, oR, left, right, top):
	oL.t1 = top
	oL.t2 = top
	oR.t1 = top
	oR.t2 = top
	oL.l1 = left - OPTWIDTH
	oL.l2 = left
	oR.l1 = right
	oR.l2 = right + OPTWIDTH








