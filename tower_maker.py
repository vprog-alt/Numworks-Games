from bprg import *
imp("tower_level")

B="-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPPQRSTUVWXYZ"

platforms=[]
bg,c,C_PIECE=(10,20,30),(80,120,200),(255,255,0)
COLORS=[(80,120,200),(40,70,120),(20,30,60),(180,180,200),(255,140,0),(200,100,0),(230,230,200),(255,0,255),(150,255,20),(20,220,255),(255,230,50)]
c_cursor=[(40,70,120),(20,30,60),(180,180,200),(180,180,200),(255,140,0),(255,255,0),(230,230,200),(230,230,200),(230,230,200),(230,230,200),(255,0,255),(150,255,20),(20,220,255),(255,230,50)]
ptf_nb_types=13

types=["normal","trav","move -","move |","break","piece","pic ^","pic v","pic <","pic >","nmy","pad","ice","rope"]

t=10
W,H=(320//t)*t,(222//t)*t
X,Y=0,2
x,y,ptf,u,actual=0,2,0,0,[0,0,0,0,0]
platforms=[]

def seed(ptfs):
  platforms,l,removed=ptfs,"",[]
  for P in platforms:
    if P[4]==13:removed.append(P),platforms.remove(P)
  for P in platforms:
    if P[4] in (6,7,8,9):removed.append(P),platforms.remove(P)
  for P in platforms+removed:l+="{}{}{}{}{}".format(B[int(P[0]/t)+1],B[int(P[1]/t+1)],B[int(P[2]/t)+1],B[int(P[3]/t)+1],B[P[4]+1])
  print(l)
  return l
def read(level):
  platforms=[]
  for i in range(len(level)/5):
    x,y,w,h,ptf=[B.index(rang)-1 for rang in level[i*5:][:5]]
    if ptf==4:
      for i in range(w):platforms.append([x*t+i*t,y*t+2,t,h*t,ptf])
    else:platforms.append([x*t,y*t+2,w*t,h*t,ptf])
  return platforms

class PTF:
  def add(actual):
    global platforms
    x,y,x2,y2,ptf=actual
    w,h=x2-x,y2-y
    if w>0 and h>0:platforms.append([x,y,w,h,ptf])
  def aff(X,Y):
    EDIT.infos()
    for idx,P in enumerate(platforms):
      x,y,w,h,ptf=P
      x,y=x+X,y+Y
      if ptf in (0,1):
        rect(x,y,w,(h if ptf==0 and w/t==1 else t),COLORS[0])
        if w/t>1:rect(x,y+t,w,h-t,COLORS[ptf+1])
      if ptf in (2,3):
        rect(x,y,w,h,COLORS[3])
        if ptf==2:rect(x-t*3,y+h//2-1,w+t*6,2,(255,0,0))
        if ptf==3:rect(x+w//2-1,y-t*3,2,h+t*6,(255,0,0))
      if ptf==4:
        for i in range(w/t):rect(x+1+i*t,y,t-2,t,COLORS[4]),rect(x+i*t,y+1,t,t-2,COLORS[4]),rect(x+2+i*t,y+2,t-4,t-4,COLORS[5])
      if ptf==5:rect(x+2,y+2,t-4,t-4,C_PIECE)
      if ptf==6:
        for i in range(w/t):rect(x+i*t+t//2-1,y+t-6,2,6,COLORS[6]),rect(x+i*t+t//2-3,y+t-4,6,4,COLORS[6])
        rect(x,y+t-2,w,2,COLORS[6])
      if ptf==7:
        for i in range(w/t):rect(x+i*t+t//2-1,y,2,6,COLORS[6]),rect(x+i*t+t//2-3,y,6,4,COLORS[6])
        rect(x,y,w,2,COLORS[6])
      if ptf==8:
        for i in range(h/t):rect(x+t-6,y+i*t+t//2-1,6,2,COLORS[6]),rect(x+t-4,y+i*t+t//2-3,4,6,COLORS[6])
        rect(x+t-2,y,2,h,COLORS[6])
      if ptf==9:
        for i in range(h/t):rect(x,y+i*t+t//2-1,6,2,COLORS[6]),rect(x,y+i*t+t//2-3,4,6,COLORS[6])
        rect(x,y,2,h,COLORS[6])
      if ptf==10:rect(x,y,t,t,COLORS[7]),rect(x-w+t,y+t//2-1,w*2-t,2,(255,0,0))
      if ptf==11:rect(x+1,y+t-2,w-2,2,COLORS[8])
      if ptf==12:rect(x,y,w,h,COLORS[9])
      if ptf==13:
        if (w/t)>1:
          for i in range(w/t):rect(x+t//2-1+i*t,y,2,h,COLORS[10]),rect(x+t//2-2+i*t,y,4,2,COLORS[3])
          for j in range(h/t):rect(x,y+t//2-1+j*t,w,2,COLORS[10])          
        else:rect(x+t//2-1,y,2,h,COLORS[10]),rect(x+t//2-2,y,4,2,COLORS[3])

class CURSOR:
  def aff(c):
    for i in [(-3,0,7,1),(0,-3,1,7)]:
      X,Y,W,H=i
      rect(x+X,y+Y,W,H,c)
  def move():
    global x,y
    x,y=passlimits(x+(key(3)-key(0))*t,0,W-1+t),passlimits(y+(key(2)-key(1))*t,2-t,H+1+t*2)

class EDIT:
  def new():
    global actual,u
    if keyS(4):
      actual[u*2],actual[u*2+1],u=x,y,u+1
    if u==2:
      actual[4],u=ptf,0
      background(bg),PTF.add(actual),PTF.aff(0,0)
    if u:rect(actual[0]-1,actual[1]-1,2,2,c_cursor[ptf])
  def infos():
    draw("x:{} y:{}  ".format(x,y),0,0,(80,120,200),bg)
    draw("type:{}   ".format(types[ptf]),0,18,(80,120,200),bg)
    if platforms:draw("CP:x{} y{}  size:{}b ".format(platforms[0][0]+platforms[0][2]//2,platforms[0][1],len(platforms)*5),0,204,(80,120,200),bg)
  def ks():
    global ptf
    if keyR([0,1,2,3,4,17,33,34]):
      CURSOR.aff(bg),CURSOR.move()
      ptf=passlimits(ptf+key(34)-key(33),0,ptf_nb_types)
      EDIT.infos(),PTF.aff(0,0),CURSOR.aff(c_cursor[ptf])
      if not keyR([33,34]):sleep(0.08)
      else:release(33,34)
  def suppr():
    global platforms
    background(bg)
    actual_ptf=0
    for p in platforms:
      X,Y,W,H,ptf=p
      if [x,y]==[X,Y]:actual_ptf=p
    if actual_ptf:platforms.remove(actual_ptf)
    PTF.aff(0,0)
  def CP():
    global platforms
    if platforms:
      if platforms[0][2]==platforms[0][3]==platforms[0][4]==0:platforms.reverse(),platforms.pop(),platforms.reverse()
      platforms.reverse(),platforms.append([x,y,0,0,0]),platforms.reverse()
      draw_center([" CP set at x{} y{} ".format(x,y)],160,111,c,bg),sleep(0.5),background(bg),PTF.aff(0,0)
  def end():
    release(52),background(c),draw_center(["press ok"],160,111,bg,c)
    wait(4)
    return seed(platforms)

def EDITOR(edit_mode):
  global x,y,ptf,u,actual,platforms,custom
  x,y,ptf,u,actual=0,2,0,0,[0,0,0,0,0]
  if edit_mode==0:platforms=[]
  elif edit_mode==1:platforms=read(input("hash: "))
  else:platforms=[]
  background(bg),PTF.aff(0,0),EDIT.infos(),release(4,52)
  while not keyS(52):
    EDIT.new()
    if keyS(17):EDIT.suppr()
    if keyS(14):EDIT.CP()
    EDIT.ks()
  custom.append(EDIT.end())
  return

release(4,52)

if key(1):EDITOR(0)
if key(3):EDITOR(1)
