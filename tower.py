from tower_maker import *

CONV="-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPPQRSTUVWXYZ"

#size,posX,posY,sleep,jump,grav,antigrav,friction,dash
t,X,Y,S,J,G,Q,B,DASH=10,0,2,1/63,-7,0.98,0.49,0.8,2;Bm=B

COLORS=[(80,120,200),(40,70,120),(20,30,60),(180,180,200),(255,140,0),(200,100,0),(230,230,200),(255,0,255),(150,255,20),(20,220,255),(255,230,50)]
bg,c,c2,c_title=[(0,)*3]*4
C_PIECE,C_PLAYER=(255,255,0),[(255,0,0),(0,0,255),(220,255,255),(255,255,255),(0,255,0)]

def PALETTE(gm):
  global COLORS,bg,c,c2,c_title
  c,COLORS[1],bg,c2,c_title=(80,120,200),(40,70,120),(10,20,30),(20,30,60),(200,255,255)
  if gm==1:c,COLORS[1],bg,c2,c_title=(80,200,150),(40,120,90),(10,30,20),(20,60,50),(200,255,220)
  if gm==2:c,COLORS[1],bg,c2,c_title=(150,80,200),(90,40,120),(20,10,30),(50,20,60),(255,200,255)
  if gm==3:c,COLORS[1],bg,c2,c_title=(200,200,80),(120,120,40),(30,30,10),(60,60,20),(255,255,200)
  if gm==4:c,COLORS[1],bg,c2,c_title=(200,100,100),(150,60,60),(30,10,10),(80,35,35),(255,200,200)
  COLORS[0],COLORS[2],c_title=c,fade(1,7,bg,c),fade(2,3,c,(255,)*3)

