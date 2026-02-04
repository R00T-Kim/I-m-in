#!/usr/bin/env python3
"""Parse MIC1103 text firmware records and emit stats/CSV.

Usage:
  ./parse_records.py --input MIC110301_v2.3.14.txt --outdir out
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv
from collections import Counter

def load_records(path: Path):
    lines=[l.strip() for l in path.read_text().splitlines() if l.strip()]
    return lines

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--outdir', required=True)
    args=ap.parse_args()
    inp=Path(args.input)
    outdir=Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    recs=load_records(inp)
    lengths=Counter(len(r) for r in recs)
    types=Counter()
    for r in recs:
        if r.startswith('110301') and len(r)>=8:
            types[r[6:8]]+=1
        else:
            types[r[:2]]+=1

    # write stats
    (outdir/'stats.txt').write_text(
        'lines=%d\n'%len(recs)+
        'lengths='+' '.join(f'{k}:{v}' for k,v in sorted(lengths.items()))+'\n'+
        'types='+' '.join(f'{k}:{v}' for k,v in types.most_common())+'\n'
    )

    # export per-record summary
    with (outdir/'records.csv').open('w', newline='') as f:
        w=csv.writer(f)
        w.writerow(['idx','type','len','payload_hex'])
        for i,r in enumerate(recs):
            t=r[6:8] if r.startswith('110301') and len(r)>=8 else r[:2]
            payload=r[8:] if r.startswith('110301') and len(r)>=8 else r[2:]
            w.writerow([i,t,len(r),payload])

if __name__=='__main__':
    main()
