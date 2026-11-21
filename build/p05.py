# -*- coding: utf-8 -*-
"""마지막 장 · 실전 연습장 — 어시장 운영 시뮬레이터 (진열대 정리 · 지도 만들기 · 검수대)"""
from lib import *

P = 'practice/index.html'


def scene(sid, title, situation, env_html, me_html, links, extra=''):
    return ('<section class="level scene-sec" id="%s" data-scene="%s"><div class="wrap"><h2>%s</h2>'
            '<div class="note">%s</div>'
            '<div class="grid2"><div class="ctl-env"><h4 style="color:var(--gfp)">시장 조건 (초록)</h4>%s</div><div class="ctl-me"><h4 style="color:var(--info)">내 결정 (파랑)</h4>%s</div></div>'
            '<section class="kpis" id="kp_%s" aria-label="성적표"></section>'
            '<div class="grid2"><div>%s</div><div>%s</div></div>%s'
            '<div class="chat" id="ch_%s" aria-live="polite"></div>'
            '<h3>미션</h3><div id="ms_%s"></div>'
            '<p class="small">배운 곳 다시 보기: %s</p></div></section>') % (
        sid, sid, title, situation, env_html, me_html, sid,
        canvas('g1_' + sid, 300, title + ' 첫째 그래프'), canvas('g2_' + sid, 300, title + ' 둘째 그래프'), extra, sid, sid, links)


