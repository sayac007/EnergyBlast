"""Draw original layered UI assets; no game images, fonts or logos are traced."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import math,random
R=Path(__file__).resolve().parents[1];O=R/'shared/assets/defold06';S=3
def save(name,image):image.resize((image.width//S,image.height//S),Image.Resampling.LANCZOS).save(O/(name+'.png'))
def poly(draw,points,fill):draw.polygon([(int(x*S),int(y*S))for x,y in points],fill=fill)
for name,top,bottom in [('button_blue',(66,165,239),(29,83,166)),('button_gold',(255,211,82),(211,124,27)),('button_green',(76,220,168),(25,133,115)),('button_violet',(161,115,240),(87,48,166)),('panel',(38,67,105),(16,35,64))]:
 im=Image.new('RGBA',(128*S,128*S));d=ImageDraw.Draw(im);d.rounded_rectangle((2*S,9*S,126*S,127*S),radius=21*S,fill=(3,12,29,190))
 mask=Image.new('L',im.size);md=ImageDraw.Draw(mask);md.rounded_rectangle((3*S,3*S,125*S,119*S),radius=20*S,fill=255)
 fill=Image.new('RGBA',im.size);px=fill.load()
 for y in range(im.height):
  t=min(1,max(0,(y/S-3)/116));c=tuple(round(a*(1-t)+b*t)for a,b in zip(top,bottom))+(255,)
  for x in range(im.width):px[x,y]=c
 im.paste(fill,(0,0),mask);d=ImageDraw.Draw(im);d.rounded_rectangle((3*S,3*S,125*S,119*S),radius=20*S,outline=(9,23,48,255),width=3*S);d.arc((8*S,7*S,120*S,44*S),180,360,fill=(255,255,255,110),width=2*S);save(name,im)
for name in ['star','heart','aim','dash','hint','radio','gear','menu','sound','trap']:
 im=Image.new('RGBA',(128*S,128*S));d=ImageDraw.Draw(im)
 if name=='star':
  points=[(64+math.cos(-math.pi/2+i*math.pi/5)*(49 if i%2==0 else 24),64+math.sin(-math.pi/2+i*math.pi/5)*(49 if i%2==0 else 24))for i in range(10)]
  poly(d,[(x,y+5)for x,y in points],(124,67,16));poly(d,points,(255,203,47));poly(d,[(64,28),(72,53),(97,53),(76,68),(84,92),(64,77),(43,92),(51,68),(31,53),(56,53)],(255,224,104));d.ellipse((43*S,35*S,58*S,44*S),fill=(255,251,201))
 elif name=='heart':
  d.ellipse((16*S,18*S,70*S,73*S),fill=(218,54,106));d.ellipse((58*S,18*S,112*S,73*S),fill=(218,54,106));poly(d,[(19,57),(109,57),(64,114)],(218,54,106));d.ellipse((22*S,22*S,66*S,65*S),fill=(255,120,159));d.ellipse((65*S,22*S,104*S,64*S),fill=(255,120,159));d.ellipse((31*S,28*S,48*S,38*S),fill=(255,223,230))
 else:
  c=(239,251,255);g=(126,227,239)
  if name=='aim':
   d.ellipse((25*S,25*S,103*S,103*S),outline=c,width=7*S);d.ellipse((54*S,54*S,74*S,74*S),fill=(255,218,96))
   for p in [(64,10,64,38),(64,90,64,118),(10,64,38,64),(90,64,118,64)]:d.line(tuple(int(v*S)for v in p),fill=c,width=7*S)
  elif name=='dash':
   poly(d,[(25,27),(54,27),(88,64),(54,101),(25,101),(59,64)],c);poly(d,[(69,27),(85,27),(119,64),(85,101),(69,101),(102,64)],g)
  elif name=='hint':
   d.ellipse((38*S,17*S,90*S,74*S),fill=(255,225,112));d.rounded_rectangle((47*S,73*S,80*S,97*S),radius=6*S,fill=g);d.line((49*S,105*S,78*S,105*S),fill=c,width=6*S)
  elif name=='radio':
   d.rounded_rectangle((32*S,42*S,94*S,107*S),radius=12*S,fill=c);d.line((48*S,45*S,85*S,15*S),fill=g,width=7*S)
   for y in [66,78,90]:d.line((45*S,y*S,80*S,y*S),fill=(45,88,130),width=5*S)
  elif name=='gear':
   for i in range(8):a=i*math.pi/4;poly(d,[(64+math.cos(a)*45+math.sin(a)*9,64+math.sin(a)*45-math.cos(a)*9),(64+math.cos(a)*60+math.sin(a)*9,64+math.sin(a)*60-math.cos(a)*9),(64+math.cos(a)*60-math.sin(a)*9,64+math.sin(a)*60+math.cos(a)*9),(64+math.cos(a)*45-math.sin(a)*9,64+math.sin(a)*45+math.cos(a)*9)],c)
   d.ellipse((24*S,24*S,104*S,104*S),fill=c);d.ellipse((48*S,48*S,80*S,80*S),fill=(37,77,117))
  elif name=='menu':
   for y in [30,61,92]:d.rounded_rectangle((24*S,y*S,105*S,(y+11)*S),radius=5*S,fill=c)
  elif name=='sound':
   poly(d,[(20,49),(42,49),(66,28),(66,101),(42,80),(20,80)],c);d.arc((48*S,27*S,110*S,102*S),285,75,fill=g,width=7*S)
  elif name=='trap':
   d.arc((25*S,20*S,103*S,110*S),0,180,fill=(205,163,255),width=17*S);d.rectangle((25*S,32*S,42*S,65*S),fill=c);d.rectangle((86*S,32*S,103*S,65*S),fill=c)
 save('ui_'+name,im)
# Original calm lobby gradient, with sparse tiny sparks, not a reference-game image.
im=Image.new('RGB',(1280,720));px=im.load()
for y in range(720):
 for x in range(1280):
  glow=math.exp(-(((x-300)/500)**2+((y-330)/420)**2));px[x,y]=(int(9+10*glow),int(21+49*glow),int(43+54*glow))
d=ImageDraw.Draw(im);rng=random.Random(606)
for i in range(65):
 x=rng.randrange(1280);y=rng.randrange(720);a=rng.randrange(15,40);d.ellipse((x,y,x+2,y+2),fill=(29+a,62+a,91+a))
im.save(O/'ui_background.png')
print('Original polished UI assets generated')
