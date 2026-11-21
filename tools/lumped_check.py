import math
rho,c,mu=1.14,350.0,1.9e-5
def resp(V_ml,d_mm,L_mm,f,P0,K=1.5,kappa=2.0):
    r=d_mm/2e3; A=math.pi*r*r; L=L_mm/1e3; Le=L+1.7*r; V=V_ml*1e-6; w=2*math.pi*f
    M=rho*Le/A; C=V/(rho*c*c); X=w*M-1/(w*C)
    Rl=max(8*mu*L/(math.pi*r**4),(L/(math.pi*r**3))*math.sqrt(2*rho*mu*w))+rho*w*w/(2*math.pi*c)
    R2=K*rho/(2*A*A); k=8/(3*math.pi)*R2
    lo,hi=0,P0/math.sqrt(Rl*Rl+X*X)
    for _ in range(80):
        q=(lo+hi)/2
        if q*math.sqrt((Rl+k*q)**2+X*X)>P0: hi=q
        else: lo=q
    q=lo; Vs=q/w; Vin=2*Vs; L0=Vin/A; eta=1-math.exp(-L0/(kappa*d_mm/1e3))
    Qex=eta*Vin*f
    f0=c/(2*math.pi)*math.sqrt(A/(V*Le))
    return dict(f0=f0,Q=q,Vin_ul=Vin*1e9,L0_d=L0/(d_mm/1e3),eta=eta,Qex_mlps=Qex*1e6,tau_s=V/Qex if Qex>0 else 1e9, Qfac=math.sqrt(M/C)/(Rl+k*q))
for d in [0.8,1.29,1.9,2.1,2.4,3,4]:
    r=resp(15,d,8,200,100); print(d, {k:round(v,3) for k,v in r.items()})
print()
for P0 in [10,30,100,300]:
    r=resp(12,2.4,8,150,P0); print(P0,{k:round(v,3) for k,v in r.items()})
