#!/usr/bin/env python3
"""Exhaustive check of non-injective guard-closed alpha for 45 threshold vectors.
This is a finite two-sensor operational instance at the RCRA clause interface;
NOT a proof of coverage for unrestricted L-DINF models.
"""
from collections import defaultdict,deque
from itertools import product

LEVELS=range(5)
STAGES=('observed','pending','committed','delegated','finished')
VARIANTS=('A','B')
C0=('init',None); CLOSED=('closed',None)

def alpha(c): return c[0]
def observed(c):
    # Only semantic observations used by this finite application.
    return frozenset({'committed'} if c[0] in ('committed','delegated','finished') else set()) | \
           frozenset({'completed'} if c[0]=='finished' else set()) | \
           frozenset({'pending'} if c[0]=='pending' else set())

def concrete_edges(c,x):
    s,m,p=x;stage,src=c
    if stage=='init': return [('observe',('observed',sensor)) for sensor in VARIANTS]
    if stage=='observed':
        if s>3: return [('source_reject',CLOSED)]
        if m<=2: return [('autonomous_commit',('committed',src))]
        return [('review_request',('pending',src))]
    if stage=='pending': return [('senior_validate',('committed',src))]
    if stage=='committed':
        if p<=2: return [('autonomous_execute',('finished',src))]
        return [('delegate',('delegated',src))]
    if stage=='delegated': return [('senior_execute',('finished',src))]
    return []

def abstract_edges(q,x):
    s,m,p=x
    if q=='init': return [('observe','observed')]
    if q=='observed':
        if s>3: return [('source_reject','closed')]
        if m<=2: return [('autonomous_commit','committed')]
        return [('review_request','pending')]
    if q=='pending':return [('senior_validate','committed')]
    if q=='committed':
        if p<=2: return [('autonomous_execute','finished')]
        return [('delegate','delegated')]
    if q=='delegated':return [('senior_execute','finished')]
    return []

def reachable(start, successor):
    found={start};todo=deque([start])
    while todo:
        for _,nxt in successor(todo.popleft()):
            if nxt not in found:found.add(nxt);todo.append(nxt)
    return found

def check(x):
    C=reachable(C0,lambda c:concrete_edges(c,x))
    Q=reachable('init',lambda q:abstract_edges(q,x))
    assert {alpha(c) for c in C}==Q
    assert alpha(C0)=='init'
    for c in C:
        q=alpha(c)
        assert observed(c)==observed((q,None))
        l={(e,alpha(d)) for e,d in concrete_edges(c,x)}
        r=set(abstract_edges(q,x))
        assert l==r,(x,c,l,r)
    return len(C),len(Q)

def main():
    result=[(x,check(x)) for x in product(LEVELS,(2,3,4),(2,3,4))]
    assert len(result)==45
    assert check((3,3,3))==(11,6)
    print('PASS: all 45 admissible threshold vectors satisfy observation, surjectivity, and both event-step inclusions.')
    print('At (s,m,p)=(3,3,3):',check((3,3,3)),'reachable concrete/abstract states; alpha is non-injective.')
    from collections import Counter
    print('Reachable state-size distributions:',Counter(size for _,size in result))
if __name__=='__main__':main()
