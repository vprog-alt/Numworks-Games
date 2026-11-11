from bprg import *

t=17
bg=(0,)*3

c=[(0,0,255)]*9+[(255,)*3]*9+[(0,220,0)]*9+[(255,0,0)]*9+[(255,160,20)]*9+[(255,255,0)]*9
c_solved=c[:]
VIT=0.02
scr,chrono=False,0

class Cube:
  def face(C,x,y):
    for i in range(9):rect(x+(i%3)*t,y+(i//3)*t,t,t,C[i])
  def tranch(C,x,y,o):
    for i in range(3):
      if o:rect(x,y+i*t,t,t,C[i])
      else:rect(x+i*t,y,t,t,C[-i-1])
  def aff():
    x,y=160-t*4.5,111-t*1.5
    for (C,X,Y) in ([c[0:9],x,y],[c[9:18],x+t*3,y],[c[18:27],x+t*6,y],[c[27:36],x+t*3,y-t*3],[c[36:45],x+t*3,y+t*3]):Cube.face(C,X,Y)
    for (C,X,Y,O) in [(c[45:48],x+t*3,y-t*4-t//2,0),(c[51:54],x+t*3,y+t*6+t//2,0),([c[47],c[50],c[53]],x-t-t//2,y,1),([c[45],c[48],c[51]],x+t*9+t//2,y,1)]:Cube.tranch(C,X,Y,O)

class Mv:
  def anclnk(R):
    global c
    R2,c2=R[1:]+R[:1],c[:]
    for i in R:c[i]=c2[R2[R.index(i)]]
  def clnk(R):
    global c
    R2,c2=R[-1:]+R[:-1],c[:]
    for i in R:c[i]=c2[R2[R.index(i)]]

class Rt:
  def L(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([9,33,30,27,47,50,53,42,39,36,15,12])".format(f))
      if i in (0,2):exec("Mv.{}clnk([0,3,6,7,8,5,2,1])".format(f))
      Cube.aff()
  def R(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([11,35,32,29,45,48,51,44,41,38,17,14])".format(f))
      if i in (0,2):exec("Mv.{}clnk([18,19,20,23,26,25,24,21])".format(f))
      Cube.aff()
  def U(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([9,2,1,0,47,46,45,20,19,18,11,10])".format(f))
      if i in (0,2):exec("Mv.{}clnk([27,28,29,32,35,34,33,30])".format(f))
      Cube.aff()
  def D(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([15,16,17,24,25,26,51,52,53,6,7,8])".format(f))
      if i in (0,2):exec("Mv.{}clnk([36,37,38,41,44,43,42,39])".format(f))
      Cube.aff()
  def F(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([33,34,35,18,21,24,38,37,36,8,5,2])".format(f))
      if i in (0,2):exec("Mv.{}clnk([9,10,11,14,17,16,15,12])".format(f))
      Cube.aff()
  def B(s):
    f="an" if s else ""
    for i in range(3):
      sleep(VIT),exec("Mv.{}clnk([27,0,3,6,42,43,44,26,23,20,29,28])".format(f))
      if i in (0,2):exec("Mv.{}clnk([45,46,47,50,53,52,51,48])".format(f))
      Cube.aff()
  def M(s):
    f="an" if s else ""
    for i in range(3):sleep(VIT),exec("Mv.{}clnk([10,34,31,28,46,49,52,43,40,37,16,13])".format(f)),Cube.aff()
  def S(s):
    f="an" if s else ""
    for i in range(3):sleep(VIT),exec("Mv.{}clnk([30,31,32,19,22,25,41,40,39,7,4,1])".format(f)),Cube.aff()
  def E(s):
    f="an" if s else ""
    for i in range(3):sleep(VIT),exec("Mv.{}clnk([12,13,14,21,22,23,48,49,50,3,4,5])".format(f)),Cube.aff()
  def X(s):
    global VIT
    V,VIT=VIT,VIT/3
    Rt.U(not s),Rt.E(s),Rt.D(s)
    VIT=V
  def Y(s):
    global VIT
    V,VIT=VIT,VIT/3
    Rt.L(s),Rt.M(s),Rt.R(s)
    VIT=V
  def Z(s):
    global VIT
    V,VIT=VIT,VIT/3
    Rt.F(s),Rt.S(s),Rt.B(not s)
    VIT=V
  def prog(*M):
    for i in M:
      exec("Rt.{}({})".format(i[0],len(i)-1))

class SC:
  def C(a,b,c):rect(2,2,18,18,(a,b,c))
  def solved():
    for i in range(0,45):
      if c[i]!=c[cut(i,9)]:return False
    return True
  def scramble():
    global VIT
    V,VIT=VIT,0
    for i in range(randint(18,30)):
      exec("Rt.{}({})".format(choice("LRUDFB"),randint(0,1)))
    VIT=V
  def reset():
    global c
    c=c_solved[:]
    Cube.aff()
  def timer():
    global scr,chrono
    if key(4) and not scr:
      if not SC.solved():
        m=monotonic()
        SC.C(255,0,0)
        while key(4):
          if monotonic()-m>0.4:
            SC.C(0,220,0)
            scr=True
      chrono=monotonic()
    T="{:.3f}".format(monotonic()-chrono)
    if scr:
      SC.C(0,200,0),draw(T,318-10*len(T),0,(255,)*3,bg)
      if monotonic()%0.1<0.05:SC.C(*bg)
    if SC.solved() and scr:
      SC.C(0,220,0),draw(T,318-10*len(T),0,(0,220,0),bg)
      scr,chrono=False,0

def k(k):
  if keyS(k):return True

background(bg),Cube.aff()

while True:
  if k(12):Rt.L(0)
  if k(18):Rt.L(1)
  if k(17):Rt.R(0)
  if k(23):Rt.R(1)
  if k(13):Rt.U(0)
  if k(16):Rt.U(1)
  if k(22):Rt.D(0)
  if k(19):Rt.D(1)
  if k(15):Rt.F(0)
  if k(14):Rt.F(1)
  if k(20):Rt.B(0)
  if k(21):Rt.B(1)
  if k(29):Rt.M(0)
  if k(24):Rt.M(1)
  if k(27):Rt.S(0)
  if k(26):Rt.S(1)
  if k(28):Rt.E(0)
  if k(25):Rt.E(1)
  if k(3):Rt.X(0)
  if k(0):Rt.X(1)
  if k(1):Rt.Y(0)
  if k(2):Rt.Y(1)
  if k(34):Rt.Z(0)
  if k(33):Rt.Z(1)
  if k(50):SC.scramble()
  if k(48):SC.reset()
  SC.timer()

#11 Nov 2026 V7 1.6 (175 4.6ko) (V6:273 11.5ko) |JellyCubing(YT)|Jell(NW)|Vprog-alt(GTB)
