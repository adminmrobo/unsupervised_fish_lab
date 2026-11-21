# -*- coding: utf-8 -*-
"""목차 · 비지도학습 물고기 연구실"""
from lib import *

P = 'index.html'
COLAB = 'https://colab.research.google.com/drive/19BdWcG0mjgrbJ3pwlqzBwbQ7Qt2hh3DN?usp=sharing'


WORK = {'01_no_answer_key.html': '단위가 섞인 데이터(센서, 고객 기록)를 비교하기 전에 눈금부터 맞춥니다.',
        '02_grouping.html': '고객·설비를 패턴별로 묶고, 묶음마다 대표 기록을 읽어 사람이 이름을 붙입니다.',
        '03_folding.html': '변수 수십 개를 지도 한 장으로 요약해 대시보드에 띄웁니다.',
        '04_guessing.html': '빠진 값을 채우고, 처음 보는 데이터에는 "모른다" 경보를 붙입니다.',
        'practice/index.html': '조건을 바꿔도 결론이 유지되는지 직접 확인합니다.'}


def body():
    s_ = R['supervised']; kr = R['kmr']; pc = R['pca']; mw = R['mask_weight']; av = R['ae_vs_pca']; km = R['knn_map']
    b = three([
        ('무엇을', '어시장에서 잰 물고기 1,554마리의 종 이름표를 덮고, 측정값 여섯 개만으로 무리를 나누고(묶기), 지도를 그리고(접기), 가린 값을 맞히는(맞히기) 비지도학습을 기초부터 배웁니다.'),
        ('왜 중요한가', '현장 데이터 대부분에는 정답표가 없습니다. 정답표 없이 데이터의 모양을 읽는 힘이 데이터를 처음 받았을 때의 첫걸음입니다.'),
        ('업무에서는', '고객 묶기, 센서 요약 대시보드, 빠진 값 채우기, 처음 보는 데이터 걸러내기에 그대로 씁니다.')],
        '코드·수식을 몰라도 됩니다. 앞 시리즈(지도학습)에서 같은 물고기로 종을 맞혀 봤다면, 장마다 나오는 「모아의 지도학습 노트」가 그때와 지금을 나란히 보여 줍니다.',
        title='처음 오신 분께 — 이 시리즈를 3줄로')
    b += ('<section class="level" id="cast"><div class="wrap"><h2>연구실 식구</h2>' + cast_cards([
        ('doc', 'board', '해설과 판정. 이 시리즈에서는 친절한 선생님 역할도 함께 맡습니다. 판정은 언제나 숫자대로.'),
        ('asst', 'proud', '실험 진행과 숫자 발표. 수식이 나오면 여러분 대신 하나씩 묻습니다.'),
        ('fly', 'magnify', '의심하는 쪽. 단순한 방법, 검증, 숨은 함정을 고릅니다.'),
        ('robo', 'smile', '확신하는 쪽. 크고 많은 쪽에 겁니다. 악역은 아닙니다.'),
        ('moa', 'report', '지도학습 시리즈의 기록을 모아 두었다가 "그때와 지금"을 비교해 줍니다.'),
        ('sia', 'guide', '순서 정리와 안내. 단계가 바뀔 때 길을 알려 줍니다.')]) + '</div></section>')

    b += section('compare', '지도학습과 비지도학습 — 같은 물고기, 다른 질문',
                 '<p>앞 시리즈 <a href="%s">「Fish Market Data로 쉽게 따라하는 머신러닝」</a>은 같은 1,554마리로 종을 맞혔습니다(지도학습). 이 시리즈는 이름표를 덮고 시작합니다. 같은 데이터에 던지는 질문이 어떻게 바뀌는지 한 표로 봅니다.</p>' % SUP_SITE +
                 '<div class="tw"><table class="tb"><tr><th></th><th>지도학습 (앞 시리즈)</th><th>비지도학습 (이 시리즈)</th></tr>'
                 '<tr><td>받는 것</td><td>측정값 6개 + 종 이름</td><td>측정값 6개만</td></tr>'
                 '<tr><td>질문</td><td>"이 물고기는 무슨 종인가?"</td><td>"어떤 물고기끼리 닮았나? 숫자를 줄여도 모양이 남나? 가린 값을 맞힐 수 있나?"</td></tr>'
                 '<tr><td>채점</td><td>정답률 — 이웃 하나 보기(KNN) %s, 로지스틱 회귀 %s (물고기 단위 교차검증)</td><td>모양 점수 — 실루엣 %s(체형 k=3), 두 축이 남긴 흔들림 %s, 시험 복원 오차 %s</td></tr>'
                 '<tr><td>이름표의 자리</td><td>학습 재료</td><td>마지막 대조용 — 주머니와 종의 대조 점수 %s, 지도 위 이웃 5마리 정답률 %s</td></tr>'
                 '<tr><td>같은 도구</td><td colspan="2">거리, 표준화, 이웃(KNN), 신경망 — 두 시리즈에 모두 나옵니다. 쓰는 목적이 다를 뿐입니다.</td></tr></table></div>' % (
                     pct(s_['knn1_group_cv']), pct(s_['logit_group_cv']), num(kr['3']['sil'], 3), pct(pc['evr'][0] + pc['evr'][1]), num(av['ae_test_mse'], 4), num(kr['3']['ari'], 3), pct(km['pc2_k5_test_acc']))
                 + panel('p0', '미리 보기 · 이름표를 덮으면', '실제 데이터 1,554마리',
                         '<div class="ctrl"><div class="group"><button class="bt" data-m="sp" aria-pressed="true">이름표 보기 (지도학습)</button><button class="bt" data-m="no" aria-pressed="false">이름표 덮기 (비지도학습)</button></div></div>'
                         + canvas('cv0', 320, '체형 비율 평면 위 물고기 1,554마리') + '<div class="legend" id="lg0"></div><div class="insight" id="in0" aria-live="polite"></div>', real=True))

    toc = [('01_no_answer_key.html', '1장', '정답표 없이 배운다 — 거리와 표준화', ['1-1 세 가지 배우는 법 (지도·비지도·자기지도)', '1-2 두 물고기 사이의 거리', '1-3 표준화', '대결: 표준화를 할까, 말까 (F · 초파리 승)']),
           ('02_grouping.html', '2장', '묶기 — 군집화', ['2-1 k-평균', '2-2 엘보', '2-3 실루엣', '2-4 계층 군집', '2-5 체형 세 갈래와 이름표', '대결: 주머니 3개 vs 7개 (F · 초파리 승)']),
           ('03_folding.html', '3장', '접기 — 차원 축소', ['3-1 겹친 정보', '3-2 가장 길게 뻗은 방향', '3-3 PCA 네 걸음', '3-4 물고기 지도', '3-5 복원과 잃은 것', '대결: 두 축 vs 여섯 축 (R · 주판봇 승)']),
           ('04_guessing.html', '4장', '맞히기 — 자기지도학습', ['4-1 가린 무게 맞히기', '4-2 오토인코더', '4-3 지도 위 이웃 찾기', '4-4 배운 범위 밖 경보', '대결: PCA vs 오토인코더 (R · 주판봇 승)']),
           ('practice/index.html', '마지막 장', '실전 연습장 — 어시장 운영 시뮬레이터', ['진열대 정리 (군집)', '물고기 지도 만들기 (PCA)', '검수대 (가린 무게·범위 밖)'])]
    b += section('toc', '목차',
                 '<div class="mapbar"><span>정답표 없이</span><i>→</i><span>묶기</span><i>→</i><span>접기</span><i>→</i><span>맞히기</span><i>→</i><span class="on">실전 연습장</span></div>'
                 '<div class="toc">' + ''.join('<a href="%s"><span class="k">%s</span><b>%s</b><ul>%s</ul><span class="small"><b>업무에서는</b> %s</span></a>' % (h, k, t, ''.join('<li>%s</li>' % x for x in li), WORK[h]) for h, k, t, li in toc) + '</div>'
                 + say('sia', 'guide', '1장부터 차례로 읽기를 권해요. 앞 단계의 결과가 다음 단계의 재료가 됩니다. 이미 아는 장은 건너뛰어도 괜찮습니다.'))

    b += section('record', '대결 전적 — 초파리 연구원 vs 주판봇',
                 '<div class="tw"><table class="tb"><tr><th>장</th><th>대결 질문</th><th>판정 기준</th><th>결과</th></tr>'
                 '<tr><td>1장</td><td>표준화를 할까, 말까</td><td>가장 가까운 이웃이 같은 종인 비율</td><td>초파리 승 (%s 대 %s)</td></tr>'
                 '<tr><td>2장</td><td>주머니 3개 vs 7개</td><td>평균 실루엣</td><td>초파리 승 (약 %s 대 %s)</td></tr>'
                 '<tr><td>3장</td><td>두 축 지도 vs 여섯 축 전부</td><td>가장 가까운 이웃이 같은 종인 비율</td><td>주판봇 승 (%s 대 %s)</td></tr>'
                 '<tr><td>4장</td><td>PCA vs 오토인코더</td><td>시험 복원 오차 (작을수록 좋음)</td><td>주판봇 승 (%s 대 %s)</td></tr></table></div>'
                 '<p>2승 2패입니다. "단순한 게 늘 정답"도, "큰 게 늘 정답"도 아닙니다. 데이터와 질문에 따라 판정이 갈립니다.</p>' % (
                     pct(R['nn_agree']['std']), pct(R['nn_agree']['raw']), num(kr['3']['sil'], 2), num(kr['7']['sil'], 2),
                     pct(R['nn_agree_pc']['pc2']), pct(R['nn_agree_pc']['all6']), num(av['pca2_test_mse'], 4), num(av['ae_test_mse'], 4)))

    b += section('data', '데이터와 실습',
                 '<div class="tw"><table class="tb"><tr><th>항목</th><th>내용</th></tr>'
                 '<tr><td>데이터</td><td>Kaggle Fish Market(물고기 7종 159마리, CC BY 4.0)을 종별 평균·분산을 지키며 10배로 늘린 1,590행에서, 무게 0인 1행과 똑같은 35행을 뺀 1,554마리. 파일: <code>data/fish_market_x10.csv</code> (지도학습 시리즈와 같은 파일)</td></tr>'
                 '<tr><td>측정값</td><td>무게(g), 길이1·길이2·길이3(cm, 재는 기준이 다른 세 길이), 높이(cm), 폭(cm)</td></tr>'
                 '<tr><td>숫자의 원본</td><td><code>code/analysis.py</code> → <code>data/results.json</code> (scikit-learn 1.9.1). 페이지의 실험은 같은 데이터로 브라우저에서 직접 다시 계산합니다</td></tr>'
                 '<tr><td>실습 노트북</td><td><a href="%s">Colab 실습 노트북 (강의용)</a></td></tr>'
                 '<tr><td>원자료</td><td>안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 (2026, 35쪽). 원자료와 다르게 적은 곳은 해당 장에 "바꿉니다"로 밝혔습니다</td></tr>'
                 '<tr><td>저장소</td><td><a href="%s">%s</a></td></tr></table></div>' % (COLAB, REPO, REPO.replace('https://', '')))
    b += outro([('doc', 'front', '이 시리즈의 한 줄. 비지도학습은 정답이 없는 학습이 아니라, 정답의 위치가 다른 학습입니다. 정답은 데이터의 모양 안에 있습니다.'),
                ('fly', 'clip', '대신 자를 고르고, 잃은 걸 확인하고, 범위 밖을 걸러내는 건 사람 몫이야.'),
                ('robo', 'smile', '전적은 2승 2패. 큰 모델이 이길 때도 있다는 걸 잊지 마!'),
                ('asst', 'proud', '1장부터 같이 가요. 버튼만 눌러도 따라올 수 있게 만들었어요.')],
               '연구실 식구 네 명이 어시장 앞에서 이름표를 덮은 물고기 상자를 열어 보는 장면')
    return b