def body():
    b = three([
        ('무엇을', '어시장 하루를 직접 운영합니다. 진열대 나누기(군집), 물고기 지도 만들기(PCA), 검수대 지키기(가린 무게·범위 밖)를 조작판으로 해 봅니다.'),
        ('왜 중요한가', '배운 도구는 조건이 바뀌어도 결론이 유지되는지 확인해야 현장에서 씁니다. 함정도 직접 밟아 봐야 기억에 남습니다.'),
        ('어떻게', '초록 조작판은 시장 조건, 파랑 조작판은 내 결정입니다. 성적표와 그래프를 보며 미션 세 개를 통과하세요. 기록은 이 탭에만 남고 저장되지 않습니다.')],
        '숫자는 교육용 예시입니다. 실제 수산물 유통·경영 권고가 아닙니다.', title='실전 연습장 — 3줄 안내')
    b += ('<section class="level" style="padding-top:40px"><div class="wrap"><div class="tabs" role="tablist">'
          '<button class="bt" data-tab="shelf" role="tab" aria-pressed="true">① 진열대 정리 (묶기)</button>'
          '<button class="bt" data-tab="map" role="tab" aria-pressed="false">② 물고기 지도 (접기)</button>'
          '<button class="bt" data-tab="check" role="tab" aria-pressed="false">③ 검수대 (맞히기·범위 밖)</button></div>'
          '<p class="small muted">주소 끝에 #shelf, #map, #check를 붙이면 그 장면이 바로 열립니다.</p></div></section>')
    b += scene('shelf', '① 진열대 정리 — 몇 개의 진열대에 어떻게 나눌까',
               '아침에 물고기 1,554마리가 이름표 없이 들어왔습니다. 손님이 고르기 쉽게 생김새가 비슷한 것끼리 진열대에 나눠 놓아야 합니다. 진열대 수와 "무엇으로 닮음을 잴지"를 정하세요.',
               '<div class="group"><span class="glabel">측정 오차</span><button class="bt" data-env="0" aria-pressed="true">없음</button><button class="bt" data-env="0.04" aria-pressed="false">보통 (±4%)</button><button class="bt" data-env="0.08" aria-pressed="false">높음 (±8%)</button></div>'
               '<p class="small muted">자로 잴 때 높이·폭에 섞이는 오차입니다.</p>',
               '<div class="group"><span class="glabel">자</span><button class="bt" data-feat="ratio" aria-pressed="true">체형 비율 2개</button><button class="bt" data-feat="six" aria-pressed="false">측정값 6개 (표준화)</button><button class="bt" data-feat="raw" aria-pressed="false">측정값 6개 (원 단위)</button></div>'
               '<div class="group"><span class="glabel">진열대 수 k</span><input type="range" id="k_shelf" min="2" max="7" value="5" aria-label="진열대 수"><span class="val" id="kv_shelf">5</span></div>',
               '<a href="../02_grouping.html#s1">2-1 k-평균</a> · <a href="../02_grouping.html#s2">2-2 엘보</a> · <a href="../02_grouping.html#s3">2-3 실루엣</a> · <a href="../01_no_answer_key.html#s3">1-3 표준화</a>')
    b += scene('map', '② 물고기 지도 — 몇 축으로, 어떻게 접을까',
               '경매사가 오늘 들어온 물고기를 한눈에 볼 지도를 원합니다. 지도는 화면 한 장이어야 하지만, 너무 많이 버리면 비슷한 물고기를 잘못 붙입니다.',
               '<div class="group"><span class="glabel">측정값 세트</span><button class="bt" data-env="six" aria-pressed="true">6개 전부</button><button class="bt" data-env="four" aria-pressed="false">4개 (무게·길이1·높이·폭)</button></div>'
               '<p class="small muted">길이 세 값 중 하나만 재는 어시장도 있습니다.</p>',
               '<div class="group"><span class="glabel">표준화</span><button class="bt" data-std="1" aria-pressed="false">하기</button><button class="bt" data-std="0" aria-pressed="true">안 하기</button></div>'
               '<div class="group"><span class="glabel">남길 축 수</span><input type="range" id="k_map" min="1" max="4" value="1" aria-label="남길 축 수"><span class="val" id="kv_map">1</span></div>',
               '<a href="../03_folding.html#s3">3-3 PCA 네 걸음</a> · <a href="../03_folding.html#s4">3-4 물고기 지도</a> · <a href="../03_folding.html#s5">3-5 복원</a>')
    b += scene('check', '③ 검수대 — 무엇을 다시 잴까',
               '물고기가 한 줄로 들어옵니다. 검수원은 경보가 뜬 물고기만 다시 잽니다(한 마리 5분). 섞여 들어온 이상한 물고기(측정 기준이 다른 물고기, 무게를 잘못 적은 물고기, 처음 보는 큰 물고기)를 놓치지 말되, 괜한 경보로 검수원을 지치게 하지도 마세요.',
               '<div class="group"><span class="glabel">오늘의 줄</span><button class="bt" data-env="normal" aria-pressed="true">평소 (이상 3마리)</button><button class="bt" data-env="mixed" aria-pressed="false">다른 바다 물고기가 많은 날 (이상 7마리)</button></div>',
               '<div class="group"><span class="glabel">범위 밖 문턱 (지도 거리·복원 오차 공통 배율)</span><input type="range" id="t_check" min="0.5" max="6" step="0.1" value="6" aria-label="범위 밖 문턱 배율"><span class="val" id="tv_check"></span></div>'
               '<div class="group"><span class="glabel">무게 의심 기준</span><input type="range" id="w_check" min="5" max="80" step="1" value="80" aria-label="무게 의심 기준"><span class="val" id="wv_check"></span></div>',
               '<a href="../04_guessing.html#s1">4-1 가린 무게</a> · <a href="../04_guessing.html#s4">4-4 배운 범위 밖</a> · <a href="../03_folding.html#s4">3-4 물고기 지도</a>')
    b += section('close', '마무리 — 세 장면이 함께 묻는 것',
                 '<p>세 장면 모두 같은 질문을 던집니다. <b>"AI가 낸 숫자를 그대로 쓰기 전에, 무엇으로 쟀고, 무엇을 버렸고, 배운 범위 안인지 확인했나?"</b> '
                 '진열대는 자(변수)를 잘못 고르면 크기로만 나뉘고, 지도는 표준화를 빼먹으면 무게 한 축이 되고, 검수대는 문턱을 너무 낮추면 경보가 쏟아지고 너무 높이면 이상한 물고기를 놓칩니다.</p>'
                 + note('이 연습장의 모형은 교육용으로 단순화했습니다. 측정 오차는 높이·폭에만 넣었고, 이상 물고기는 직접 만든 가상 물고기입니다. 숫자는 교육용 예시이며 실제 수산물 유통·경영·투자 권고가 아닙니다.', warn=True)
                 + say('doc', 'magic', '세 장면을 다 통과했다면, 비지도학습을 현장에 쓸 준비가 된 겁니다. 도구보다 확인 습관이 먼저입니다.'))
    return b


