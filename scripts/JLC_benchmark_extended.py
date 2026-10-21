#!/usr/bin/env python3
"""Finite synthetic guard-template benchmark, NOT an L-DINF/RCRA implementation.
Three families: favourable (binary outcomes); mixed (some five-way tests);
and distinct (five distinct comparison outcomes per coordinate).
Use: python JLC_benchmark_extended.py --output JLC_benchmark_extended.csv
"""
import argparse, csv, itertools, time
from collections import deque
L = tuple(range(5))

def template(n, family):
    assert family in ('favourable','mixed','distinct')
    kinds = tuple('SMP'[i%3] for i in range(n))
    m = n if family == 'favourable' else n//2 if family == 'mixed' else 0
    return kinds, tuple(i < m for i in range(n))

def allowed(k):
    return (0,1,2) if k == 'S' else (3,4)

def profile(x, must):
    return ('low' if x <= 2 else 'high') if must else x

def instantiate(x, kinds, mandatory, nondet=3):
    """Construct labelled reachable graph; check AG(not bad) and AF(final)."""
    n = len(x)
    init = ('stage',0)
    reached = {init}; todo = deque([init]); edge_count = 0
    while todo:
        q = todo.popleft(); outgoing = []
        if q[0]=='stage' and q[1]<n:
            i=q[1]
            if mandatory[i]:
                good = x[i] in allowed(kinds[i])
                if not good:
                    outgoing=[('reject_or_unsafe',('bad',i))]
                else:
                    if kinds[i]=='S': outgoing=[('admit',('stage',i+1))]
                    else: outgoing=[('route',('pending',i))]
            else:
                outgoing=[(f'grade_{x[i]}_env_{j}',('choice',i,j,x[i])) for j in range(nondet)]
        elif q[0]=='pending':
            i=q[1]
            outgoing=[(f'validator_{j}',('choice',i,j,'trusted')) for j in range(2)]
        elif q[0]=='choice':
            outgoing=[('continue',('stage',q[1]+1))]
        for ev,d in outgoing:
            edge_count += 1
            if d not in reached:
                reached.add(d); todo.append(d)
    good = not any(q[0]=='bad' for q in reached) and ('stage',n) in reached
    return good,len(reached),edge_count

def candidates(n, family, method):
    kinds, mandatory=template(n,family)
    domains=[]
    for k,m in zip(kinds,mandatory):
        if method=='naive': ds=L
        elif method=='signature': ds=(2,3) if m else L
        elif method=='pruned': ds=allowed(k) if m else L
        else: raise ValueError(method)
        domains.append(ds)
    return itertools.product(*domains)

def run(n, family, method):
    kinds,mandatory=template(n,family)
    start=time.perf_counter(); built=good_count=total_states=total_edges=0
    for x in candidates(n,family,method):
        g,s,e=instantiate(x,kinds,mandatory)
        built+=1; good_count+=g; total_states+=s; total_edges+=e
    return dict(family=family,n=n,mandatory=sum(mandatory),neutral=n-sum(mandatory),method=method,
        graph_builds=built,feasible_representatives=good_count,
        states_constructed=total_states,edges_constructed=total_edges,
        wall_seconds=round(time.perf_counter()-start,5))

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',default='JLC_benchmark_extended.csv'); a=p.parse_args()
    out=[]
    for family in ('favourable','mixed','distinct'):
        for n in (4,6,7):
            kinds,mandatory=template(n,family)
            naive=5**n
            sig=(2**sum(mandatory))* (5**(n-sum(mandatory)))
            filtered=1
            for k,m in zip(kinds,mandatory): filtered*=len(allowed(k)) if m else 5
            expected={'naive':naive,'signature':sig,'pruned':filtered}
            for method in ('naive','signature','pruned'):
                row=run(n,family,method)
                assert row['graph_builds']==expected[method],(row,expected)
                expected_feasible = (5**(n-sum(mandatory)) if method=='signature' else filtered)
                assert row['feasible_representatives']==expected_feasible, (row,expected_feasible)
                out.append(row)
                print(family,n,method,row['graph_builds'],row['feasible_representatives'],flush=True)
    with open(a.output,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
if __name__=='__main__':main()