def UNPACK():
  global platforms,movable,spawn
  platforms,movable,spawn,lvdef=[],[],[],levels
  if gamemode==1:lvdef=tuto
  if custom and gamemode in (3,5,6):lvdef=custom
  PALETTE(gamemode)
  for i in range(len(lvdef[LV])/5):
    x,y,w,h,ptf=tuple(CONV.index(rang)-1 for rang in lvdef[LV][i*5:][:5])
    if i==0:spawn=[x*t+(w*t-t)//2,Y+(y-1)*t]
    if ptf==4:
      for i in range(w):platforms.append([x*t+i*t,Y+y*t,t,h*t,ptf])
    else:platforms.append([x*t,Y+y*t,w*t,h*t,ptf,[x*t-t*3,x*t+t*3] if ptf==2 else [Y+y*t-t*2,Y+y*t+t*2] if ptf==3 else [x*t-t*w+t,x*t+t*w-t,h/10] if ptf==10 else []])

def SETLEVEL():
  global x,y,a,jump,jumps,platforms,collisions,objets,pieces
  px,py,collisions,removing,cTime=x,y,[],[],sin(monotonic())/1.6
  for P in platforms:
    x,y,w,h,ptf=P[:5]
    if ptf in (0,1):
      if w/t>1:rect(x,y+t,w,h-t,COLORS[ptf+1])
      rect(x,y,w,(h if ptf==0 and w/t==1 else t),COLORS[0]);collisions.append([x,y,w,(t if ptf else h),0])
    if ptf in (2,3):
      P[ptf-2]=limits(P[ptf-2]+cTime,P[5][0],P[5][1])
      rect(x-1,y,1,h,bg),rect(x+w,y,1,h,bg),rect(x,y-1,w,1,bg),rect(x,y+h,w,1,bg),rect(P[0],P[1],w,h,COLORS[3]);collisions.append([P[0],P[1],w,h,ptf])
    if ptf==4:
      C=[x,y,t,t,4]
      rect(x+1,y,t-2,t,COLORS[4]),rect(x,y+1,t,t-2,COLORS[4]),rect(x+2,y+2,t-4,t-4,COLORS[5]);collisions.append(C)
      if grounded([px,py],C):
        if key(4):a,jump,jumps=-7,True,jumps+1
        rect(x,y,w,h,bg);removing.append([P,C])
    if ptf==5:
      if not objets[LV]:
        rect(x+3,y+2,t-6,t-4,C_PIECE),rect(x+2,y+3,t-4,t-6,C_PIECE)
        if inside([px,py],P):
          pieces,objets[LV]=pieces+1,1
          rect(x+2,y+2,t-4,t-4,bg);removing.append([P])
    if ptf==6:
      for i in range(w/t):rect(x+i*t+t//2-1,y+t-6,2,6,COLORS[6]),rect(x+i*t+t//2-3,y+t-4,6,4,COLORS[6])
      rect(x,y+t-2,w,2,COLORS[6]);collisions.append([x+2,y+t-4,w-4,4,6])
    if ptf==7:
      for i in range(w/t):rect(x+i*t+t//2-1,y,2,6,COLORS[6]),rect(x+i*t+t//2-3,y,6,4,COLORS[6])
      rect(x,y,w,2,COLORS[6]);collisions.append([x+2,y,w-4,4,7])
    if ptf==8:
      for i in range(h/t):rect(x+t-6,y+i*t+t//2-1,6,2,COLORS[6]),rect(x+t-4,y+i*t+t//2-3,4,6,COLORS[6])
      rect(x+t-2,y,2,h,COLORS[6]);collisions.append([x+t-4,y+2,4,h-4,8])
    if ptf==9:
      for i in range(h/t):rect(x,y+i*t+t//2-1,6,2,COLORS[6]),rect(x,y+i*t+t//2-3,4,6,COLORS[6])
      rect(x,y,2,h,COLORS[6]);collisions.append([x,y+2,4,h-4,9])
    if ptf==10:
      P[0]=limits(P[0]+cTime*P[5][2],P[5][0],P[5][1])
      rect(x-2,y,t+4,t,bg),rect(P[0],y,t,t,COLORS[7]);collisions.append([x,y,t,t-1,10])
    if ptf==11:
      rect(x+1,y+t-2,w-2,2,COLORS[8])
      C=[x+1,y+t-2,w,1,11];collisions.append(C)
      if grounded([px,py],C):a,jump=-10,True
    if ptf==12:rect(x,y,w,h,COLORS[9]);collisions.append([x,y,w,h,12])
    if ptf==13:
      if (w/t)>1:
        for i in range(w/t):rect(x+t//2-1+i*t,y,2,h,COLORS[10]),rect(x+t//2-2+i*t,y,4,2,COLORS[3])
        for j in range(h/t):rect(x,y+t//2-1+j*t,w,2,COLORS[10])
        collisions.append([x,y+t+3,w,h-t-3,13])
      else:rect(x+t//2-1,y,2,h,COLORS[10]),rect(x+t//2-2,y,4,2,COLORS[3]);collisions.append([x+t//2-1,y+t+3,2,h-t-3,13])
  for N in removing:
    try:platforms.remove(N[0]);collisions.remove(N[1])#retire la plateforme, puis la collision
    except:""
  x,y=px,py

def grounded(it,it2):
  if it[0]+t>it2[0] and it[0]<it2[0]+it2[2] and it[1]+t>=it2[1] and it[1]<it2[1]:return True
def uped(it,it2):
  if it[0]+t>it2[0] and it[0]<it2[0]+it2[2] and it[1]<=it2[1]+it2[3] and it[1]+t>it2[1]+it2[3]:return True
def walled(it,it2):
  if it[1]>it2[1]-t and it[1]<it2[1]+it2[3]:
    if it[0]+t>it2[0] and it[0]<it2[0]+it2[2]:return True
def inside(it,it2):
  if it[0]+t>it2[0] and it[0]<it2[0]+it2[2] and it[1]+t>it2[1] and it[1]<it2[1]+it2[3]:return True

def APPLY_cols():
  global x,y,a,b,B,jump,jumps,kill,dash,m_dash,C,spawn
  B,C=Bm,C_PLAYER[0]
  for cn in collisions:
    X,Y,W,H,ptf=cn
    it=[x,y]
    if inside(it,cn):
      if ptf in (6,7,8,9,10):kill=True
      if ptf==12:B,C=1/8,C_PLAYER[2]
      if ptf==13:a,b,jump,x,y=-G,0,True,x+(key(3)-key(0))*2,y+(key(2)-key(1))*2
    if ptf!=13:
      if grounded(it,cn):y,a,jump=Y-t,0,False
      elif uped(it,cn):
        y,a=Y+H-key(1),0
        if key(1):jump,C=False,C_PLAYER[1]
      elif walled(it,cn):
        if b<0:x,b=X+W,0
        elif b>0:x,b=X-t,0
        if WALLJUMP and a>0:a,jump=G,False
  if dash:C=C_PLAYER[2]

def APPLY_phy():
  global x,y,a,b,B,jump,jumps,C,dash,m_dash
  if keyS(4) and not jump:
    if C!=C_PLAYER[1]:jumps+=1
    a,jump=J,True
  if keyS(16) and not dash:m_dash,dash=monotonic()+0.2,True
  if dash and monotonic()>m_dash:dash=False
  a,b=limits(a+G-key(4)*Q,-10,6),limits(b+(key(3)-key(0))*2,-4.5,4.5)*(DASH if dash else 1)
  if a>4:jump=True
  if b>0:b-=B
  elif b<0:b+=B
  if b<Bm/2 and b>-Bm/2:b=0

def PLAYER():
  global x,y,a,b
  rect(x,y,t,t,bg),APPLY_phy()
  x,y=limits(x+b,0,320-t),y+a
  APPLY_cols(),rect(x,y,t,t,C)

def WARP():
  global LV,x,y,a,b,kill
  if y<-t:
    background(bg)
    a,y,LV=-7,222,LV+1
    try:UNPACK(),SETLEVEL()
    except:finish("congratulations!")
  if y>222:
    if LV-1>=0:
      y,LV=0,LV-1
      background(bg),UNPACK(),SETLEVEL()
    else:kill=True

def KEYOTHERS():
  global x,y,a,b,jump,kill,deaths,platforms,collisions,spawn,objets,pieces,m,chrono,m_dash,gamemode
  if kill or keyS(26):
    if objets[LV]:objets[LV],pieces=0,pieces-1
    if not key(26):deaths+=1
    background((0,0,0)),sleep(0.3),background(bg)
    x,y,platforms,collisions,spawn=-t,-t,[],[],[]
    UNPACK(),SETLEVEL()
    x,y,a,b,jump,kill=spawn[0],spawn[1],0,0,False,False
    if gamemode==2:finish("you died")
  if key(17):
    m=monotonic()
    draw(" PAUSED ",120,0,bg,COLORS[0]),stopall(17),rect(120,0,80,20,bg)
    chrono+=monotonic()-m
    m_dash+=monotonic()-m
  if keyS(18):print(levels[LV])
  if key(52):INIT()

IMG_LIB={"T":"3ef45ef22514248955cf22554288f29e9","OT":"57671942744eaa82a848895d586509912aaa0a4122255671886777"}

def IMG(N,x,y,t,z,c):
  img=bin(int("0x"+IMG_LIB[N]))[2:]
  for i in range(len(img)):
    if img[i]=="1":rect(x+(i%z)*t,y+(i//z)*t,t,t,c)

def elt():IMG("T",15,45,11,26,fadetime(c,c_title)),IMG("OT",95,115,3,43,C_PIECE),rect(88,158,144,22,c),draw(" <          > ",90,160,C_PIECE,c2),draw_center([modes[gamemode]],160,169,C_PIECE,c2)

def menu():
  global LV,gamemode
  LV,gamemode=randint(0,len(levels)-2),0
  background(bg),UNPACK(),SETLEVEL(),elt()
  while not key(4):
    IMG("T",15,45,11,26,fadetime(c,c_title))
    gamemode=passlimits(gamemode+key(3)-key(0),0,len(modes)-1)
    if gamemode==3 and not custom:
      if key(0):gamemode-=1
      if key(3):gamemode+=1
    if keyR([0,3]):PALETTE(gamemode),background(bg),SETLEVEL(),elt(),sleep(0.14)
  LV=0
  background(bg)

def finish(TITLE):
  msg=[TITLE,"time: {} min {}s".format(int(round(monotonic()-chrono,3)//60),round((monotonic()-chrono)%60,3)),"jumps:{}  deaths:{}  points:{}".format(jumps,deaths,pieces)]
  background(bg),print(pieces,len(levels)),rect(160-t//2,92-t,t,t,C),rect(0,132,320,21,COLORS[0]),draw(msg[0],160-5*len(msg[0]),96,C_PIECE,bg),draw(msg[1],160-5*len(msg[1]),134,bg,COLORS[0])
  if deaths==0 and pieces==len(levels):draw(msg[2],160-5*len(msg[2]),156,C_PIECE,bg)
  else:draw(msg[2],160-5*len(msg[2]),156,COLORS[0],bg)
  stopall(4),background(bg),INIT()

def INIT():
  global LV,platforms,collisions,spawn,gamemode,x,y,a,b,jump,jumps,dash,m_dash,kill,deaths,pieces,objets
  LV,platforms,collisions,spawn,gamemode=0,[],[],[],0
  menu()
  if gamemode in (5,6):EDITOR(gamemode-5)
  PALETTE(gamemode),background(bg),UNPACK()
  x,y,a,b,jump=spawn[0],spawn[1],0,0,False
  jumps=kill=deaths=pieces=dash=m_dash=0
  objets=[0]*len(levels)
  release(4,0,3),SETLEVEL()
  chrono=monotonic()

def TRIGS():
  if gamemode==1:
    if LV==0:draw_center(["PRESS OK","TO JUMP"],60,120,C_PIECE,bg),draw_center(["OK LONGER","= HIGHER"],180,50,C_PIECE,bg),draw_center(["^EXIT^"],285,15,C_PIECE,bg)
    if LV==1:draw_center(["JUMP AND","PRESS UP"],230,172,C_PIECE,bg),draw_center(["RELEASE","UP"],100,172,C_PIECE,bg),draw_center(["COLLECT","PIECES"],35,40,C_PIECE,bg)
    if LV==2:draw_center(["DASH WITH","KEY TBX"],100,80,C_PIECE,bg)
    if LV==3:draw_center(["YOU CAN","WALL JUMP"],170,20,C_PIECE,bg)
  if gamemode==4:
    draw_center([" "+str(100-jumps)+" "],160,10,C_PIECE,bg)
    if jumps==101:AFFY.finish("100 jumps seem difficult")

pal,gamemode,modes=0,0,["PLAY","TUTORIAL","HARDCORE","CUSTOM LVL","100 JUMPS","CREATE","HASH"]
LV,platforms,collisions,spawn=0,[],[],[]
UNPACK()
x,y,a,b,jump=spawn[0],spawn[1],0,0,False
jumps=kill=deaths=pieces=dash=m_dash=0
objets=[0]*len(levels)
background(bg)
INIT()

chrono=monotonic()

while True:
  SETLEVEL(),TRIGS(),PLAYER(),KEYOTHERS(),WARP(),sleep(S)

#9.817ko|2026.10.31.12.19|jell(NW)|jellycubing(YT)|vprog-alt(GITHUB)