JS = r'''
var D=FL.load(),X=D.X,N=D.n,SP=FL.SP,SPC=FL.SPC,SPKO=FL.SPKO,CLC=FL.CLC;
var TE=D.test,isTe={};TE.forEach(function(i){isTe[i]=1;});var TR=[];for(var i=0;i<N;i++)if(!isTe[i])TR.push(i);
var MW=__MW__,THR0=__THR__,THR4=__THR4__;
function sayHTML(lines){return lines.map(function(l){return '<div class="say" data-who="'+l[0]+'"><img data-who="'+l[0]+'" data-mood="'+l[1]+'" src="'+Cast.src(l[0],l[1])+'" alt="" aria-hidden="true"><div><b class="name">'+{doc:'박사',asst:'조수 하루',fly:'초파리 연구원',robo:'주판봇'}[l[0]]+'</b><p>'+l[2]+'</p></div></div>';}).join('');}
function Missions(id,list){var st=list.map(function(){return false;});var touched=false;
  return {touch:function(){touched=true;},update:function(state){if(touched)list.forEach(function(m,i){if(!st[i]&&m.test(state))st[i]=true;});
    $('#ms_'+id).innerHTML=list.map(function(m,i){return '<div class="mission'+(st[i]?' ok':'')+'"><span class="st">'+(st[i]?'통과':'미션 '+(i+1))+'</span><p>'+m.text+'</p></div>';}).join('');},state:st};}
function press(sel,el){$$(sel).forEach(function(x){x.setAttribute('aria-pressed',x===el?'true':'false');});}
function gauss(r){return (r()+r()+r()+r()-2)/0.5774;}
/* ── ① 진열대 ── */
var SH=(function(){var env=0,feat='ratio',k=5,cache={};var M=Missions('shelf',[
   {text:'진열대 나누기의 평균 실루엣을 0.65 이상으로 만드세요. (자와 진열대 수를 바꿔 보세요)',test:function(s){return s.sil>=0.65;}},
   {text:'함정 관찰: 자를 "측정값 6개 (원 단위)"로 두고 진열대 3개로 나눠, 이름표 대조 점수가 0.2보다 낮아지는 것을 확인하세요.',test:function(s){return s.feat==='raw'&&s.k===3&&s.ari<0.2;}},
   {text:'조건 바꾸기: 측정 오차를 "높음"으로 올려도 체형 비율의 실루엣 곡선이 진열대 3개에서 가장 높은지 확인하고, 진열대 3개를 고르세요.',test:function(s){return s.env===0.08&&s.feat==='ratio'&&s.k===3&&s.bestK===3;}}]);
  function feats(){var key=env+'|'+feat;if(cache[key])return cache[key];var r=rng(907),F;
    if(feat==='ratio'){F=X.map(function(x){var h=x[4]*(1+env*gauss(r)),w=x[5]*(1+env*gauss(r));return [h/x[1],w/x[1]];});}
    else{F=X.map(function(x){var y=x.slice();y[4]=x[4]*(1+env*gauss(r));y[5]=x[5]*(1+env*gauss(r));return y;});}
    var Zf=feat==='raw'?F:FL.standardize(F);var sub=[];for(var i=0;i<N;i+=4)sub.push(i);var Zs=sub.map(function(i){return Zf[i];});
    var curve=[];for(var kk=2;kk<=7;kk++){var rr=FL.kmeans(Zs,kk,3,7);curve.push(FL.silhouette(Zs,rr.lab,kk));}
    var best=2+curve.indexOf(Math.max.apply(null,curve));var RAT=feat==='ratio'?F:F.map(function(x){return [x[4]/x[1],x[5]/x[1]];});
    return cache[key]={Zf:Zf,curve:curve,best:best,RAT:RAT,res:{}};}
  function run(){var f=feats();if(!f.res[k]){var r=FL.kmeans(f.Zf,k,4,7);var sub=[];for(var i=0;i<N;i+=3)sub.push(i);var sil=0;
      /* 부분 표본 실루엣: 표본 점마다 전체와의 거리 */
      var size=new Array(k).fill(0);r.lab.forEach(function(l){size[l]++;});sub.forEach(function(i){var sums=new Array(k).fill(0);for(var j=0;j<N;j++){if(j!==i)sums[r.lab[j]]+=Math.sqrt(FL.d2(f.Zf[i],f.Zf[j]));}var a=sums[r.lab[i]]/Math.max(1,size[r.lab[i]]-1),b=Infinity;for(var c=0;c<k;c++){if(c!==r.lab[i]&&size[c]){var m=sums[c]/size[c];if(m<b)b=m;}}sil+=(b-a)/Math.max(a,b);});
      f.res[k]={lab:r.lab,sil:sil/sub.length,ari:FL.ari(D.sp,r.lab),minShare:Math.min.apply(null,size)/N};}
    return f.res[k];}
  function draw(){var f=feats(),r=run();var c1=fit($('#g1_shelf')),g=c1.c,A=FL.axes(g,c1.W,c1.H,{xmin:.12,xmax:.62,ymin:.07,ymax:.25,xlab:'높이 ÷ 길이1',ylab:'폭 ÷ 길이1',padL:52});
    for(var i=0;i<N;i++)FL.dot(g,A.sx(f.RAT[i][0]),A.sy(f.RAT[i][1]),2.4,CLC[r.lab[i]],.65);stamp(g,c1.W,'색 = 내가 만든 진열대');
    var c2=fit($('#g2_shelf')),h=c2.c,B=FL.axes(h,c2.W,c2.H,{xmin:1.5,xmax:7.5,ymin:0,ymax:1,xlab:'진열대 수 k',ylab:'평균 실루엣 (표본)',xt:6});
    h.strokeStyle='#1e55c8';h.lineWidth=2.5;h.beginPath();f.curve.forEach(function(v,i){var x=B.sx(i+2),y=B.sy(v);i?h.lineTo(x,y):h.moveTo(x,y);});h.stroke();
    f.curve.forEach(function(v,i){FL.dot(h,B.sx(i+2),B.sy(v),i+2===k?7:4,i+2===f.best?'#1f7a52':'#1e55c8',1);});h.fillStyle='#1f7a52';h.font='700 12px "IBM Plex Sans KR",sans-serif';h.fillText('곡선의 꼭대기: k='+f.best,B.sx(f.best)+8,B.sy(f.curve[f.best-2])-8);stamp(h,c2.W,'큰 점 = 내가 고른 k');
    var s={env:env,feat:feat,k:k,sil:r.sil,ari:r.ari,bestK:f.best};
    FL.kpis($('#kp_shelf'),[[r.sil.toFixed(3),'평균 실루엣 (0.6 이상 좋음)',r.sil>=.6?'g':'r'],[FL.pct(r.minShare),'가장 작은 진열대의 몫 (5% 이상 좋음)',r.minShare>=.05?'g':'r'],[r.ari.toFixed(3),'이름표 대조 점수 (채점용, 0.5 이상 좋음)',r.ari>=.5?'g':'r'],[k+'개','진열대 수','i']]);
    var lines=[];if(r.sil>=.6)lines.push(['doc','judge','진열대 안은 촘촘하고 진열대끼리는 떨어져 있다. 이 나누기는 쓸 만하다.']);else lines.push(['doc','think','실루엣 '+r.sil.toFixed(2)+'. 진열대 경계에 선 물고기가 많다. 자나 진열대 수를 다시 보자.']);
    lines.push(['asst','report','실루엣 '+r.sil.toFixed(3)+', 이름표 대조 '+r.ari.toFixed(3)+', 가장 작은 진열대는 전체의 '+FL.pct(r.minShare)+'예요. 곡선의 꼭대기는 k='+f.best+'이에요.']);
    lines.push(feat==='raw'?['fly','magnify','원 단위로 쟀지? 그럼 진열대가 생김새가 아니라 무게로 갈렸을 거야.']:['fly','point',k===f.best?'곡선 꼭대기를 골랐네. 오차를 올려도 그대로인지 봐.':'곡선 꼭대기는 k='+f.best+'인데? 왜 다른 수를 골랐는지 말할 수 있어?']);
    lines.push(k>=6?['robo','happy','진열대가 많을수록 손님이 좋아하지! 더 늘리자!']:['robo','coin','진열대 '+k+'개? 7개로 늘리면 일곱 종이랑 딱 맞을 텐데!']);
    $('#ch_shelf').innerHTML=sayHTML(lines);M.update(s);}
  function bind(){$$('#shelf [data-env]').forEach(function(b){b.addEventListener('click',function(){env=+b.dataset.env;press('#shelf [data-env]',b);M.touch();draw();});});
    $$('#shelf [data-feat]').forEach(function(b){b.addEventListener('click',function(){feat=b.dataset.feat;press('#shelf [data-feat]',b);M.touch();draw();});});
    $('#k_shelf').addEventListener('input',function(){k=+this.value;$('#kv_shelf').textContent=k;M.touch();draw();});}
  return {draw:draw,bind:bind,set:function(o){if(o.env!==undefined)env=o.env;if(o.feat)feat=o.feat;if(o.k)k=o.k;M.touch();draw();},M:M};})();
/* ── ② 지도 ── */
var MP=(function(){var set='six',std=false,k=1,cache={};var M=Missions('map',[
   {text:'표준화를 켜고 측정값 6개로, 남긴 흔들림이 95%를 넘는 가장 적은 축 수를 고르세요.',test:function(s){return s.std&&s.set==='six'&&s.cum>=.95&&s.cumPrev<.95;}},
   {text:'함정 관찰: 표준화를 끄면 첫 축(PC1)에서 무게가 차지하는 몫이 99%를 넘는 것을 확인하세요.',test:function(s){return !s.std&&s.wShare>=.99;}},
   {text:'조건 바꾸기: 측정값을 4개로 줄여도(표준화 켬) 두 축이 흔들림의 90% 이상을 남기는지 확인하세요.',test:function(s){return s.std&&s.set==='four'&&s.k===2&&s.cum>=.9;}}]);
  var NM6=['무게','길이1','길이2','길이3','높이','폭'],NM4=['무게','길이1','높이','폭'];
  function prep(){var key=set+'|'+std;if(cache[key])return cache[key];var F=set==='six'?X:X.map(function(x){return [x[0],x[1],x[4],x[5]];});
    var M2=std?FL.standardize(F):(function(){var ms=FL.meanStd(F);return F.map(function(r){return r.map(function(v,j){return v-ms.m[j];});});})();
    var P=FL.pca(M2);var S=M2.map(function(z){return FL.project(z,P.vecs,4);});return cache[key]={P:P,S:S,names:set==='six'?NM6:NM4,agree:{}};}
  function agree(c,kk){if(c.agree[kk]!==undefined)return c.agree[kk];var ok=0,cnt=0;for(var i=0;i<N;i+=2){var o=-1,od=Infinity;for(var j=0;j<N;j++){if(j===i||D.seed[j]===D.seed[i])continue;var d=0;for(var q=0;q<kk;q++){var t=c.S[i][q]-c.S[j][q];d+=t*t;}if(d<od){od=d;o=j;}}if(D.sp[o]===D.sp[i])ok++;cnt++;}return c.agree[kk]=ok/cnt;}
  function draw(){var c=prep(),cum=c.P.evr.slice(0,k).reduce(function(a,b){return a+b;},0),cumPrev=c.P.evr.slice(0,k-1).reduce(function(a,b){return a+b;},0),wShare=c.P.vecs[0][0]*c.P.vecs[0][0],ag=agree(c,k);
    var c1=fit($('#g1_map')),g=c1.c;var xs=c.S.map(function(s){return s[0];}),ys=c.S.map(function(s,i){return k>=2?s[1]:((i*37)%21-10)/10;});var rx=FL.range(xs),ry=FL.range(ys);
    var A=FL.axes(g,c1.W,c1.H,{xmin:rx[0],xmax:rx[1],ymin:ry[0],ymax:ry[1],xlab:'PC1',ylab:k>=2?'PC2':'(한 축뿐 · 세로는 흩뿌림)',xfmt:function(t){return std?t:Math.round(t);},yfmt:function(t){return std||k<2?t:Math.round(t);}});
    for(var i=0;i<N;i++)FL.dot(g,A.sx(xs[i]),A.sy(ys[i]),2.3,SPC[D.sp[i]],.55);stamp(g,c1.W,'색 = 덮어 둔 종 (대조용)');
    var c2=fit($('#g2_map')),h=c2.c,n=c.P.evr.length,B=FL.axes(h,c2.W,c2.H,{xmin:.5,xmax:n+.5,ymin:0,ymax:1,xlab:'축 번호',ylab:'흔들림의 몫',xt:n,yfmt:function(t){return Math.round(t*100)+'%';}});
    var acc=0;c.P.evr.forEach(function(v,q){var x=B.sx(q+1);h.fillStyle=q<k?'rgba(31,122,82,.7)':'rgba(138,150,163,.35)';h.fillRect(x-14,B.sy(v),28,B.sy(0)-B.sy(v));acc+=v;FL.dot(h,x,B.sy(acc),4,'#1e55c8',1);});
    h.setLineDash([5,4]);h.strokeStyle='#c9302c';h.beginPath();h.moveTo(B.sx(.5),B.sy(.95));h.lineTo(B.sx(n+.5),B.sy(.95));h.stroke();h.setLineDash([]);h.fillStyle='#c9302c';h.font='12px "IBM Plex Sans KR",sans-serif';h.fillText('95%',B.sx(.6),B.sy(.95)-5);stamp(h,c2.W,'막대 = 각 축 · 파란 점 = 누적');
    var s={set:set,std:std,k:k,cum:cum,cumPrev:cumPrev,wShare:wShare};
    FL.kpis($('#kp_map'),[[FL.pct(cum),'남긴 흔들림 (95% 이상 좋음)',cum>=.95?'g':'a'],[FL.pct(wShare),'PC1에서 무게의 몫 (한 변수가 독점하면 나쁨)',wShare>.9?'r':'g'],[FL.pct(ag),'이웃이 같은 종인 비율 (채점용)',ag>=.75?'g':'r'],[k+'축','지도 축 수','i']]);
    var lines=[];lines.push(!std?['doc','verdict','표준화를 안 했다. 이 지도의 첫 축은 사실상 무게 하나다.']:cum>=.95?['doc','judge','두 가지를 다 챙겼다. 화면 한 장에 흔들림 '+FL.pct(cum)+'.']:['doc','think','흔들림을 '+FL.pct(cum)+'만 남겼다. 무엇을 버렸는지 보자.']);
    lines.push(['asst','report','남긴 흔들림 '+FL.pct(cum)+', PC1의 무게 몫 '+FL.pct(wShare)+', 이웃 일치율 '+FL.pct(ag)+'이에요.']);
    lines.push(!std?['fly','magnify','남긴 흔들림이 높다고 좋은 지도가 아니야. 무게 눈금이 커서 무게만 흔들린 거잖아.']:['fly','point','축을 하나 줄이면 이웃 일치율이 얼마나 떨어지는지도 같이 봐.']);
    lines.push(k>=3?['robo','happy','축은 많을수록 좋지! 네 개 다 넣자!']:['robo','coin','한 축에 '+FL.pct(c.P.evr[0])+'면 그걸로 끝 아냐?']);
    $('#ch_map').innerHTML=sayHTML(lines);M.update(s);}
  function bind(){$$('#map [data-env]').forEach(function(b){b.addEventListener('click',function(){set=b.dataset.env;press('#map [data-env]',b);M.touch();draw();});});
    $$('#map [data-std]').forEach(function(b){b.addEventListener('click',function(){std=b.dataset.std==='1';press('#map [data-std]',b);M.touch();draw();});});
    $('#k_map').addEventListener('input',function(){k=+this.value;$('#kv_map').textContent=k;M.touch();draw();});}
  return {draw:draw,bind:bind,set:function(o){if(o.set)set=o.set;if(o.std!==undefined)std=o.std;if(o.k)k=o.k;M.touch();draw();},M:M};})();
/* ── ③ 검수대 ── */
var CK=(function(){var day='normal',mult=6,tol=80;
  var MS=FL.meanStd(X),Z=FL.standardize(X,MS);var Ztr=TR.map(function(i){return Z[i];}),mtr=[0,0,0,0,0,0];Ztr.forEach(function(z){for(var j=0;j<6;j++)mtr[j]+=z[j]/Ztr.length;});
  var PCt=FL.pca(Ztr.map(function(z){return z.map(function(v,j){return v-mtr[j];});}));function toMap(x){var z=x.map(function(v,j){return (v-MS.m[j])/MS.s[j]-mtr[j];});return FL.project(z,PCt.vecs,2);}
  var MAPtr=TR.map(function(i){return toMap(X[i]);});function nnd(m){var b=Infinity;MAPtr.forEach(function(p){var d=(p[0]-m[0])*(p[0]-m[0])+(p[1]-m[1])*(p[1]-m[1]);if(d<b)b=d;});return Math.sqrt(b);}
  function rec4(x){var c=x.map(function(v,j){return (v-MS.m[j])/MS.s[j]-mtr[j];}),s=FL.project(c,PCt.vecs,4),b=FL.unproject(s,PCt.vecs),e=0;for(var j=0;j<6;j++)e+=(c[j]-b[j])*(c[j]-b[j]);return e/6;}
  function predW(x){return Math.exp(MW.intercept+MW.coef[0]*Math.log(x[1])+MW.coef[1]*Math.log(x[4])+MW.coef[2]*Math.log(x[5]));}
  var r=rng(2026),pick=TE.slice();for(var q=pick.length-1;q>0;q--){var j=Math.floor(r()*(q+1)),t=pick[q];pick[q]=pick[j];pick[j]=t;}
  function lineup(d){var L=pick.slice(0,40).map(function(i){return {x:X[i].slice(),odd:null,sp:D.sp[i]};});
    var perch=pick.filter(function(i){return D.sp[i]==='Perch'&&X[i][1]>20;});var roach=pick.filter(function(i){return D.sp[i]==='Roach';});
    var sea=function(i){var x=X[i].slice();x[1]=x[3];return {x:x,odd:'다른 바다 (길이1 항목에 길이3 값)',sp:D.sp[i]};};
    var odd=[{x:[9000,100,108,115,30,14],odd:'처음 보는 큰 물고기',sp:'?'},sea(perch[0]),(function(){var x=X[roach[0]].slice();x[0]=Math.round(x[0]*1.8);return {x:x,odd:'무게를 잘못 적음 (실제의 1.8배)',sp:D.sp[roach[0]]};})()];
    if(d==='mixed')odd=odd.concat([sea(perch[1]),sea(perch[2]),sea(roach[1]),sea(pick.filter(function(i){return D.sp[i]==='Bream';})[0])]);
    odd.forEach(function(o,k2){L.splice(5+k2*6,0,o);});return L.map(function(o){var m=toMap(o.x);o.m=m;o.d=nnd(m);o.rc=rec4(o.x);o.pw=predW(o.x);o.dev=Math.abs(o.x[0]-o.pw)/o.pw;return o;});}
  var LU={normal:lineup('normal'),mixed:lineup('mixed')};
  var M=Missions('check',[
   {text:'평소 줄에서 이상한 물고기 3마리를 모두 잡으면서, 괜한 경보를 3마리 이하로 줄이세요.',test:function(s){return s.day==='normal'&&s.miss===0&&s.fa<=3;}},
   {text:'함정 관찰: 범위 밖 문턱을 ×1.0 아래로 내려, 괜한 경보가 6마리 이상으로 쏟아지는 것을 확인하세요.',test:function(s){return s.mult<1&&s.fa>=6;}},
   {text:'조건 바꾸기: "다른 바다 물고기가 많은 날"에도 같은 원칙으로 이상한 물고기 7마리를 모두 잡고, 괜한 경보를 3마리 이하로 유지하세요.',test:function(s){return s.day==='mixed'&&s.miss===0&&s.fa<=3;}}]);
  function draw(){var L=LU[day],T=THR0*mult,flag=0,caught=0,odd=0,fa=0;L.forEach(function(o){o.fo=o.d>T||o.rc>THR4*mult;o.fw=o.dev>tol/100;o.flag=o.fo||o.fw;if(o.flag)flag++;if(o.odd){odd++;if(o.flag)caught++;}else if(o.flag)fa++;});
    $('#tv_check').textContent='×'+mult.toFixed(1)+' ('+T.toFixed(2)+')';$('#wv_check').textContent=tol+'%';
    var c1=fit($('#g1_check')),g=c1.c,A=FL.axes(g,c1.W,c1.H,{xmin:-5,xmax:9,ymin:-3.5,ymax:3.5,xlab:'지도 가로 (크기)',ylab:'지도 세로 (체형)'});
    MAPtr.forEach(function(p){FL.dot(g,A.sx(p[0]),A.sy(p[1]),1.8,'#1f7a52',.18);});
    L.forEach(function(o){var x=A.sx(Math.min(8.8,o.m[0])),y=A.sy(Math.max(-3.4,Math.min(3.4,o.m[1])));FL.dot(g,x,y,o.odd?6:4,o.odd?'#a35c00':'#1e55c8',.9);if(o.flag){g.strokeStyle='#c9302c';g.lineWidth=2;g.beginPath();g.arc(x,y,9,0,6.2832);g.stroke();}});
    stamp(g,c1.W,'파랑 = 줄의 물고기 · 주황 = 섞인 이상 물고기 · 빨간 고리 = 경보');
    var c2=fit($('#g2_check')),h=c2.c,B=FL.axes(h,c2.W,c2.H,{xmin:0,xmax:2600,ymin:0,ymax:2600,xlab:'길이·높이·폭으로 맞힌 무게 (g)',ylab:'적힌 무게 (g)'});
    h.fillStyle='rgba(31,122,82,.08)';h.beginPath();h.moveTo(B.sx(0),B.sy(0));h.lineTo(B.sx(2600),B.sy(2600*(1+tol/100)));h.lineTo(B.sx(2600),B.sy(2600*(1-tol/100)));h.closePath();h.fill();
    L.forEach(function(o){if(o.pw>2600||o.x[0]>2600)return;var x=B.sx(o.pw),y=B.sy(o.x[0]);FL.dot(h,x,y,o.odd?6:4,o.odd?'#a35c00':'#1e55c8',.9);if(o.fw){h.strokeStyle='#c9302c';h.lineWidth=2;h.beginPath();h.arc(x,y,9,0,6.2832);h.stroke();}});
    stamp(h,c2.W,'초록 띠 = 무게 의심 기준 안');
    var miss=odd-caught,s={day:day,mult:mult,tol:tol,miss:miss,fa:fa};
    FL.kpis($('#kp_check'),[[caught+' / '+odd,'잡은 이상 물고기',miss===0?'g':'r'],[fa+'마리','괜한 경보 (정상인데 경보)',fa<=3?'g':'r'],[flag*5+'분','다시 재는 데 드는 시간 (경보 × 5분)','a'],[L.length+'마리','오늘 줄의 물고기','i']]);
    var lines=[];lines.push(miss===0&&fa<=3?['doc','judge','이상한 물고기는 다 잡고, 검수원은 덜 지쳤다. 좋은 문턱이다.']:miss>0?['doc','verdict','이상한 물고기 '+miss+'마리가 검수대를 그냥 지나갔다. 문턱을 다시 보자.']:['doc','think','다 잡긴 했지만 괜한 경보가 '+fa+'마리다. 검수원이 하루 종일 다시 재게 된다.']);
    lines.push(['asst','report','경보 '+flag+'마리, 이상 물고기 '+caught+'/'+odd+', 괜한 경보 '+fa+'마리, 다시 재는 시간 '+flag*5+'분이에요.']);
    lines.push(miss>0?['fly','magnify','놓친 물고기를 봐. 범위 밖이었는데 문턱이 너무 높았나, 무게가 이상했는데 기준이 너무 느슨했나?']:['fly','point','문턱을 조금 바꿔도 결과가 그대로인지 확인해. 딱 한 점에서만 통과하면 운이야.']);
    lines.push(fa>=6?['robo','sigh','경보가 이렇게 많으면 인건비가… 이번 판은 손절이다.']:['robo','coin','문턱 없이 다 통과시키면 검수 시간 0분! 제일 싸잖아!']);
    $('#ch_check').innerHTML=sayHTML(lines);M.update(s);}
  function bind(){$$('#check [data-env]').forEach(function(b){b.addEventListener('click',function(){day=b.dataset.env;press('#check [data-env]',b);M.touch();draw();});});
    $('#t_check').addEventListener('input',function(){mult=+this.value;M.touch();draw();});$('#w_check').addEventListener('input',function(){tol=+this.value;M.touch();draw();});}
  return {draw:draw,bind:bind,set:function(o){if(o.day)day=o.day;if(o.mult)mult=o.mult;if(o.tol)tol=o.tol;M.touch();draw();},M:M,LU:LU};})();
/* 탭 */
var SC={shelf:SH,map:MP,check:CK},drawn={};
function show(t){if(!SC[t])t='shelf';$$('.scene-sec').forEach(function(s){s.hidden=s.dataset.scene!==t;});press('[data-tab]',$('[data-tab="'+t+'"]'));setTimeout(function(){SC[t].draw();drawn[t]=1;},20);}
$$('[data-tab]').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.tab);try{history.replaceState(null,'','#'+b.dataset.tab);}catch(e){}});});
SH.bind();MP.bind();CK.bind();show((location.hash||'#shelf').slice(1));
window.addEventListener('hashchange',function(){show((location.hash||'#shelf').slice(1));});
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){Object.keys(drawn).forEach(function(t){if(!$('#'+t).hidden)SC[t].draw();});},150);});
window.LAB_PRACTICE=SC;
'''.replace('__MW__', json.dumps(R['mask_weight'])).replace('__THR__', json.dumps(R['ood']['thr_q99'])).replace('__THR4__', json.dumps(R['pca4_ood']['thr_q99']))


