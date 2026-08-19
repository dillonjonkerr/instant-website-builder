#!/usr/bin/env python3
"""PDF text extractor that reconstructs rows using text-matrix positions.

Zero-dependency fallback for machines without poppler/pypdf. Handles
FlateDecode streams, object streams, and ToUnicode CMaps (the encoding
Semrush export PDFs use). Groups text runs into lines by their y position
and inserts tabs on large x gaps so tables stay readable.

Usage: python3 pdf_extract.py report.pdf > report.txt
"""
import re, sys, zlib
from collections import defaultdict

path = sys.argv[1]
data = open(path, 'rb').read()
objs = {}

def stream_of(body):
    m = re.search(rb'stream\r?\n', body)
    if not m: return None
    raw = body[m.end():]
    e = raw.rfind(b'endstream')
    if e >= 0: raw = raw[:e]
    if b'/FlateDecode' in body:
        try: return zlib.decompress(raw)
        except Exception:
            try: return zlib.decompressobj().decompress(raw)
            except Exception: return None
    return raw

for m in re.finditer(rb'(\d+)\s+(\d+)\s+obj\b', data):
    end = data.find(b'endobj', m.end())
    objs[int(m.group(1))] = data[m.end():end if end > 0 else len(data)]

for num, body in list(objs.items()):
    if b'/ObjStm' not in body: continue
    dec = stream_of(body)
    if not dec: continue
    try:
        n = int(re.search(rb'/N\s+(\d+)', body).group(1))
        first = int(re.search(rb'/First\s+(\d+)', body).group(1))
    except Exception: continue
    hdr = dec[:first].split()
    for i in range(n):
        try:
            onum, off = int(hdr[2*i]), int(hdr[2*i+1])
        except Exception: break
        nxt = int(hdr[2*i+3]) if 2*i+3 < len(hdr) else len(dec)-first
        objs.setdefault(onum, dec[first+off: first+nxt])

def parse_cmap(txt):
    cm = {}
    for blk in re.findall(rb'beginbfchar(.*?)endbfchar', txt, re.S):
        for s, d in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            cm[int(s,16)] = bytes.fromhex(d.decode()).decode('utf-16-be','replace')
    for blk in re.findall(rb'beginbfrange(.*?)endbfrange', txt, re.S):
        for lo, hi, d in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            lo, hi, base = int(lo,16), int(hi,16), int(d,16)
            for k in range(lo, hi+1): cm[k] = chr(base + k - lo)
    return cm

font_cmaps = {}
for num, body in objs.items():
    m = re.search(rb'/ToUnicode\s+(\d+)\s+\d+\s+R', body)
    if not m: continue
    tu = objs.get(int(m.group(1)))
    if tu:
        d = stream_of(tu)
        if d: font_cmaps[num] = parse_cmap(d)

name_to_cmap = {}
for num, body in objs.items():
    for nm, ref in re.findall(rb'/([A-Za-z0-9#_.+-]+)\s+(\d+)\s+\d+\s+R', body):
        if int(ref) in font_cmaps: name_to_cmap[nm] = font_cmaps[int(ref)]

def decode(seg, cmap):
    out = []
    for tok in re.finditer(rb'<([0-9A-Fa-f\s]*)>|\(((?:\\.|[^\\()])*)\)', seg):
        if tok.group(1) is not None:
            h = re.sub(rb'\s', b'', tok.group(1))
            step = 4 if (len(h) % 4 == 0 and cmap and max(cmap)>255) else 2
            if cmap:
                for i in range(0, len(h), step):
                    out.append(cmap.get(int(h[i:i+step],16), ''))
        else:
            out.append(tok.group(2).replace(b'\\(',b'(').replace(b'\\)',b')').decode('latin-1'))
    return ''.join(out)

TOK = re.compile(
    rb'/([A-Za-z0-9#_.+-]+)\s+[\d.]+\s+Tf'
    rb'|([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm'
    rb'|([-\d.]+)\s+([-\d.]+)\s+T[dD]'
    rb'|(\[(?:\\.|[^\]])*\]\s*TJ|\((?:\\.|[^\\()])*\)\s*Tj|<[0-9A-Fa-f\s]*>\s*Tj)'
    rb'|(BT|T\*)')

for pnum, (num, body) in enumerate(sorted(objs.items())):
    dec = stream_of(body)
    if not dec or b'Tf' not in dec: continue
    if b'Tj' not in dec and b'TJ' not in dec: continue
    rows = defaultdict(list)
    cm = None; x = y = 0.0
    for m in TOK.finditer(dec):
        if m.group(1):
            cm = name_to_cmap.get(m.group(1))
        elif m.group(2) is not None:
            x, y = float(m.group(6)), float(m.group(7))
        elif m.group(8) is not None:
            x += float(m.group(8)); y += float(m.group(9))
        elif m.group(10):
            t = decode(m.group(10), cm)
            if t: rows[round(y, 0)].append((x, t))
    if not rows: continue
    print(f"\n=================== CONTENT BLOCK (obj {num}) ===================")
    for yy in sorted(rows, reverse=True):
        cells = sorted(rows[yy], key=lambda p: p[0])
        # join glyphs; insert tab when x-gap is large (column boundary)
        line, prevx = [], None
        for xx, t in cells:
            if prevx is not None and xx - prevx > 13: line.append('\t')
            line.append(t); prevx = xx
        s = ''.join(line).strip()
        if s: print(s)