JS = r'''
var D=FL.load(),X=D.X,N=D.n,SPC=FL.SPC;var RAT=X.map(function(r){return [r[4]/r[1],r[5]/r[1]];});
(function(){var cv=$('#cv0'),m='sp';
  function draw(){var f=fit(cv),g=f.c,A=FL.axes(g,f.W,f.H,{xmin:.12,xmax:.6,ymin:.08,ymax:.24,xlab:'높이 ÷ 길이1 (납작한 정도)',ylab:'폭 ÷ 길이1',padL:58});
    for(var i=0;i<N;i++)FL.dot(g,A.sx(RAT[i][0]),A.sy(RAT[i][1]),2.6,m==='sp'?SPC[D.sp[i]]:'#8a96a3',m==='sp'?.7:.45);stamp(g,f.W,'실제 데이터');}
  function info(){if(m==='sp')FL.spLegend($('#lg0'));else $('#lg0').innerHTML='<span><i style="background:#8a96a3"></i>이름표 없는 물고기</span>';
    $('#in0').innerHTML=m==='sp'?'<p class="g">이름표가 있으면 색을 맞히는 규칙을 배웁니다(지도학습).</p>':'<p class="m">이름표를 덮어도 점들은 세 갈래(납작·중간·길쭉)로 모여 있습니다. 이 갈래를 이름표 없이 찾아내는 것이 2장의 일입니다.</p>';}
  $$('#p0 [data-m]').forEach(function(bt){bt.addEventListener('click',function(){m=bt.dataset.m;$$('#p0 [data-m]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();info();});});
  info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
'''