GLOSS = {
    '실루엣': ['실루엣 점수', '진열대 안은 붙고 진열대끼리는 떨어진 정도. −1~+1. 2장 2-3.'],
    '표준화': ['표준화', '평균 0, 표준편차 1로 눈금을 맞추는 일. 1장 1-3.'],
    '문턱': ['문턱', '경보를 울리는 기준. 학습 물고기 이웃 거리 상위 1%에 배율을 곱한 값. 4장 4-4.'],
}


def main():
    USED.update(['doc_judge', 'doc_think', 'doc_verdict', 'doc_magic', 'asst_report', 'fly_magnify', 'fly_point', 'robo_happy', 'robo_coin', 'robo_sigh'])
    hero_html = hero('마지막 장 · 비지도학습 물고기 연구실', '실전 연습장 — 어시장 운영 시뮬레이터', '배운 도구를 조건이 바뀌어도 믿고 쓸 수 있을까?',
                     '어시장의 하루를 세 장면으로 운영합니다. <b>진열대 정리</b>에서 물고기를 묶고, <b>물고기 지도</b>에서 접고, <b>검수대</b>에서 가린 무게와 범위 밖 경보로 이상한 물고기를 걸러 냅니다. '
                     '장면마다 미션 세 개가 있습니다. 최적을 찾고, 함정을 직접 밟아 보고, 조건을 바꿔도 결론이 유지되는지 확인합니다.',
                     [('3', '장면 (묶기·접기·맞히기)', 'g'), ('9', '미션 (장면마다 3개)', 'i'), ('1,554', '물고기 (이름표는 대조에만)', 'm'), ('0', '저장하는 기록 (이 탭에만 남음)', 'a')],
                     [('doc', 'front', '오늘은 여러분이 어시장 운영자입니다. 판정은 성적표가, 확인은 여러분이 합니다.'),
                      ('asst', 'smile', '장면마다 미션이 셋이에요. 조작판을 움직여야 판정이 시작돼요.'),
                      ('fly', 'point', '최적 하나 찾고 끝내지 마. 조건을 바꿔도 그대로인지가 진짜 시험이야.'),
                      ('robo', 'coin', '진열대도 축도 경보도 많을수록 좋지! …라고 생각하면 함정 미션에서 만나자.')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a> 증강본'),
                 ('가린 무게 규칙·문턱', 'code/analysis.py → data/results.json (4장과 같은 값)'),
                 ('계산', '진열대·지도·검수대 모두 이 페이지가 브라우저에서 직접 계산 (실루엣 곡선은 4마리 중 1마리 표본)')],
                ['측정 오차(±4%, ±8%)는 높이·폭에만 넣은 설명용 잡음', '이상 물고기 3~7마리는 직접 만든 가상 물고기', '검수 시간(경보 × 5분)은 예시값', '숫자는 교육용 예시이며 경영·투자 권고가 아님'],
                prev=('04_guessing.html', '4장 · 맞히기'), depth=1)
    return build(P, title='실전 연습장 — 어시장 운영 시뮬레이터 · 비지도학습 물고기 연구실',
                 desc='진열대 정리(군집), 물고기 지도(PCA), 검수대(가린 무게·범위 밖 경보)를 직접 조작하며 미션 아홉 개를 푸는 비지도학습 실전 연습장.',
                 nav=[('#first', '3줄'), ('#shelf', '① 진열대'), ('#map', '② 지도'), ('#check', '③ 검수대'), ('#close', '마무리')],
                 cover_html=cover('cover_05', '마지막 장 · 실전 연습장', '어시장 운영 시뮬레이터', depth=1), hero=hero_html, body=b, gloss=GLOSS, quizzes={}, page_js=JS,
                 with_test=True, depth=1, og='og_05')


if __name__ == '__main__':
    print(main())
