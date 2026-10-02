import math, random
from PIL import Image, ImageDraw, ImageFont
S=2; W,H=800,450; FPS=12; DUR=14; N=FPS*DUR
BG=(18,22,34)
FP='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(sz,b=False): return ImageFont.truetype(FB if b else FP,int(sz*S))
VX0,VY0,VX1,VY1=40,72,760,372; HY=205; BY=VY1+40; CX=400
def fl(u,v,ox=0,oy=0):
    wd=300+800*v
    return (CX+(u-.5)*wd+ox, HY+(BY-HY)*v+oy)
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def clip(x,a=0,b=1): return max(a,min(b,x))
def eo3(p): return 1-(1-p)**3
def eob(p):
    c1=1.70158; c3=c1+1
    return 1+c3*(p-1)**3+c1*(p-1)**2
class D:
    def __init__(s,im): s.d=ImageDraw.Draw(im)
    def sc(s,p): return [(x*S,y*S) for x,y in p]
    def poly(s,p,fill=None,outline=None,w=1):
        p=s.sc(p)
        if fill: s.d.polygon(p,fill=fill)
        if outline: s.d.line(p+[p[0]],fill=outline,width=max(1,int(w*S)),joint='curve')
    def line(s,p,fill,w=1): s.d.line(s.sc(p),fill=fill,width=max(1,int(w*S)))
    def ell(s,cx,cy,rx,ry=None,fill=None,outline=None,w=1):
        ry=rx if ry is None else ry
        s.d.ellipse([(cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S],fill=fill,outline=outline,width=max(1,int(w*S)))
    def rect(s,b,fill=None,outline=None,w=1):
        s.d.rectangle([b[0]*S,b[1]*S,b[2]*S,b[3]*S],fill=fill,outline=outline,width=max(1,int(w*S)))
    def rr(s,b,r,fill=None,outline=None,w=1):
        s.d.rounded_rectangle([b[0]*S,b[1]*S,b[2]*S,b[3]*S],radius=r*S,fill=fill,outline=outline,width=max(1,int(w*S)))
    def text(s,xy,t,font,fill,anchor='la'):
        s.d.text((xy[0]*S,xy[1]*S),t,font=font,fill=fill,anchor=anchor)
def layer(): return Image.new('RGBA',(W*S,H*S),(0,0,0,0))

random.seed(3)
seams=[]
for k in range(-4,12):
    for j in range(3):
        seams.append((k/8,(k+1)/8,random.uniform(.08,.98)))
cands=[s for s in seams if .1<(s[0]+s[1])/2<.9 and s[2]>.12]
random.shuffle(cands)
FLOORPTS=cands[:22]
frames_rect=[(110,105,200,170,(120,160,200)),(565,98,685,178,(230,190,120))]
POTS=[(330,160,372,205)]
pts=[]  # x,y,kind,u,v
for (a,b,c,d_,_) in frames_rect:
    for p in [(a,b),(c,b),(a,d_),(c,d_)]: pts.append((p[0],p[1],'wall',0,0))
pts.append((330,160,'wall',0,0)); pts.append((372,160,'wall',0,0))
pts.append((330,205,'wall',0,0)); pts.append((372,205,'wall',0,0))
for (u0,u1,v) in FLOORPTS:
    x,y=fl(u0,v); pts.append((x,y,'floor',u0,v))
random.seed(11); random.shuffle(pts)
NP=len(pts)
tapp=[2.2+(p[0]-VX0)/(VX1-VX0)*2.4+random.uniform(0,.15) for p in pts]
edges=set()
for i,p in enumerate(pts):
    ds=sorted(range(NP),key=lambda j:(pts[j][0]-p[0])**2+(pts[j][1]-p[1])**2)[1:3]
    for j in ds: edges.add((min(i,j),max(i,j)))

def amp(t):
    if t<5: return 0
    if t<5.6: return 9*(t-5)/.6
    if t<8: return 9
    if t<9: return 9-7*(t-8)
    return 2
def off(t): a=amp(t); return a*math.sin(2.1*t), a*.6*math.sin(2.9*t+1)

def draw_scene(d,ox,oy):
    y0=VY0-30+oy
    for i in range(12):
        ya=y0+(HY+oy-y0)*i/12; yb=y0+(HY+oy-y0)*(i+1)/12
        d.rect((VX0-30+ox,ya,VX1+30+ox,yb+1),fill=lerp((208,218,230),(182,194,210),i/11))
    for (a,b,c,e,col) in frames_rect:
        d.rect((a+ox,b+oy,c+ox,e+oy),fill=(240,238,232),outline=(90,70,55),w=3)
        d.rect((a+8+ox,b+8+oy,c-8+ox,e-8+oy),fill=col)
    for (a,b,c,e) in POTS:
        d.ell((a+c)/2+ox,b-22+oy,26,24,fill=(70,150,90))
        d.ell((a+c)/2-14+ox,b-10+oy,14,18,fill=(60,135,80))
        d.ell((a+c)/2+14+ox,b-12+oy,14,18,fill=(85,165,105))
        d.poly([(a+ox,b+oy),(c+ox,b+oy),(c-4+ox,e+oy),(a+4+ox,e+oy)],fill=(186,98,70))
    d.rect((VX0-30+ox,HY-7+oy,VX1+30+ox,HY+oy),fill=(240,240,240))
    n=26
    for i in range(n):
        va,vb=i/n,(i+1)/n
        q=[fl(-1.2,va,ox,oy),fl(2.2,va,ox,oy),fl(2.2,vb,ox,oy),fl(-1.2,vb,ox,oy)]
        d.poly(q,fill=lerp((188,146,104),(152,110,74),(va+vb)/2))
    for k in range(-8,17):
        d.line([fl(k/8,0,ox,oy),fl(k/8,1,ox,oy)],(128,92,60),.8)
    for (u0,u1,v) in seams:
        d.line([fl(u0,v,ox,oy),fl(u1,v,ox,oy)],(128,92,60),1)

def cube(d,px,py,k):
    a,b,h=40*k,20*k,44*k
    B=[(px,py+b),(px+a,py),(px,py-b),(px-a,py)]
    T=[(x,y-h) for x,y in B]
    d.poly([B[3],B[0],T[0],T[3]],fill=(46,125,214))
    d.poly([B[0],B[1],T[1],T[0]],fill=(30,95,170))
    d.poly(T,fill=(105,180,250))
    for poly in ([B[3],B[0],T[0],T[3]],[B[0],B[1],T[1],T[0]],T):
        d.line(poly+[poly[0]],(235,245,255),1)

STAGES=[(0,'Kamera / Dunia Nyata','Kamera HP menangkap lingkungan sekitar sebagai input video (frame demi frame).'),
 (2,'Tahap 1 · Feature Detection','Algoritma mencari titik unik (sudut, tepi, tekstur) yang mudah dikenali di tiap frame.'),
 (5,'Tahap 2 · Tracking','Titik feature diikuti antar-frame untuk menghitung gerak dan posisi kamera.'),
 (8,'Tahap 3 · Plane Detection','Titik-titik yang sejajar dikelompokkan menjadi bidang datar (lantai/meja) → tampil grid.'),
 (11,'Tahap 4 · Object Placement','User tap layar → objek 3D diletakkan dan menempel di atas plane.')]
PILLS=['Feature Detection','Tracking','Plane Detection','Object Placement']
U0,U1,V0,V1,NU,NV=.12,.88,.18,.98,8,6
CU,CV=.5,.62

def chip(d,x,y,txt,font):
    w=len(txt)*6.6+16
    d.rr((x,y,x+w,y+22),6,fill=(0,0,0,170)); d.text((x+8,y+11),txt,font,(255,255,255,255),'lm')

def render(i):
    t=i/FPS
    ox,oy=off(t)
    stage=max(k for k,s in enumerate(STAGES) if t>=s[0]); ts=STAGES[stage][0]
    vp=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); draw_scene(D(vp),ox,oy)
    L=layer(); d=D(L); f11=F(11,True)
    # focus box (stage 0)
    if stage==0:
        hs=90-40*eo3(clip(t/1.5)); col=(255,255,255,230) if t<1.5 else (90,240,140,240)
        cx,cy=400,260
        for sx,sy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            x,y=cx+sx*hs,cy+sy*hs
            d.line([(x,y-sy*18),(x,y),(x-sx*18,y)],col,2.5)
    # scan line
    if 2.0<=t<5.0:
        xs=VX0+(VX1-VX0)*clip((t-2.0)/2.4); a=int(255*clip(1-(t-4.4)/.6))
        if xs<VX1+1:
            d.rect((xs-26,VY0,xs,VY1),fill=(0,220,255,int(45*a/255)))
            d.line([(xs,VY0),(xs,VY1)],(0,230,255,a),2)
    # mesh
    if 5<=t<8.6:
        a=clip((t-5)/.8)*clip(1-(t-8)/.6)
        for (p,q) in edges:
            if tapp[p]<=t and tapp[q]<=t:
                d.line([(pts[p][0]+ox,pts[p][1]+oy),(pts[q][0]+ox,pts[q][1]+oy)],(90,235,140,int(120*a)),1)
    # plane grid
    q=clip((t-8.2)/2.0) if t>=8.2 else 0
    if q>0:
        R=q*.75
        for a in range(NU):
            for b in range(NV):
                ua,ub=U0+(U1-U0)*a/NU,U0+(U1-U0)*(a+1)/NU
                va,vb=V0+(V1-V0)*b/NV,V0+(V1-V0)*(b+1)/NV
                dist=math.hypot((ua+ub)/2-CU,(va+vb)/2-CV)
                if dist<R:
                    quad=[fl(ua,va,ox,oy),fl(ub,va,ox,oy),fl(ub,vb,ox,oy),fl(ua,vb,ox,oy)]
                    d.poly(quad,fill=(0,220,255,115 if R-dist<.1 else 55),outline=(0,235,255,210),w=1.2)
        if q>=1:
            per=[fl(U0,V0,ox,oy),fl(U1,V0,ox,oy),fl(U1,V1,ox,oy),fl(U0,V1,ox,oy)]
            d.poly(per,outline=(255,255,255,int(150+90*math.sin(t*6))),w=2.2)
            x,y=fl(U0,V0,ox,oy); chip(d,x+6,y+6,'Plane terdeteksi ✓',f11)
    # tap + shadow
    px,py=fl(CU,CV,ox,oy)
    p=clip((t-11.5)/1.0) if t>=11.5 else 0
    if stage==4:
        tp=t-11.0
        if tp<.9:
            d.ell(px,py,6+40*tp/.9,6*.5+20*tp/.9,outline=(255,255,255,int(230*(1-tp/.9))),w=2)
            if tp<.4: d.ell(px,py,10,fill=(255,255,255,130))
        if p>0:
            k=max(.05,eob(p)); d.ell(px,py,40*1.15*k,20*1.1*k,fill=(0,0,0,int(95*eo3(p))))
    vp=Image.alpha_composite(vp,L)
    # points
    L=layer(); d=D(L)
    cnt=0
    for idx,pt in enumerate(pts):
        if tapp[idx]>t: continue
        cnt+=1
        x,y=pt[0]+ox,pt[1]+oy
        if t<5: col=(255,210,40); r=3.5
        elif t<8: col=(90,235,140); r=3.5
        else:
            col=(60,225,255) if pt[2]=='floor' else (150,160,175); r=3.5 if pt[2]=='floor' else 2.5
        if stage==4 and p>=1: r*=.8
        if 5<=t<8.4:
            qx,qy=off(t-.45); d.line([(pt[0]+qx,pt[1]+qy),(x,y)],col+(210,),1.6)
        age=t-tapp[idx]
        if 0<=age<.5 and stage==1:
            d.ell(x,y,3+14*age/.5,outline=col+(int(220*(1-age/.5)),),w=1.5)
        d.ell(x,y,r+1.5,fill=(20,20,30,255)); d.ell(x,y,r,fill=col+(255,))
    if stage==1: chip(d,VX0+12,VY1-30,f'Titik terdeteksi: {cnt}',f11)
    elif stage==2: chip(d,VX0+12,VY1-30,f'Titik terlacak: {cnt}',f11)
    elif stage==3: chip(d,VX0+12,VY1-30,'Titik di lantai → dikelompokkan jadi plane',f11)
    vp=Image.alpha_composite(vp,L)
    # cube
    if stage==4 and p>0:
        k=max(.05,eob(p)); drop=(1-eo3(p))*80
        d2=D(vp); cube(d2,px,py-drop,k)
        if p>=1:
            L=layer(); d=D(L); top=py-22-44
            d.line([(px+20,top+10),(px+62,top-14)],(255,255,255,220),1.2)
            chip(d,px+62,top-26,'Objek 3D menempel di plane',f11)
            vp=Image.alpha_composite(vp,L)
    # flash on stage change
    if stage>0:
        fa=int(80*clip(1-(t-ts)/.25))
        if fa>0:
            L=layer(); D(L).rect((0,0,W,H),fill=(255,255,255,fa)); vp=Image.alpha_composite(vp,L)
    img=Image.new('RGBA',(W*S,H*S),BG+(255,))
    mask=Image.new('L',(W*S,H*S),0)
    ImageDraw.Draw(mask).rounded_rectangle([VX0*S,VY0*S,VX1*S,VY1*S],radius=14*S,fill=255)
    img.paste(vp,(0,0),mask)
    d=D(img)
    d.rr((VX0,VY0,VX1,VY1),14,outline=(70,80,110),w=2)
    for sx,sy in [(0,0),(1,0),(0,1),(1,1)]:
        x=VX0+10+sx*(VX1-VX0-20); y=VY0+10+sy*(VY1-VY0-20); dx=-1 if sx else 1; dy=-1 if sy else 1
        d.line([(x,y+dy*14),(x,y),(x+dx*14,y)],(255,255,255),2)
    if int(t*2)%2==0: d.ell(VX0+24,VY0+22,4,fill=(235,60,60))
    d.text((VX0+34,VY0+22),'LIVE CAMERA',F(11,True),(255,255,255),'lm')
    # pills
    pw,gap=160,26
    for k,name in enumerate(PILLS):
        x=VX0+k*(pw+gap); cur=stage
        if cur>k+1: fc,tc=(36,120,80),(255,255,255); label='✓ '+name
        elif cur==k+1: fc,tc=(40,130,255),(255,255,255); label=name
        else: fc,tc=(44,52,74),(130,140,165); label=name
        d.rr((x,16,x+pw,46),15,fill=fc); d.text((x+pw/2,31),label,F(12,True),tc,'mm')
        if k<3: d.poly([(x+pw+8,25),(x+pw+8,37),(x+pw+18,31)],fill=(110,120,150))
    d.rect((VX0,58,VX1,61),fill=(44,52,74)); d.rect((VX0,58,VX0+(VX1-VX0)*t/DUR,61),fill=(40,130,255))
    # caption
    _,title,desc=STAGES[stage]; a=clip((t-ts)/.35)
    C=layer(); dc=D(C); yo=8*(1-a); al=int(255*a)
    dc.text((VX0,392+yo),title,F(19,True),(255,255,255,al),'la')
    dc.text((VX0,422+yo),desc,F(13),(175,188,212,al),'la')
    img=Image.alpha_composite(img,C)
    return img.convert('RGB').resize((W,H),Image.LANCZOS)

if __name__=='__main__':
    frames=[render(i) for i in range(N)]
    mont=Image.new('RGB',(W,H*5))
    for k,tt in enumerate([1,3.5,6.5,9.5,13]): mont.paste(frames[int(tt*FPS)],(0,k*H))
    pal=mont.quantize(colors=255,method=Image.MEDIANCUT)
    out=[f.quantize(palette=pal,dither=0) for f in frames]
    out[0].save('AR_Pipeline_Animation.gif',save_all=True,append_images=out[1:],duration=80,loop=0,optimize=False)
    sheet=Image.new('RGB',(W*2,H*3))
    for k,tt in enumerate([1,3.5,6.5,9.5,11.8,13.5]): sheet.paste(frames[int(tt*FPS)],((k%2)*W,(k//2)*H))
    sheet.save('sheet.png')
    print('ok')
