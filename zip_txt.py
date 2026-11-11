from bprg import *

def ZIP(txt,nbline=None,B=55):
  L=S=""
  for i in txt:L+=fill_txt(str(ord(i)),"0",3)
  for i in range(len(L)/6):
    l=L[i*6:i*6+6]
    S+=chr(int(fill_txt(l,"0",6)))
  return S

def UNZIP(txt,nbline=None,char="",B=150):
  if len(txt)>1587:
    print("txt to big for the alocated memory.")
    return
  S=L=""
  for i in txt:S+=fill_txt(str(ord(i)),"0",6)
  for i in range(len(S)):
    l=S[i*3:i*3+3]
    if l=="010":L+=char
    if l!="":L+=chr(int(l))
  return L

def aff(L,nbline):
  if nbline=="":
  for i in range(len(L)/B):print(L[i*B:i*B+B])
  elif nbline==None:print(L)
  elif nbline>-1:print(L[nbline*B:nbline*B+B])
  return L

cmp="𑦥𚙌𛆸𕑇𛶼𘚠"
print(UNZIP(cmp))
