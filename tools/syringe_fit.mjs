// HISTORICAL: fit to the printed output ratios with the old soft law, as recorded in results/syringe_lumped_fit.md.
// Superseded by tools/syringe_fig6_fit.mjs (Fig. 6 target, shared model in tools/model.mjs). Kept unchanged on purpose.
const RHO=1.14,C0=350,MU=1.9e-5,KLOSS=1.5;
const mix=x=>0.59*(1-Math.exp(-Math.pow(x/1.89,1.76)));
function lumped(V,d,Lmm,f,P0){const r=d/2e3,A=Math.PI*r*r,L=Lmm/1e3,Le=L+1.7*r,Vm=V*1e-6,w=2*Math.PI*f;
const M=RHO*Le/A,Cc=Vm/(RHO*C0*C0),X=w*M-1/(w*Cc);
const Rl=Math.max(8*MU*L/(Math.PI*r**4),(L/(Math.PI*r**3))*Math.sqrt(2*RHO*MU*w))+RHO*w*w/(2*Math.PI*C0);
const k=(8/(3*Math.PI))*KLOSS*RHO/(2*A*A);let lo=0,hi=P0/Math.sqrt(Rl*Rl+X*X);
for(let i=0;i<60;i++){const q=(lo+hi)/2;if(q*Math.sqrt((Rl+k*q)**2+X*X)>P0)hi=q;else lo=q;}
const Vin=2*lo/w,u=lo/A;return{f0:C0/(2*Math.PI)*Math.sqrt(A/(Vm*Le)),x:Vin/A/L,kH:mix(Vin/A/L)*Vin*f/Vm,Re:u*d/1e3/1.5e-5,L0d:Vin/A/(d/1e3)};}
const DS=[0.8,1.3,1.9,2.1,4.0], HUM=[1,4.5,6,14,30], ART=[1,8,13,15,39];
const FA=[[120,230],[200,295],[450,143]], FH=[[130,204],[150,175],[450,143]];
const out=(d,L,f,P0,t)=>1-Math.exp(-lumped(15,d,L,f,P0).kH*t);
let res=[];
for (let L=1;L<=30;L+=0.5) for (let lp=1;lp<=3.3;lp+=0.05) for (const t of [5,10,30]) {
  const P0=10**lp;
  const sz=DS.map(d=>out(d,L,150,P0,t)); if(sz[0]<=0)continue;
  const eS=DS.reduce((a,_,i)=>a+(Math.log(sz[i]/sz[0])-Math.log(HUM[i]))**2,0);
  const fa=FA.map(([f])=>out(1.9,L,f,P0,t)); const eF=FA.reduce((a,[,v],i)=>a+(Math.log(fa[i]/fa[1])-Math.log(v/295))**2,0);
  res.push({L,P0:Math.round(P0),t,eS,eF,e:eS+eF*2,sz:sz.map(v=>(v/sz[0]).toFixed(1)).join(':'),fa:fa.map(v=>(v/fa[1]).toFixed(2)).join('/')});
}
res.sort((a,b)=>a.e-b.e); console.log('best combined'); res.slice(0,6).forEach(r=>console.log(JSON.stringify(r)));
res.sort((a,b)=>a.eS-b.eS); console.log('best size only'); res.slice(0,4).forEach(r=>console.log(JSON.stringify(r)));
res.sort((a,b)=>a.eF-b.eF); console.log('best freq only'); res.slice(0,4).forEach(r=>console.log(JSON.stringify(r)));
const b=res.sort((a,b)=>a.e-b.e)[0]; DS.forEach(d=>{const r=lumped(15,d,b.L,150,b.P0);console.log(d,'f0',r.f0.toFixed(0),'x',r.x.toFixed(2),'Re',r.Re.toFixed(0),'L0/d',r.L0d.toFixed(2))});
console.log('--- 4.0 mm short opening, others long');
for (const [Ls,L4,P0,t] of [[7,2,220,5],[7,1,220,5],[10,2,300,5],[7,2,220,10],[15,2,400,5]]) {
  const sz=DS.map(d=>out(d,d===4?L4:Ls,150,P0,t));
  console.log(Ls,L4,P0,t, sz.map(v=>(v/sz[0]).toFixed(1)).join(':'), 'abs', sz.map(v=>(v*100).toFixed(0)).join('/'));
}
