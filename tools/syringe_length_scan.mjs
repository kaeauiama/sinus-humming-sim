// HISTORICAL: length scan with the old soft law (results/syringe_lumped_fit.md). Superseded by tools/syringe_fig6_fit.mjs.
const RHO=1.14,C0=350,MU=1.9e-5,KLOSS=1.5;
const mix=x=>0.59*(1-Math.exp(-Math.pow(x/1.89,1.76)));
function lumped(V,d,Lmm,f,P0){const r=d/2e3,A=Math.PI*r*r,L=Lmm/1e3,Le=L+1.7*r,Vm=V*1e-6,w=2*Math.PI*f;
const M=RHO*Le/A,Cc=Vm/(RHO*C0*C0),X=w*M-1/(w*Cc);
const Rl=Math.max(8*MU*L/(Math.PI*r**4),(L/(Math.PI*r**3))*Math.sqrt(2*RHO*MU*w))+RHO*w*w/(2*Math.PI*C0);
const k=(8/(3*Math.PI))*KLOSS*RHO/(2*A*A);let lo=0,hi=P0/Math.sqrt(Rl*Rl+X*X);
for(let i=0;i<60;i++){const q=(lo+hi)/2;if(q*Math.sqrt((Rl+k*q)**2+X*X)>P0)hi=q;else lo=q;}
const Vin=2*lo/w;return{f0:C0/(2*Math.PI)*Math.sqrt(A/(Vm*Le)),x:Vin/A/L,kH:mix(Vin/A/L)*Vin*f/Vm};}
const DS=[0.8,1.3,1.9,2.1,4.0];
for (const L of [2.1,5,10,15]) for (const P0 of [100,300,1000]) for (const f of [150]) {
  const t=10; const ex=DS.map(d=>{const r=lumped(15,d,L,f,P0);return 1-Math.exp(-r.kH*t)});
  const f0=DS.map(d=>lumped(15,d,L,f,P0).f0.toFixed(0)).join('/');
  console.log(`L=${L} P0=${P0} f=${f} f0=${f0} exch10s=`+ex.map(v=>(v*100).toFixed(1)).join(' ')+' ratio='+ex.map(v=>(v/ex[0]).toFixed(1)).join(':'));
}
