#!/usr/bin/env python3
"""Attempt DA->DD segment mapping and emit candidate table.

Usage:
  ./dd_da_map.py --input MIC110301_v2.3.14.txt --outdir out
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv

def parse_records(path: Path):
    return [l.strip() for l in path.read_text().splitlines() if l.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--outdir', required=True)
    args=ap.parse_args()
    outdir=Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    recs=parse_records(Path(args.input))
    DA=[r for r in recs if r.startswith('110301DA')]
    DD=[r for r in recs if r.startswith('110301DD')]

    # parse DA: 7 bytes payload -> addr(3), len(2), tail(2)
    da_rows=[]
    for r in DA:
        b=bytes.fromhex(r[8:])
        if len(b)!=7: continue
        addr=b[0]<<16 | b[1]<<8 | b[2]
        seglen=b[3]<<8 | b[4]
        tail=b[5:]  # maybe checksum
        da_rows.append((r,addr,seglen,tail.hex()))

    # parse DD: payload first 4 bytes as hi16/lo16
    dd_rows=[]
    for r in DD:
        b=bytes.fromhex(r[8:])
        if len(b)<4: continue
        hi16=(b[0]<<8)|b[1]
        lo16=(b[2]<<8)|b[3]
        dd_rows.append((r,hi16,lo16,len(b)))

    # naive mapping: sequentially assign DD blocks after each DA by count guessed from seglen
    # This is heuristic; adjust manually later.
    out=[]
    dd_idx=0
    for r,addr,seglen,tail in da_rows:
        # guess bytes per DD block
        blocks=[]
        # assign up to 2 blocks if seglen large, else 1
        n=2 if seglen>=256 else 1
        for _ in range(n):
            if dd_idx>=len(dd_rows): break
            blocks.append(dd_rows[dd_idx])
            dd_idx+=1
        out.append((r,addr,seglen,tail,blocks))

    with (outdir/'da_dd_map.csv').open('w', newline='') as f:
        w=csv.writer(f)
        w.writerow(['da_record','da_addr','da_len','da_tail','dd_record','dd_hi16','dd_lo16','dd_len'])
        for r,addr,seglen,tail,blocks in out:
            if not blocks:
                w.writerow([r,addr,seglen,tail,'','','',''])
            else:
                for ddrec,hi16,lo16,ddlen in blocks:
                    w.writerow([r,addr,seglen,tail,ddrec,hi16,lo16,ddlen])

if __name__=='__main__':
    main()
