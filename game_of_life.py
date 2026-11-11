from bprg import randint,rect,fullist,passlimits,same,background,key,keyS,sleep

def randcells(W,H):
  for j in range(int(H)):
    for i in range(int(W)):cells[j][i]=randint(0,1)
  return cells
def aff():
  background(clr[0])
  for j in range(int(H)):
    for i in range(int(W)):
      if cells[j][i]:rect(i*t,j*t,t,t,clr[1])

def next_gen():
  global cells
  cells_next=fullist(0,W,H)
  for j in range(H):
    for i in range(W):
      compt,cell=0,cells[j][i]
      for d in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        if cells[passlimits(j+d[1],0,H-1)][passlimits(i+d[0],0,W-1)]:compt+=1
      if compt in (2,3) and cell:cells_next[j][i]=1
      elif compt==3 and not cell:cells_next[j][i]=1
  cells=same(cells_next)

def edit():
  global cells,x,y,t
  while not keyS(52):
    x,y=passlimits(x+key(3)-key(0),0,W-1),passlimits(y+key(2)-key(1),0,H-1)
    if key(4):cells[y][x]=1
    if key(17):cells[y][x]=0
    if keyS(26):cells=fullist(0,W,H);aff()
    if keyS(27):cells=randcells(W,H);aff()
    if key(51):next_gen(),aff()
    cell=cells[y][x]
    rect(x*t,y*t,t,t,clr[2]),rect(x*t+1,y*t+1,t*0.8,t*0.8,clr[cell]),sleep(0.08),rect(x*t,y*t,t,t,clr[cell])

x,y,t=0,0,8
W,H=320//t,222//t
cells,clr=fullist(0,W,H),[(0,0,0),(0,150,150),(255,60,60)]
cells=randcells(W,H)
background(clr[0])

while True:
  aff()
  if keyS(52):edit()
  next_gen()
