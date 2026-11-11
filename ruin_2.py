#P="""
from ruin_maker import *

class Entity():
  def __init__(it,x,y,w,h,drawFonc):
    it.x,it.y,it.w,it.h=x,y,w,h
    it.draw=lambda:drawFonc(it)
  def hitBox(it,it2):
    if it.x<it2.x+it2.w and it2.x<it.x+it.w and it.y<it2.y+it2.h and it2.y<it.y+it.h:return 1
    return 0
class Platform(Entity):
  def __init__(it,x,y,w,h):super().__init__(x,y,w,h,drawPlatform)
  def hitBox(it,it2):
    if super().hitBox(it2) and it2.y+it2.h<it.y+it.h:return 1
    return 0
class Movable(Entity):
  def __init__(it,*arg):
    super().__init__(*arg)
    it.vx,it.vy,it.grounded=0,0,0
  def setVel(it,vx,vy):it.vx,it.vy=vx,vy
  def addVel(it,vx,vy):
    it.vx+=vx
    it.vy+=vy
  def applyPhysics(it):
    if it.grounded:
      it2=it.grounded
      it.vy=0
      if it.x>it2.x+it2.w or it2.x>it.x+it.w:
        it.grounded=0
    else :
      it.addVel(0,0.2)
      it.y+=min(it.vy,4)
    it.vx/=1.3
    it.x+=it.vx
    it.x=max(min(it.x,320-it.w),0)
  def onPlatform(it,plat):
    if plat.hitBox(it) and not it.grounded and it.vy>0:
      it.grounded=plat
      it.vy,it.y=0,plat.y-it.h
  def jump(it):it.vy,it.grounded=-4.3,0
class Enemy(Movable):
  def __init__(it,*arg):
    super().__init__(*list(arg)+[drawEnemy])
  def applyPhysics(it):
    if it.grounded:
      it2=it.grounded
      if it2.w>20:
        if it.x<it2.x+it.w:
          it.vx+=0.05
        elif it.x>it2.x+it2.w-it.w*2:
          it.vx-=0.05
        elif it.vx==0:
          it.vx=1
    super().applyPhysics()
    it.vx*=1.3
class Bullet(Movable):
  def __init__(it,it2,input_vy):
    super().__init__(it2.x+it2.w/2,it2.y+it2.h/2,3,3,drawBullet)
    it.setVel(copysign(3,it2.vx)+it2.vx,it2.vy+input_vy*2-1)
  def applyPhysics(it):
    it.addVel(0,0.2)
    it.x+=it.vx
    it.y+=it.vy
def shadow(it):
  for i in range(1,6):
    drawRect(int(it.x-i*2),int(it.y+i*it.h),it.w-i,it.h,fade(i/6,1,BLACK,BG_COL))
def drawBaseEntity(it,col):
  drawRect(int(it.x+2),int(it.y),it.w-2,it.h,col)
  drawRect(int(it.x),int(it.y),2,it.h,BLACK)
def drawPlayer(it):
  drawBaseEntity(it,PL_COL)
  drawRect(int(it.x+it.w/2),int(it.y+7),2,3,BLACK)
  for i in (3,it.h-3):drawRect(int(it.x+i+it.vx/4),int(it.y+2),2,2,BLACK)
