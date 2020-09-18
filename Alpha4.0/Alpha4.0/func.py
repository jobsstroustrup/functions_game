'''
改动：1.因为全部放在func.py文件下，所以所有''func_''部分省去，stream, expression作为这个文件下的全局变量。2.对键盘值的相应放在main.py里，所以对update_stream做了一些修改。3.加了consume()计算消耗
'''
import math

KEYDICT = {'e': 'L_e',  'w': 'L_l',  's': 'L_s',  'd': 'L_d',  'a': 'L_a',  'u': 'L_*',  'i': 'L_/',  'j': 'R_*',  'k': 'R_/'}
stream = []
bas_cons = 8
expression = ''
reflx = False
refly = False

class out_of_domain(Exception):
        pass

def clear():
        global stream
        stream = []

def complex(keytype):
        keyvalue = KEYDICT[keytype]
        if list(keyvalue)[0] == 'L':
                value = keyvalue[2:]
                stream.append(value)
        if list(keyvalue)[0] == 'R':
                value = keyvalue[2:]
                stream.insert(0, value)

def reflect(rx, ry):
        if len(stream) >= 2:
                if rx and stream[0] != '-':
                        stream.insert(0,'-')
                elif not rx and stream[0] == '-':
                        stream.pop(0)
                if ry and stream[len(stream)-1] != '-':
                        stream.append('-')
                elif not ry and stream[len(stream)-1] == '-':
                        stream.pop(len(stream)-1)
        elif len(stream) == 1 and stream[0] != '-':
                if rx:
                        stream.insert(0,'-')
                if ry:
                        stream.append('-')
        elif len(stream) == 1 and stream[0] == '-':
                if not rx and not ry:
                        stream.pop(0)
                if rx and ry:
                        stream.append('-')
        elif len(stream) == 0:
                if rx != ry:
                        stream.append('-')
                if rx and ry:
                        stream.append('-')
                        stream.append('-')

def simp_stream():
        i = 1
        while i < len(stream):
                if (stream[i-1] == '-') and (stream[i] == '-'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == '/') and (stream[i] == '*'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == '*') and (stream[i] == '/'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == 'a') and (stream[i] == 's'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == 's') and (stream[i] == 'a'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == 'd') and (stream[i] == 'd'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == 'l') and (stream[i] == 'e'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                elif (stream[i-1] == 'e') and (stream[i] == 'l'):
                        stream.pop(i-1)
                        stream.pop(i-1)
                i += 1

def calc(x):
        for let in stream:
                if let == '-':
                        x = -x
                elif let == '/':
                        x = x/2
                elif let == '*':
                        x = x*2
                elif let == 'a':
                        if abs(x)<=1:
                                x = math.asin(x)
                        else:
                                raise out_of_domain
                elif let == 'd':
                        if x != 0:
                                x = 1/x
                        else:
                                raise out_of_domain
                elif let == 'e':
                        if x <= -10:
                                x = -10
                        elif x >= 10:
                                x = 10
                        x = math.exp(x)
                elif let == 'l':
                        if x > 0:
                                x = math.log(x)
                        else:
                                raise out_of_domain
                elif let == 's':
                        x = math.sin(x)
        return x
        
def consume():
        A = 0
        linear = 0
        is_lin = 1
        d = 0
        e = 0
        l = 0
        linear_function = ['/', '*']
        for i in stream:
                if i in linear_function:
                        linear += 1
                elif i == 's':
                        A += 1
                elif i == 'a':
                        A -= 1
                elif i == 'd':
                        d += 1
                        is_lin = 0
                elif i == 'e':
                        e += 1
                        is_lin = 0
                elif i == 'l':
                        l += 1
                        is_lin = 0
        if A > 0: is_lin = 1
        cost = int(bas_cons + pow(2+linear,1.5+A+0.5*is_lin) + pow(5*d,1+A) + pow(3*e,1+A) + pow(4*l,1+A))
        return cost

def make_expr():
        myexpr = 'x'
        for i in range(len(stream)):
                if i==0 and stream[i]=='-':myexpr='-x'
                if i==0 and stream[i]=='*':myexpr='2x'
                if i==0 and stream[i]=='s':myexpr='sinx'
                if i==0 and stream[i]=='e':myexpr='ex'
                if i==0 and stream[i]=='/':myexpr='x/2'
                if i==0 and stream[i]=='d':myexpr='1/x'
                if i==0 and stream[i]=='l':myexpr='lnx'
                if i==0 and stream[i]=='a':myexpr='arcsinx'

                if i>0 and stream[i]=='d':myexpr='1/'+'('+myexpr+')'
                if i>0 and stream[i]=='s':myexpr='sin'+'('+myexpr+')'
                if i>0 and stream[i]=='a':myexpr='arcsin'+'('+myexpr+')'
                if i>0 and stream[i]=='l':myexpr='ln'+'('+myexpr+')'
                if i>0 and stream[i]=='e':myexpr='e'+'('+myexpr+')'
                if i>0 and stream[i]=='*':
                        if stream[i-1]=='e' or stream[i-1]=='s' or stream[i-1]=='l' or stream[i-1]=='f':
                                myexpr='2'+myexpr
                        elif stream[i-1]=='d':
                                myexpr='2'+myexpr[1:len(myexpr)]
                        else: myexpr='2'+'('+myexpr+')'
                if i>0 and stream[i]=='-':
                        if stream[i-1]=='-':
                                myexpr='-('+myexpr+')'
                        else:
                                myexpr='-'+myexpr
                if i>0 and stream[i]=='/':
                        if stream[i-1]=='d':
                                myexpr=myexpr[0:1]+'(2'+myexpr[2:len(myexpr)]+')'
                        else: myexpr='('+myexpr+')/2'
        return myexpr
