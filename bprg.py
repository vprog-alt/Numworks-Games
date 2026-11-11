def imp(*S):
  for s in S:exec("from {} import *".format(s))
imp("math","random","time")

from ion import keydown as key
from kandinsky import draw_string, get_pixel as get, set_pixel, set_pixel as set,fill_rect

#FILL
def rect(x,y,w,h,c):fill_rect(int(x),int(y),int(w),int(h),c)
def set(x,y,c):set_pixel(int(x),int(y),c)
def draw(txt,x,y,*C):draw_string(str(txt),int(x),int(y),*C)
def draw_center(txt,x,y,*C):
  for i,l in enumerate(txt):draw(l,x-5*len(l),y+i*18-len(txt)*9,*C)
def background(bg):rect(0,0,320,222,bg)
def circle(cx,cy,r,color):
  for y in range(-r,r+1):
    dx=int((r*r-y*y)**0.5)
    fill_rect(cx-dx,cy+y,2*dx,1,color)
def line(x1,y1,x2,y2,c):
  v_x,v_y=(x2-x1)/320,(y2-y1)/320
  for _ in range(320):
    set(x1,y1,c)
    x1,y1=x1+v_x,y1+v_y
def in_rayon(x,y,x2,y2,rayon):
  return (x2-x)**2+(y2-y)**2<rayon**2

#RVB
def fade(step,segments,*colors):
  n=len(colors)-1
  i=min(int((step/segments)*n),n-1)
  if n==0:return colors[0]
  return tuple(int(a+(b-a)*(((step/segments)*n)-i)) for a,b in zip(colors[i],colors[i+1]))
def fadetime(*colors):
  step,segments,n=abs(sin(monotonic())),1,len(colors)-1
  i=min(int((step/segments)*n),n-1)
  if n==0:return colors[0]
  return tuple(int(a+(b-a)*(((step/segments)*n)-i)) for a,b in zip(colors[i],colors[i+1]))

#KEYDOWN
__pressed_state__={}
def release(*K):
  for k in K:
    while key(k):0
def wait(k):
  while not key(k):""
def stopall(k):release(k),wait(k),release(k)
def keyS(k):
  if k not in __pressed_state__:__pressed_state__[k]=0
  if not key(k):
    __pressed_state__[k]=0
    return 0
  if not __pressed_state__[k]:
    __pressed_state__[k]=1
    return 1
  return 0
def keyR(K):
  for k in K:
    if key(k)==1:return 1

#MODULO
def limits(nb,mi,ma):return min(max(nb,mi),ma)
def passlimits(nb,mi,ma):
  if nb<mi:nb=ma-(mi-nb)+1
  elif nb>ma:nb=mi-(ma-nb)-1
  return nb
def exlimits(nb,mi,ma):
  while nb>ma or nb<mi:nb=passlimits(nb,mi,ma)
  return nb
def cut(i,val):return (i//val)*val

#LIST
def same(lst):return [row[:] for row in lst]
def randlist(r,*R):return [choice(R) for i in range(r)]
def randbits(nb):return "".join(str(b) for b in [randint(0,1) for i in range(nb)])
def fullist(car,w,h):return [[car for i in range(w)] for j in range(h)]

#CONV
def bin_to_hex(b):return hex(int("0b"+b))[2:]
def hex_to_bin(h):return bin(int("0x"+h))[2:]
def fill_txt(txt,char,max):return char*(max-len(txt))+txt
def ascii(n):return chr(n)

release(4)
