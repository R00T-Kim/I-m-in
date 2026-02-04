#!/usr/bin/env python3
"""Analyze EE records (18-byte and 6-byte) and print distributions.

Usage:
  ./ee_analyze.py --input MIC110301_v2.3.14.txt --outdir out
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv
from collections import Counter

def load_recs(path: Path):
    return [l.strip() for l in path.read_text().splitlines() if l.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--outdir', required=True)
    args=ap.parse_args()
    outdir=Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    recs=load_recs(Path(args.input))
    EE=[r for r in recs if r.startswith('110301EE')]
    lens=Counter(len(r) for r in EE)

    pos_counts=[Counter() for _ in range(9)]
    short=[]
    table_rows=[]
    for r in EE:
        payload=bytes.fromhex(r[8:])
        if len(payload)==18:
            words=[int.from_bytes(payload[i:i+2],'big') for i in range(0,18,2)]
            for i,w in enumerate(words):
                pos_counts[i][w]+=1
            pos2,pos3,pos4,pos6,pos8=words[2],words[3],words[4],words[6],words[8]
            table_rows.append((pos2,pos3,pos4,pos6,pos8))
        else:
            short.append(payload.hex())

    # stats
    lines=['EE count=%d'%len(EE),'EE lens='+str(dict(lens))]
    for i,c in enumerate(pos_counts):
        if c:
            lines.append(f'pos{i} top: '+str(c.most_common(5)))
    (outdir/'ee_stats.txt').write_text('\n'.join(lines))

    # table
    with (outdir/'ee_table.csv').open('w', newline='') as f:
        w=csv.writer(f)
        w.writerow(['pos2','pos3','pos4','pos6','pos8','offset'])
        for pos2,pos3,pos4,pos6,pos8 in table_rows:
            w.writerow([pos2,pos3,pos4,pos6,pos8,pos8-pos2])

    if short:
        (outdir/'ee_short.txt').write_text('\n'.join(short))

if __name__=='__main__':
    main()
