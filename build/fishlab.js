/* 비지도학습 물고기 연구실 — 공용 계산·그리기 모듈 (외부 라이브러리 없음) */
window.FL=(function(){
'use strict';
var SP=['Bream','Parkki','Perch','Pike','Roach','Smelt','Whitefish'];
var SPKO={Bream:'도미',Parkki:'파르키',Perch:'농어',Pike:'강꼬치고기',Roach:'로치',Smelt:'빙어',Whitefish:'흰송어'};
var SPC={Bream:'#a35c00',Parkki:'#9b3fb5',Perch:'#13733a',Pike:'#1e55c8',Roach:'#c42a6e',Smelt:'#0b7a86',Whitefish:'#6b5b3e'};
/* 주머니(군집) 색: 첫 색은 비지도 강조색(스킬 8-3) */
var CLC=['#1f7a52','#c9302c','#1e55c8','#a35c00','#9b3fb5','#0b7a86','#5b6874','#8f5a2e'];
var COLS=['무게','길이1','길이2','길이3','높이','폭'];
var UNITS=['g','cm','cm','cm','cm','cm'];
var D=null;
function load(){
  if(D)return D;var el=document.getElementById('fish-data');if(!el)return null;
  var raw=JSON.parse(el.textContent);var rows=raw.rows.split(';');
  var sp=[],X=[],seed=[],orig=[];
  rows.forEach(function(r){var f=r.split(',');sp.push(SP[+f[0]]);X.push([+f[1],+f[2],+f[3],+f[4],+f[5],+f[6]]);seed.push(+f[7]);orig.push(f[8]==='1');});
  D={sp:sp,X:X,seed:seed,orig:orig,n:sp.length,test:raw.test||null};return D;
}
function meanStd(X){var p=X[0].length,n=X.length,m=[],s=[];for(var j=0;j<p;j++){var a=0;for(var i=0;i<n;i++)a+=X[i][j];a/=n;var v=0;for(i=0;i<n;i++)v+=(X[i][j]-a)*(X[i][j]-a);m.push(a);s.push(Math.sqrt(v/n)||1);}return {m:m,s:s};}
function standardize(X,ms){ms=ms||meanStd(X);return X.map(function(r){return r.map(function(v,j){return (v-ms.m[j])/ms.s[j];});});}
function d2(a,b){var s=0;for(var j=0;j<a.length;j++){var t=a[j]-b[j];s+=t*t;}return s;}
function dist(a,b){return Math.sqrt(d2(a,b));}
function manhattan(a,b){var s=0;for(var j=0;j<a.length;j++)s+=Math.abs(a[j]-b[j]);return s;}
/* k-평균: init은 중심 좌표 배열. 한 걸음씩도, 끝까지도 */
function assign(Z,C){var lab=new Array(Z.length),inertia=0;for(var i=0;i<Z.length;i++){var b=0,bd=Infinity;for(var c=0;c<C.length;c++){var dd=d2(Z[i],C[c]);if(dd<bd){bd=dd;b=c;}}lab[i]=b;inertia+=bd;}return {lab:lab,inertia:inertia};}
function recenter(Z,lab,k,old){var p=Z[0].length,C=[],cnt=[];for(var c=0;c<k;c++){C.push(new Array(p).fill(0));cnt.push(0);}for(var i=0;i<Z.length;i++){cnt[lab[i]]++;for(var j=0;j<p;j++)C[lab[i]][j]+=Z[i][j];}for(c=0;c<k;c++){if(cnt[c])for(j=0;j<p;j++)C[c][j]/=cnt[c];else C[c]=old[c].slice();}return C;}
function kmeansFrom(Z,C,maxIt){var it=0,a=assign(Z,C),prev;for(;it<(maxIt||100);it++){C=recenter(Z,a.lab,C.length,C);prev=a.inertia;a=assign(Z,C);if(Math.abs(prev-a.inertia)<1e-9)break;}return {lab:a.lab,C:C,inertia:a.inertia,iters:it+1};}
/* k-means++ 시작점 (시드 고정) */
function ppInit(Z,k,seed){var r=rng(seed||7),C=[Z[Math.floor(r()*Z.length)].slice()];while(C.length<k){var dd=Z.map(function(z){var m=Infinity;C.forEach(function(c){var t=d2(z,c);if(t<m)m=t;});return m;});var tot=dd.reduce(function(a,b){return a+b;},0),u=r()*tot,acc=0,pick=0;for(var i=0;i<dd.length;i++){acc+=dd[i];if(acc>=u){pick=i;break;}}C.push(Z[pick].slice());}return C;}
function kmeans(Z,k,nInit,seed){var best=null;for(var t=0;t<(nInit||5);t++){var res=kmeansFrom(Z,ppInit(Z,k,(seed||7)+t*101));if(!best||res.inertia<best.inertia)best=res;}return best;}
function silhouette(Z,lab,k,idx){var n=Z.length,tot=0,cnt=0,list=idx||Z.map(function(_,i){return i;});var size=new Array(k).fill(0);lab.forEach(function(l){size[l]++;});
  list.forEach(function(i){var sums=new Array(k).fill(0);for(var j=0;j<n;j++){if(j===i)continue;sums[lab[j]]+=Math.sqrt(d2(Z[i],Z[j]));}
    var own=lab[i],a=size[own]>1?sums[own]/(size[own]-1):0,b=Infinity;for(var c=0;c<k;c++){if(c===own||!size[c])continue;var m=sums[c]/size[c];if(m<b)b=m;}
    var s=size[own]>1?(b-a)/Math.max(a,b):0;tot+=s;cnt++;});return tot/cnt;}
function silOne(Z,lab,k,i){var n=Z.length,sums=new Array(k).fill(0),size=new Array(k).fill(0);lab.forEach(function(l){size[l]++;});for(var j=0;j<n;j++){if(j===i)continue;sums[lab[j]]+=Math.sqrt(d2(Z[i],Z[j]));}var own=lab[i],a=sums[own]/Math.max(1,size[own]-1),b=Infinity,bc=-1;for(var c=0;c<k;c++){if(c===own||!size[c])continue;var m=sums[c]/size[c];if(m<b){b=m;bc=c;}}return {a:a,b:b,s:(b-a)/Math.max(a,b),near:bc};}
/* 조정 랜드 지수 (이름표와 주머니가 얼마나 닮았나, 채점용) */
function ari(a,b){var ka={},kb={},t={},n=a.length;for(var i=0;i<n;i++){ka[a[i]]=(ka[a[i]]||0)+1;kb[b[i]]=(kb[b[i]]||0)+1;var key=a[i]+'|'+b[i];t[key]=(t[key]||0)+1;}
  function c2(x){return x*(x-1)/2;}var sij=0,sa=0,sb=0;Object.keys(t).forEach(function(k){sij+=c2(t[k]);});Object.keys(ka).forEach(function(k){sa+=c2(ka[k]);});Object.keys(kb).forEach(function(k){sb+=c2(kb[k]);});
  var exp=sa*sb/c2(n),mx=(sa+sb)/2;return (sij-exp)/(mx-exp);}
/* 공분산 행렬의 고유값 분해 (야코비) */
function cov(Z){var n=Z.length,p=Z[0].length,C=[];for(var a=0;a<p;a++){C.push([]);for(var b=0;b<p;b++){var s=0;for(var i=0;i<n;i++)s+=Z[i][a]*Z[i][b];C[a].push(s/(n-1));}}return C;}
function eig(A){var n=A.length,a=A.map(function(r){return r.slice();}),V=[];for(var i=0;i<n;i++){V.push(new Array(n).fill(0));V[i][i]=1;}
  for(var sweep=0;sweep<100;sweep++){var off=0;for(var p=0;p<n;p++)for(var q=p+1;q<n;q++)off+=a[p][q]*a[p][q];if(off<1e-20)break;
    for(p=0;p<n;p++)for(q=p+1;q<n;q++){if(Math.abs(a[p][q])<1e-15)continue;var th=(a[q][q]-a[p][p])/(2*a[p][q]),t=(th>=0?1:-1)/(Math.abs(th)+Math.sqrt(th*th+1)),c=1/Math.sqrt(t*t+1),s=t*c;
      for(var k=0;k<n;k++){var akp=a[k][p],akq=a[k][q];a[k][p]=c*akp-s*akq;a[k][q]=s*akp+c*akq;}
      for(k=0;k<n;k++){var apk=a[p][k],aqk=a[q][k];a[p][k]=c*apk-s*aqk;a[q][k]=s*apk+c*aqk;}
      for(k=0;k<n;k++){var vkp=V[k][p],vkq=V[k][q];V[k][p]=c*vkp-s*vkq;V[k][q]=s*vkp+c*vkq;}}}
  var vals=[],vecs=[];for(i=0;i<n;i++){vals.push(a[i][i]);vecs.push(V.map(function(r){return r[i];}));}
  var ord=vals.map(function(_,i){return i;}).sort(function(x,y){return vals[y]-vals[x];});
  return {vals:ord.map(function(i){return vals[i];}),vecs:ord.map(function(i){return vecs[i];})};}
function pca(Z){var e=eig(cov(Z));var tot=e.vals.reduce(function(a,b){return a+b;},0);
  /* 부호: 첫 축은 무게가 +, 둘째 축은 높이가 + 쪽 */
  e.vecs.forEach(function(v,i){var ref=i===1?4:0;if(i>1)ref=v.reduce(function(m,x,j){return Math.abs(x)>Math.abs(v[m])?j:m;},0);if(v[ref]<0)for(var j=0;j<v.length;j++)v[j]=-v[j];});
  return {vals:e.vals,vecs:e.vecs,evr:e.vals.map(function(v){return v/tot;})};}
function project(z,vecs,k){var o=[];for(var c=0;c<k;c++){var s=0;for(var j=0;j<z.length;j++)s+=z[j]*vecs[c][j];o.push(s);}return o;}
function unproject(s,vecs){var p=vecs[0].length,z=new Array(p).fill(0);for(var c=0;c<s.length;c++)for(var j=0;j<p;j++)z[j]+=s[c]*vecs[c][j];return z;}
/* 오토인코더 앞으로 계산 (scikit-learn MLPRegressor 가중치, 숨은 층 tanh, 출력 그대로) */
function aeForward(z,W,b,code){var h=z,mid=null;for(var l=0;l<W.length;l++){var o=[];for(var j=0;j<W[l][0].length;j++){var s=b[l][j];for(var i=0;i<h.length;i++)s+=h[i]*W[l][i][j];o.push(l<W.length-1?Math.tanh(s):s);}h=o;if(l===1)mid=o.slice();}return code?mid:h;}
/* 산점도 */
function niceTicks(lo,hi,n){var span=hi-lo,step=Math.pow(10,Math.floor(Math.log10(span/(n||5)))),err=(n||5)/span*step;if(err<=.15)step*=10;else if(err<=.35)step*=5;else if(err<=.75)step*=2;var t=[],v=Math.ceil(lo/step)*step;for(;v<=hi+1e-9;v+=step)t.push(+v.toFixed(10));return t;}
function axes(g,W,H,o){var L=o.padL||54,R=o.padR||14,T=o.padT||14,B=o.padB||40;var x0=o.xmin,x1=o.xmax,y0=o.ymin,y1=o.ymax;
  var sx=function(v){return L+(v-x0)/(x1-x0)*(W-L-R);},sy=function(v){return H-B-(v-y0)/(y1-y0)*(H-T-B);};
  g.save();g.fillStyle='#fff';g.fillRect(0,0,W,H);g.strokeStyle='rgba(22,33,43,.07)';g.lineWidth=1;g.font='12px "IBM Plex Sans KR",system-ui,sans-serif';g.fillStyle='#5b6874';
  niceTicks(x0,x1,o.xt||6).forEach(function(t){var x=sx(t);g.beginPath();g.moveTo(x,T);g.lineTo(x,H-B);g.stroke();g.textAlign='center';g.fillText(o.xfmt?o.xfmt(t):t,x,H-B+16);});
  niceTicks(y0,y1,o.yt||5).forEach(function(t){var y=sy(t);g.beginPath();g.moveTo(L,y);g.lineTo(W-R,y);g.stroke();g.textAlign='right';g.fillText(o.yfmt?o.yfmt(t):t,L-6,y+4);});
  g.strokeStyle='#8a96a3';g.beginPath();g.moveTo(L,T);g.lineTo(L,H-B);g.lineTo(W-R,H-B);g.stroke();
  g.fillStyle='#16212b';g.textAlign='center';if(o.xlab)g.fillText(o.xlab,(L+W-R)/2,H-6);if(o.ylab){g.save();g.translate(13,(T+H-B)/2);g.rotate(-Math.PI/2);g.fillText(o.ylab,0,0);g.restore();}
  g.restore();return {sx:sx,sy:sy,L:L,R:R,T:T,B:B};}
function dot(g,x,y,r,c,alpha){g.globalAlpha=alpha==null?.8:alpha;g.fillStyle=c;g.beginPath();g.arc(x,y,r,0,6.2832);g.fill();g.globalAlpha=1;}
function range(arr,pad){var lo=Infinity,hi=-Infinity;arr.forEach(function(v){if(v<lo)lo=v;if(v>hi)hi=v;});var p=(hi-lo)*(pad==null?.05:pad);return [lo-p,hi+p];}
function legend(el,items){el.innerHTML=items.map(function(it){return '<span><i style="background:'+it[1]+'"></i>'+it[0]+'</span>';}).join('');}
function spLegend(el){legend(el,SP.map(function(s){return [SPKO[s]+' '+s,SPC[s]];}));}
function fmt(v,d){return (+v).toLocaleString('ko-KR',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
function pct(v,d){return (v*100).toFixed(d==null?1:d)+'%';}
function kpis(el,arr){el.innerHTML=arr.map(function(a){return '<div class="kpi '+(a[2]||'')+'"><b>'+a[0]+'</b><span>'+a[1]+'</span></div>';}).join('');}
return {SP:SP,SPKO:SPKO,SPC:SPC,CLC:CLC,COLS:COLS,UNITS:UNITS,load:load,meanStd:meanStd,standardize:standardize,d2:d2,dist:dist,manhattan:manhattan,
  assign:assign,recenter:recenter,kmeansFrom:kmeansFrom,ppInit:ppInit,kmeans:kmeans,silhouette:silhouette,silOne:silOne,ari:ari,cov:cov,eig:eig,pca:pca,project:project,unproject:unproject,
  aeForward:aeForward,axes:axes,dot:dot,range:range,legend:legend,spLegend:spLegend,fmt:fmt,pct:pct,kpis:kpis,niceTicks:niceTicks};
})();
