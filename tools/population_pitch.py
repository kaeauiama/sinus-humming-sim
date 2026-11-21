# Population of sinus geometries x humming strategies (lumped model). Run: python tools/population_pitch.py
# Mixing law: the 3D refit of 2026-11-21 (results/deadspace_law_fit.md); LAW=2d uses the old 2D law it was first run with.
# P0 (default 200 = calibrated effective pressure), VOL=normal: the old normal maxillary volumes instead of NasalSeg.
# The first run (results/population_pitch.md, "old") is LAW=2d VOL=normal P0=100; note the sampling differs since
# the NasalSeg draw was added before the other sinuses, so per-person values are not identical, only the distributions.
import os
import numpy as np
rho,c,mu,K=1.14,350.0,1.9e-5,1.5
a_dv,m_dv=0.60,0.70
MIX=dict(m=0.695,x0=1.68,n=1.76,k=1.15,p=0.57,lam=48.0)
def sat(v,v0,n): return 1-np.exp(-np.power(np.maximum(v,0)/v0,n))
def mixlaw(x,ld):
    if os.environ.get('LAW')=='2d': return m_dv*np.maximum(0,1-a_dv/np.maximum(x,1e-9))
    return MIX['m']*sat(x,MIX['x0'],MIX['n'])*sat(x*ld,MIX['k'],MIX['p'])*np.exp(-ld/MIX['lam'])
def rate(V,d,L,f,P0):
    r=d/2e3; A=np.pi*r*r; Lm=L/1e3; Le=Lm+1.7*r; Vm=V*1e-6; w=2*np.pi*f
    M=rho*Le/A; C=Vm/(rho*c*c); X=w*M-1/(w*C)
    Rl=np.maximum(8*mu*Lm/(np.pi*r**4),(Lm/(np.pi*r**3))*np.sqrt(2*rho*mu*w))+rho*w*w/(2*np.pi*c)
    k=(8/(3*np.pi))*K*rho/(2*A*A)
    lo=np.zeros_like(V); hi=P0/np.sqrt(Rl*Rl+X*X)
    for _ in range(60):
        q=(lo+hi)/2; big=q*np.sqrt((Rl+k*q)**2+X*X)>P0
        hi=np.where(big,q,hi); lo=np.where(big,lo,q)
    Vin=2*lo/w; L0=Vin/A
    eta=mixlaw(L0/Lm,Lm/(2*r))
    return eta*Vin*f/Vm
def f0(V,d,L):
    r=d/2e3; A=np.pi*r*r; Le=L/1e3+1.7*r
    return c/(2*np.pi)*np.sqrt(A/(V*1e-6*Le))
rng=np.random.default_rng(1); N=4000
def clipn(m,s,lo,hi): return np.clip(rng.normal(m,s,N),lo,hi)
# maxillary volumes: NasalSeg 130 cases (both sides, results/nasalseg_maxillary_volumes.csv) unless VOL=normal
def nasalseg_volumes():
    import os as _os
    p=_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),'results','nasalseg_maxillary_volumes.csv')
    v=[]
    for line in open(p,encoding='utf-8'):
        if line.startswith('#') or line.startswith('case'): continue
        c=line.split(','); v+= [float(c[1]),float(c[2])]
    v=np.array(v); return v[v>1.0]          # drop aplastic/missing labels (< 1 mL)
VMX=clipn(12.75,4.38,4,30) if os.environ.get('VOL')=='normal' else rng.choice(nasalseg_volumes(),N,replace=True)
pop={
 'maxillary':dict(V=VMX,d=clipn(3.0,0.75,1,6),L=rng.uniform(1.5,4,N)),
 # literature (results/sinus_dimensions_literature.md): sphenoid V 4.00 +- 1.99 mL (Cohen 2018), ostium 2.2 +- 0.5 mm
 # (CBCT); frontal V 2.92 +- 2.57 mL (Cohen 2018), ostium AP 7.5 +- 2.7 mm (2-15); ethmoid 9 cells per side holding
 # 3.4-8 mL in all -> 0.3-0.9 mL per cell. Wall / channel lengths L are not measured in the literature we found.
 'sphenoid':dict(V=clipn(4.0,2.0,0.8,12),d=clipn(2.2,0.5,0.8,5),L=rng.uniform(1,3,N)),
 'frontal':dict(V=clipn(2.9,2.6,0.3,15),d=clipn(7.5,2.7,2,15),L=rng.uniform(2,8,N)),
 'ethmoid':dict(V=rng.uniform(0.3,0.9,N),d=rng.uniform(1,2.5,N),L=rng.uniform(1,3,N)),
}
for nm,p in pop.items():
    F=f0(p['V'],p['d'],p['L']); print(f"{nm:10s} f0 median {np.median(F):6.0f} Hz  10-90%: {np.percentile(F,10):5.0f}-{np.percentile(F,90):5.0f}  in 100-300Hz: {np.mean((F>100)&(F<300))*100:4.1f}%")
