"""Render the positive-prefix examples and package the offline explorer."""

import math
from fractions import Fraction as F
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
W, H = 704, 835
BG, PANEL, EDGE = "#101b32", "#162640", "#3a5477"
TEXT, MUTED = "#f7faff", "#bdc9dc"
MINT, AMBER, RED = "#6aead7", "#ffd086", "#ffb8ae"


def label(draw, xy, message, size, color=TEXT, anchor="lt"):
    draw.text(xy, message, font=ImageFont.load_default(size=size), fill=color, anchor=anchor)


def prism(draw, x, y, angle, name, tone):
    width = 33
    dx = 16 * math.cos(angle)
    top = [(x-width,y-28),(x+dx,y-47),(x+width,y-28),(x-dx,y-8)]
    left = [top[0],top[3],(x-dx,y+21),(x-width,y+2)]
    right = [top[3],top[2],(x+width,y+2),(x-dx,y+21)]
    colors = {"base":("#456281","#263c5b","#5c7697"),
              "on":("#197770","#265b5d","#53bfb2"),
              "surge":("#a87d4a","#74593e","#efb56a")}
    for points, shade in zip((left,right,top),colors[tone]):
        draw.polygon(points,fill=shade,outline="#142139")
    label(draw,(x,y-27),name,26,TEXT,"mm")


def graph(draw, angle, rate, share):
    offset = 16 * math.cos(angle)
    depth = 10 * math.sin(angle)
    start = (352,314)
    terminal = [(152+offset,451+depth),(352-offset,451),(552+offset,451-depth)]
    for j,(x,y) in enumerate(terminal):
        weight = 1-share if j == 0 else share/2
        tone = (AMBER if j == 0 else MINT if j == 1 else MUTED) if weight else "#435673"
        draw.line((start,(x,y-34)),fill=tone,width=6 if weight else 3)
    prism(draw,*start,angle,"s","base")
    captions = (f"effect {rate}","effect 1/2","effect 0")
    for j,(x,y) in enumerate(terminal):
        prism(draw,x,y,angle,"ztf"[j],("surge","on","base")[j])
        label(draw,(x,y+31),captions[j],24,AMBER if j==0 else MINT if j==1 else MUTED,"mt")
    label(draw,(88,362),"A",24,AMBER)
    label(draw,(589,363),"B splits",23,MUTED,"rt")


def frame(angle, scene):
    rate, share = [(F(1,2),F(0)),(F(1,2),F(1,2)),(F(3,4),F(1,2))][scene]
    mass = share / 2
    overall = (1-share)*rate+share/4
    relaxed = max(F(3,4),F(1,2)+rate)
    assert [(mass,overall,relaxed)] == [
        [(F(0),F(1,2),F(1))],[(F(1,4),F(3,8),F(1))],[(F(1,4),F(1,2),F(5,4))]
    ][scene]
    verdicts = ("No positive-mass word","Strictly raises the probability","Positive-mass equality violates")
    notes = ("A attains the relaxed tie off the word.",
             "On the word, effect chance is 1/2.",
             "On the word and overall, both are 1/2.")
    tint = (AMBER,MINT,RED)[scene]
    im = Image.new("RGB",(W,H),BG)
    d = ImageDraw.Draw(im)
    label(d,(36,39),"CO-SAFETY STRICT PROBABILITY RAISING",23,MINT)
    label(d,(34,84),"When does equality count?",47)
    label(d,(36,153),"The cause word is s followed by t.",29,MUTED)
    d.rounded_rectangle((32,208,672,537),21,fill=PANEL,outline=EDGE,width=2)
    label(d,(53,234),"At s, choose A or B",27,MUTED)
    graph(d,angle,rate,share)
    d.rounded_rectangle((32,557,672,801),21,fill=PANEL,outline=EDGE,width=2)
    label(d,(55,580),f"Choose B with probability {share}",28,MUTED)
    label(d,(55,629),f"Word mass  {mass}",30)
    label(d,(646,629),f"Overall effect  {overall}",30,TEXT,"rt")
    label(d,(55,677),verdicts[scene],35,tint)
    label(d,(55,730),notes[scene],25,MUTED)
    label(d,(55,768),f"Relaxed optimum: {relaxed}",23,MUTED)
    return im.convert("P",palette=Image.Palette.ADAPTIVE,colors=64)


def main():
    total = 72
    frames = [frame(2*math.pi*i/total,i//24) for i in range(total)]
    frames[0].save(HERE/"first-deviation.gif",save_all=True,append_images=frames[1:],
                   loop=0,duration=185,optimize=True)
    with ZipFile(HERE/"first-deviation-explorer.zip","w") as archive:
        for name in ("README.md","index.html"):
            info = ZipInfo(name,(1980,1,1,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info,(HERE/name).read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__ == "__main__":
    main()