def drawEnemy(it):
  drawBaseEntity(it,NMY_COL)
  drawRect(int(it.x+2),int(it.y+it.h/2),it.w-2,it.h//2,NMY_COL2)
  for i in (3,it.h-3):drawRect(int(it.x+i),int(it.y+it.h/2-2),2,5,BLACK)
def hideEntity(it):
  drawRect(int(it.x),int(it.y),int(it.w),int(it.h),BG_COL)
def drawPlatform(it):
  drawBaseEntity(it,PTF_COL)
  shadow(it)
def drawDoor(it):
  drawRect(int(it.x),int(it.y),it.w,it.h,BLACK)
  for i in range(1,5):
    drawRect(int(it.x+1),int(it.y+it.h-i*2),int(it.w/2-i*2+3),1,fade(i/6,1,PTF_COL,BLACK))
def drawBullet(it):drawRect(int(it.x),int(it.y),it.w,it.h,PTF_COL)
def createDoor(l1):
  x,y,w,h=l1
  x,y,w,h=x+w//2-7.5,y-15,15,15
  return Entity(x,y,w,h,drawDoor)
def createPlayer(l1):
  x,y,w,h=l1
  y,w,h=y-10,10,10
  return Movable(x,y,w,h,drawPlayer)
def createEnemy(l1,id):
  x,y,w,h=l1
  x,y,w,h=x+10*id,y-10,10,10
  return Enemy(x,y,w,h)

def unpackPlatforms(n,type):
  s=levels()[n]
  return [[B.index(s[i+j])*5 for j in range(4)]+[B.index(s[i+4])] for i in range(0,len(s),5)]
def loadLevel(lvl,type):
  file=unpackPlatforms(lvl,type)
  platforms,enemies=[],[]
  for i in file:
    platforms+=[Platform(*i[0:4])]
    if i[4]:
      enemies+=[createEnemy(i[0:4],j) for j in range(i[4])]
  player,door=createPlayer(file[0][0:4]),createDoor(file[-1][:4])
  return [player,platforms,enemies,door]

IMG_LIB=["3d24994937d24ba49264c49","651d57aa22e988755a908aa621157","5766761942744eaaa8a2a848895555946209912aaaa28a412225766761886777"]

def IMG(N,x,y,t,z,c):
  img=bin(int("0x"+IMG_LIB[N]))[2:]
  for i in range(len(img)):
    if img[i]=="1":drawRect(x+(i%z)*t,y+(i//z)*t,t,t,c)

modelib=["original","custom","select levels","new level","edit level","read hash","share hash"]

def titleAnim(h=150):
  global lvl_type,lvl_selected,BG_COL,PTF_COL,NMY_COL,NMY_COL2,TITLE_COL,palette
  y,s_init,p,m,o,o2=int(h),20,0,0,0,0
  drawRect(0,0,320,222,BG_COL)
  while y>5:
    if not p:
      m=passlimits(m+keyS(3)-keyS(0),0,len(modelib)-1)
      lvl_type=modelib[m]
    if key(4):
      releaseKey(4)
      if m==1 and LVL_customs==[]:
        drawTxt(" no customs levels ",65,100,BG_COL,PTF_COL),sleep(0.9),background(BG_COL)
      elif m in (2,6):
        background(BG_COL)
        while not key(4):
          if LVL_customs:o2=exlimits(o2+keyS(2)-keyS(1),0,1)
          o=exlimits(o+key(3)-key(0),0,len(LVL_customs if o2 else LVL_originals)-1)
          S=LVL_customs[o] if o2 else LVL_originals[o]
          l="  level {}: < {} >  ".format("custom" if o2 else "original",str(o+1))
          drawTxt(l,160-5*len(l),100,PTF_COL,BG_COL),sleep(0.12)
        if m==2:
          lvl_selected,p=S,1
        else:
          background(BG_COL)
          Y=int(111-9*(len(S)/20))
          for i in range(len(S)/20):
            L=S[i*20:][:20]
            drawTxt(L,160-len(L)*5,Y+i*18,PTF_COL,BG_COL)
          print("shared:\n"+S),stopall(4),background(BG_COL)
      elif m in (3,4,5):
        if launch(m) and LVL_customs:p=1
      else:p=1
      releaseKey(4)
    palette=passlimits(palette+keyS(34)-keyS(33),0,len(colors)-1)
    BG_COL,PTF_COL,NMY_COL,NMY_COL2,TITLE_COL=colors[palette]
    if key(34) or key(33):
      background(BG_COL)
    s=(1-y/h)*s_init+p
    y=round(y-s,1)
    l=" "*8+"< "+lvl_type+" >"+" "*8
    IMG(0,16,int(50+h-y),16,18,fadetime(PTF_COL,TITLE_COL))
    IMG(1,16,int(20+h-y),3,23,PTF_COL)
    IMG(2,150,int(20+h-y),3,51,PTF_COL)
    drawRect(115,int(26+h-y),9,3,PTF_COL)
    drawTxt(l,160-5*len(l),int(151+h-y),TXT_COL,BG_COL)
    drawTxt("Press [OK] to start",65,int(181+h-y),fadetime(BG_COL,PL_COL),BG_COL)
    sleep(TARG_SPF/1.2)
    if p:drawRect(0,0,320,222,BG_COL)
  
def shortTransition():
  for i in range(30):drawRect(0,0,320,222,fade(sin(i/30),1,BG_COL,BLACK))
def releaseKey(x):
  while key(x):pass

class GameEngine():
  def __init__(it,lvl_type=""):
    it.status,it.lvl_type,it.lvl_nb=0,lvl_type,len(levels())
    it.lvl,it.total_frame=0,0
  def nextLevel(it):
    global donnees
    if it.status==2:
      it.playTransition(mode=1)
      it.lvl+=1
      it.playTransition()
    elif it.status==20:
      donnees=[0,0,0]
      it.lvl,it.frame_nb,it.total_frame=0,0,0
      titleAnim()
      game.playTransition()
    else:
      donnees[1]+=1
      shortTransition()
  def endMsg(it):
    global donnees
    t=it.total_frame*TARG_SPF
    msg=["You finished the ",
"{} original levels !".format(len(LVL_originals)),
"",
"Virtual time: {} min {}s".format(int(t//60),round(t%60,2)),
"Jumps: {}  Deaths: {}".format(donnees[0],donnees[1]),
"Bullets used: {}".format(donnees[2]),]
    if lvl_type!=modelib[0]:
      msg=[msg[3],msg[4],msg[5]]
    for i,txt in enumerate(msg):
      drawTxt(txt,160-len(txt)*5,111-9*len(msg)+18*i,PTF_COL,BG_COL)
    for i in range(len(donnees)-1):donnees[i]=0
    it.lvl,it.frame_nb=0,0
    while not key(4):
      drawTxt("Press [OK]",210,200,fadetime(BG_COL,PL_COL),BG_COL)
    releaseKey(4)
    titleAnim()
    game.playTransition()
  def playTransition(it,h=222,mode=0):
    try:l=loadLevel(it.lvl,it.lvl_type)
    except:return
    entities,s_init,y=l[1]+[l[3]],20,int(h)
    if not mode:
      entities+=[l[0]]+l[2]
      for entity in entities:entity.y-=y
    del l
    while 1:
      if y<1:break
      if mode:s=(1-y/h)*s_init+5
      else:s=sqrt(y/h)*s_init
      sleep(TARG_SPF*2)
      y=round(y-s,1)
      drawRect(0,0,320,222,BG_COL)
      for entity in entities:
        entity.y+=s
        entity.draw()
  def playLevel(it):
    global donnees
    drawRect(0,0,320,222,BG_COL)
    player,platforms,enemies,door=loadLevel(it.lvl,it.lvl_type)
    frame_nb,shot_frame,bullets,it.status=0,0,[],0
    while it.status==0:
      t=cTime()
      frame_nb+=1
      player.addVel(key(3)-key(0),0.1*(1-key(4)))
      if (frame_nb+9)%10==0:door.draw()
      for b in bullets:
        hideEntity(b)
        b.applyPhysics()
        if b.y>222:bullets.remove(b)
        else:b.draw()
      for movable in enemies+[player]:
        hideEntity(movable)
        if movable!=player:
          if movable.hitBox(player):
            it.status=1
            break
          for b in bullets:
            if b.hitBox(movable):
              movable.addVel(b.vx/3,b.vy/3)
          if movable.y>222:
            enemies.remove(movable)
        movable.applyPhysics()
        for platform in platforms:
          movable.onPlatform(platform)
          if (frame_nb+9)%10==0 and movable==player:platform.draw()
        movable.draw()
      if frame_nb-shot_frame>10 and key(16):
        shot_frame=frame_nb
        bullets+=[Bullet(player,key(2)-key(1))]
        donnees[2]+=1
      if player.grounded:
        if key(4):
          player.jump()
          donnees[0]+=1
        if player.hitBox(door)==1:it.status=2
      if player.y>222:it.status=1
      while cTime()-t<TARG_SPF:pass
      if keyS(12):
        print("shared:\n"+LVL_originals[it.lvl] if lvl_type==modelib[0] else LVL_customs[it.lvl])
        drawTxt(" S H A R E D ",95,100,BG_COL,PTF_COL)
        sleep(0.8)
        drawRect(95,100,130,18,BG_COL)
      if key(17):
        drawTxt(" P A U S E D ",95,100,BG_COL,PTF_COL)
        stopall(17)
        drawRect(95,100,130,20,BG_COL)
      if key(52):it.status=20
    it.total_frame+=frame_nb

def levels():
  if lvl_type==modelib[0]:return LVL_originals
  elif lvl_type==modelib[1]:return LVL_customs if LVL_customs else LVL_originals
  elif lvl_type==modelib[2]:return [lvl_selected]
  else:return [LVL_customs[-1]]

lvl_type=modelib[0]

game=GameEngine("")
donnees=[0,0,0]

TARG_SPF=1/50

releaseKey(4)
titleAnim()
game.playTransition()
while 1:
  if game.lvl>=len(levels()):
    game.endMsg()
  else:
    game.playLevel()
    game.nextLevel()
#"""
#print(len(P)-2)