GLOSS = {
    '비지도학습': ['비지도학습 (unsupervised learning)', '정답 없이 입력만으로 데이터의 구조(무리, 방향, 관계)를 찾는 방법.'],
    '지도학습': ['지도학습 (supervised learning)', '입력과 정답(이름표)을 함께 주고 정답을 맞히도록 배우는 방법.'],
    '자기지도학습': ['자기지도학습 (self-supervised learning)', '데이터 일부를 가리고 맞히게 해서 데이터 자신을 정답으로 쓰는 방법.'],
    '실루엣': ['실루엣 점수', '내 무리엔 붙고 옆 무리와는 떨어진 정도. −1~+1. 2장.'],
    '교차검증': ['교차검증 (cross-validation)', '데이터를 여러 번 나눠 학습·채점을 되풀이해 점수의 흔들림을 줄이는 방법.'],
    '복원 오차': ['복원 오차', '접었다 편 값과 원래 값의 차이. 3장·4장.'],
}


def main():
    hero_html = hero('비지도학습 물고기 연구실 · 목차', '라벨링 없이 맞추는 AI — 비지도학습', '정답표가 없어도, 데이터 안에 숨은 모양을 찾아낼 수 있을까?',
                     '앞 시리즈에서 우리는 물고기 종 이름표를 보며 종을 맞히는 법(지도학습)을 배웠습니다. 이번에는 이름표를 덮습니다. '
                     '숫자 여섯 개만 남은 물고기 1,554마리로 <b>묶고(군집화)</b>, <b>접고(차원 축소)</b>, <b>가린 부분을 스스로 맞히는(자기지도학습)</b> 세 가지 방법을 기초부터 차례로 배우고, 마지막에 어시장 시뮬레이터에서 직접 써 봅니다.',
                     [('1,554', '물고기 (이름표는 덮음)', 'g'), ('4 + 1', '장 + 실전 연습장', 'i'), (pct(R['pca']['evr'][0] + R['pca']['evr'][1]), '두 축 지도가 남긴 흔들림', 'm'), ('2 : 2', '초파리 vs 주판봇 전적', 'a')],
                     [('doc', 'front', '어서 오세요. 이번 시리즈는 정답표 없이 배우는 법입니다. 같은 물고기, 다른 질문이에요.'),
                      ('asst', 'smile', '지도학습 때 쓴 물고기 그대로예요? 그럼 그때랑 비교하면서 보면 되겠네요.'),
                      ('fly', 'point', '이름표를 덮으면 더 조심해야 해. 채점해 줄 정답이 없으니까.'),
                      ('robo', 'coin', '정답표 없이도 큰 모델이면 다 찾아내지. 이번 시리즈는 내 거야!')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a> 증강본 fish_market_x10.csv'),
                 ('원자료', '안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 (2026, 35쪽)'),
                 ('지도학습 비교 수치', 'code/analysis.py (scikit-learn 1.9.1, StratifiedGroupKFold 5겹)'),
                 ('교과서', 'Hastie, Tibshirani, Friedman (2009). The Elements of Statistical Learning, 2nd ed., 14장 Unsupervised Learning. Springer')],
                ['표지 대체 그림(픽셀 물고기와 주머니)은 설명용', '대결 결과 괄호 안 숫자는 각 장의 계산값'],
                nxt=('01_no_answer_key.html', '1장 · 정답표 없이 배운다'))
    return build(P, title='비지도학습 물고기 연구실 — 라벨링 없이 맞추는 AI (목차)',
                 desc='어시장 물고기 1,554마리의 종 이름표를 덮고 묶기(군집화)·접기(PCA)·맞히기(자기지도학습)를 기초부터 배우는 연구실 해설 시리즈. 지도학습과 나란히 비교.',
                 nav=[('#first', '3줄'), ('#cast', '식구'), ('#compare', '지도 vs 비지도'), ('#toc', '목차'), ('#record', '대결 전적'), ('#data', '데이터')],
                 cover_html=cover('cover_00', '비지도학습 물고기 연구실', '라벨링 없이 맞추는 AI — 묶고, 접고, 맞힌다'),
                 hero=hero_html, body=b, gloss=GLOSS, quizzes={}, page_js=JS, og='og_00')


if __name__ == '__main__':
    print(main())