# Defaults follow the pages (2026-11-21): P0 = 130 Pa at the maxillary ostium (two-compartment calibration), other
# ostia scaled by their pressure ratio (results/ostium_pressure.json; OSTP=0 turns it off), and the exchanged fraction
# from the two-compartment washout (near half + far half mixing on 40 s; TWO=0 gives the one-box 1 - exp(-kT)).
import json as _json
P0=float(os.environ.get('P0',130)); T=10
_op=_json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'results','ostium_pressure.json')))
KEY={'maxillary':None,'sphenoid':'sph','frontal':'fro','ethmoid':'eth'}
def G(nm,f):
    k=KEY[nm]
    if k is None or os.environ.get('OSTP')=='0': return 1.0
    return float(np.interp(np.log(f),np.log(_op['freqs_hz']),_op['g'][k]))
def exch(k):
    if os.environ.get('TWO')=='0': return 1-np.exp(-T*k)
    fn,ti=0.5,40.0; a=1/ti/(1-fn); b=1/ti/fn; n=np.ones_like(k); fa=np.ones_like(k); h=0.02
    for _ in range(int(T/h)):
        dn=-(k/fn)*n+b*(fa-n); df=a*(n-fa); n=n+h*dn; fa=fa+h*df
    return 1-(fn*n+(1-fn)*fa)
print(f'\nP0 = {P0:.0f} Pa at the maxillary ostium, ostium pressure ratios {"off" if os.environ.get("OSTP")=="0" else "on"}, '
      f'{"one box" if os.environ.get("TWO")=="0" else "two compartments"}, maxillary volumes: {"normal 12.75 +- 4.38 mL" if os.environ.get("VOL")=="normal" else "NasalSeg 130 cases"}')
fs=np.arange(100,301,5)
def session(nm,p,strategy,beta=None):
    if beta is None:
        ks=np.array([rate(p['V'],p['d'],p['L'],f,P0*G(nm,f)) for f in fs])  # (nf,N)
    else:
        ks=np.array([sum(rate(p['V'],p['d'],p['L'],n*f,P0*n**(-beta)*G(nm,n*f)) for n in range(1,7)) for f in fs])
    res={}
    for fc in (120,150,200,250,300):
        res[f'const{fc}']=exch(ks[list(fs).index(fc)])
    res['sweep100-300']=exch(ks.mean(0))
    lowmask=fs<=200
    res['sweep100-200']=exch(ks[lowmask].mean(0))
    res['best_const']=exch(ks.max(0))
    return res
for beta in (None,2.0,1.0):
    print('\n=== harmonics:', 'fundamental only' if beta is None else f'6 harmonics, amplitude n^-{beta}')
    for nm,p in pop.items():
        r=session(nm,p,None,beta)
        line=' '.join(f"{k}:{np.median(v)*100:4.0f}%" for k,v in r.items())
        better=np.mean(r['sweep100-200']>r['const150'])*100
        print(f"{nm:10s} {line} | sweep100-200 > const150 for {better:.0f}%")
# spread between people: 10 s at 150 Hz with weak harmonics, plus diffusion-only time constants
print('\n=== spread between people (10 s at 150 Hz, harmonics n^-2): 10 / 50 / 90 percentiles')
for nm,p in pop.items():
    v=session(nm,p,None,2.0)['const150']*100
    r=p['d']/2e3; A=np.pi*r*r; Le=p['L']/1e3+1.7*r; tauD=p['V']*1e-6*Le/(2e-5*A)
    print(f"{nm:10s} exchanged by humming {np.percentile(v,10):4.0f} / {np.percentile(v,50):4.0f} / {np.percentile(v,90):4.0f} %   diffusion time constant {np.percentile(tauD,10):5.0f} / {np.percentile(tauD,50):5.0f} / {np.percentile(tauD,90):5.0f} s")
