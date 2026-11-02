"""Render the profile's looping particle banner without browser dependencies."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
W, H, SCALE = 1440, 336, 1440 / 1200
FPS, SECONDS = 12.5, 16
cam = np.array([1.2629783123, 2.6646064714, -1.8178993743])
f = -cam / np.linalg.norm(cam)
r = np.cross(f, [0,1,0]); r /= np.linalg.norm(r)
u = np.cross(r, f)
axis = np.arange(0,512,3) / 511 * 20 - 10
x,z = np.meshgrid(axis,axis); valid = x*x+z*z < 25
x,z = x[valid],z[valid]
def wave(x,z,t):
    return (np.sin(x*2+t)*np.cos(z*1.5+t)+np.sin(x*3.2+t*2)*np.cos(z*2.1+t)*.6+np.sin(x*1.7+t)*np.cos(z*2.8+t*3)*.4+np.sin(x*z*.5+t*2)*.3)*.3
def smooth(a,b,v):
    q=np.clip((v-a)/(b-a),0,1);return q*q*(3-2*q)
noise=wave(x*4,z*4,0)
hashvalue=np.mod(np.sin(x*127.1+z*74.7)*43758.5453,1)
Y,X=np.mgrid[:H,:W]
# The animation contains only particles; all profile copy is native README text.
scrim=smooth(0,35*SCALE,Y)*(1-smooth(245*SCALE,280*SCALE,Y))
palette=[]
for i in range(64):palette.extend([round(i*255/63)]*3)
palette += [112,137,186] + [0,0,0]*191
pal=Image.new('P',(1,1));pal.putpalette(palette)
frames=[]
for frame in range(round(FPS*SECONDS)):
    t=frame/FPS*2*math.pi/SECONDS
    pos=np.column_stack([x+wave(x*.6,z*.6,t)*.52,wave(x*.6+50,z*.6,t+2.094)*.52,z+wave(x*.6,z*.6,t+4.188)*.52])
    delta=pos-cam;depth=np.sum(delta*f,axis=1)
    safe=np.maximum(depth,.01)
    sx=600+(np.sum(delta*r,axis=1))/(.4663076582*safe)*365
    sy=365-(np.sum(delta*u,axis=1))/(.4663076582*safe)*365
    dist=np.abs(3.8-depth)
    reveal=1-smooth(3.8+noise*.3,4.1+noise*.3,np.linalg.norm(pos[:,[0,2]],axis=1))
    sparkle=(np.sin(t+hashvalue*2*math.pi)*.5+np.sin(t*2+hashvalue*4*math.pi)*.3+np.sin(t*3+hashvalue*6*math.pi)*.2+1)*.5
    bright=.7+(sparkle*(1-sparkle**2)+sparkle**4*sparkle**2)*1.3
    alpha=(1.04-np.clip(dist,0,1))*smooth(-.5,.25,pos[:,1])*.8*reveal*bright
    alpha*=1-smooth(.4,1.9,((sx/1200-.5)*2)**2+((sy/730-.5)*2)**2)
    px=sx*SCALE;py=(sy*.5-45)*SCALE
    radius=np.minimum(np.maximum(dist*17.9,3)/4,5)*SCALE
    mask=(depth>.01)&(px>-40)&(px<W+40)&(py>-40)&(py<H+40)&(alpha>.004)
    image=Image.new('L',(W,H));draw=ImageDraw.Draw(image)
    for a,b,c,v in zip(px[mask],py[mask],radius[mask],alpha[mask]):
        draw.ellipse((a-c,b-c,a+c,b+c),fill=min(140,round(v*180)))
    array=(np.asarray(image)*scrim).astype('uint8')
    image=Image.fromarray(array).convert('RGBA')
    frames.append(image.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE))
    if frame%60==0: print(f'Rendered {frame}/{round(FPS*SECONDS)} frames',flush=True)
output=ROOT/'assets/profile-particles.gif'
frames[0].save(output,save_all=True,append_images=frames[1:],duration=round(1000/FPS),loop=0,optimize=False,disposal=2,transparency=None)
check=Image.open(output)
assert check.n_frames==round(FPS*SECONDS) and check.info['loop']==0
# Every decoded frame must exactly match its source. This catches disposal,
# palette, and delta-frame artifacts rather than just checking frame count.
for index in [0,1,25,75,len(frames)-1]:
    check.seek(index)
    assert np.array_equal(np.asarray(check.convert('RGB')),np.asarray(frames[index].convert('RGB'))),f'Decoded frame {index} differs'
check.seek(0);first=np.asarray(check.convert('RGB'))
check.seek(75);assert np.mean(np.abs(np.asarray(check.convert('RGB')).astype(float)-first))>.5
print(f'Created {output.name}: {check.n_frames} frames, {output.stat().st_size/1024/1024:.2f} MiB',flush=True)
frames[0].convert('RGB').save('/private/tmp/banner-animated-first.png')
frames[75].convert('RGB').save('/private/tmp/banner-animated-later.png')
