import math
rho,c,mu=1.14,350.0,1.9e-5
def lumped(d,etafn,V=15,Lmm=8,f=200,P0=100,K=1.5):
    r=d/2e3; A=math.pi*r*r; L=Lmm/1e3; Le=L+1.7*r; Vm=V*1e-6; w=2*math.pi*f
    M=rho*Le/A; C=Vm/(rho*c*c); X=w*M-1/(w*C)
    Rl=max(8*mu*L/(math.pi*r**4),(L/(math.pi*r**3))*math.sqrt(2*rho*mu*w))+rho*w*w/(2*math.pi*c)
    k=(8/(3*math.pi))*K*rho/(2*A*A)
    lo,hi=0,P0/math.sqrt(Rl*Rl+X*X)
    for _ in range(60):
        q=(lo+hi)/2
        if q*math.sqrt((Rl+k*q)**2+X*X)>P0: hi=q
        else: lo=q
    Vin=2*lo/w; L0d=Vin/A/(d/1e3); eta=etafn(L0d,Lmm/d)
    return eta*Vin*f*1e6, L0d, eta
dv=lambda x,l: 0.7*max(0,1-0.6*l/x)
asm=lambda x,l: 1-math.exp(-x/2)
for L in [8,2]:
    print('L',L)
    for d in [0.8,1.29,1.9,2.1,4.0]:
        a=lumped(d,asm,Lmm=L); b=lumped(d,dv,Lmm=L)
        print(d, 'assumed %.2f (L0/d %.1f eta %.2f)'%a, ' dv %.2f eta %.2f'%(b[0],b[2]))
