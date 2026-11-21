# -*- coding: utf-8 -*-
"""1장 · 정답표 없이 배운다 — 세 가지 배우는 법, 거리, 표준화"""
from lib import *

P = '01_no_answer_key.html'
na = R['nn_agree']; ws = R['weight_share']; de = R['dist_example']; sup_ = R['supervised']


def body():
    b = three([
        ('무엇을', '어시장 물고기 1,554마리의 종 이름표를 덮고, 측정값 여섯 개만으로 "닮은 물고기"를 찾는 첫걸음을 뗍니다.'),
        ('왜 중요한가', '이름표(정답표)를 붙이는 일은 비싸고 느립니다. 이름표 없이 데이터의 모양을 읽는 힘이 비지도학습입니다.'),
        ('업무에서는', '고객 기록, 설비 센서, 거래 내역처럼 정답이 적혀 있지 않은 데이터가 훨씬 많습니다. 그 데이터를 처음 볼 때 쓰는 방법입니다.')],
        '코드·수식을 몰라도 됩니다. 버튼을 누르고 그림을 보며 따라오면 됩니다. 수식은 조수 하루가 하나씩 물어봅니다.',
        [('k-NN', 'k-Nearest Neighbors, 가장 가까운 이웃 k개'), ('z', '표준화한 값 (z 점수)'), ('Δ', '델타, 두 값의 차이')])

    b += ('<section class="level" id="cast"><div class="wrap"><h2>이 장의 식구와 사용법</h2>' + cast_cards([
        ('doc', 'board', '해설과 판정. 이 시리즈에서는 친절한 선생님 역할도 함께 맡습니다.'),
        ('asst', 'smile', '실험 진행과 숫자 발표. 수식이 나오면 여러분 대신 묻습니다.'),
        ('fly', 'magnify', '의심하는 쪽. "그 숫자, 정말 그럴듯해?"를 입에 달고 삽니다.'),
        ('robo', 'smile', '확신하는 쪽. 큰 숫자와 큰 모델을 좋아합니다. 악역은 아닙니다.'),
        ('moa', 'report', '지도학습 시리즈의 기록을 모아 두었다가, 지금 배우는 것과 나란히 보여 줍니다.'),
        ('sia', 'guide', '순서를 정리해 안내합니다. 단계가 바뀔 때 길을 알려 줍니다.')]) +
        '<p>밑줄 친 말을 누르거나 마우스를 올리면 뜻이 나옵니다. 오른쪽 아래 도우미에서 밑줄을 끌 수 있습니다. '
        '앞 시리즈 <a href="%s">「Fish Market Data로 쉽게 따라하는 머신러닝」</a>(지도학습)을 보지 않았어도 읽을 수 있게 썼습니다.</p></div></section>' % SUP_SITE)

    b += section('why', '왜 이 주제인가', '<div class="steps">'
                 '<div><span class="n">1</span><h4>정답표는 비싸다</h4><p>물고기 1,554마리에 종 이름을 붙이려면 전문가가 한 마리씩 봐야 합니다. 현장 데이터 대부분은 이름표가 없습니다.</p></div>'
                 '<div><span class="n">2</span><h4>모양부터 본다</h4><p>이름표가 없어도 값들 사이의 거리와 방향은 남아 있습니다. 그것만으로 무리를 나누고 지도를 그릴 수 있습니다.</p></div>'
                 '<div><span class="n">3</span><h4>지도학습의 짝</h4><p>지도학습 시리즈에서 쓴 거리, 표준화, 이웃이 여기서 다시 나옵니다. 같은 도구를 정답표 없이 쓰는 법을 배웁니다.</p></div></div>'
                 + say('doc', 'front', '이 시리즈는 묶기(2장) → 접기(3장) → 맞히기(4장) 순서로 갑니다. 1장은 그 셋이 모두 쓰는 바닥, "거리"와 "표준화"를 다집니다.'))

    b += section('map', '큰 그림 — 이 장은 어디쯤인가',
                 '<div class="mapbar" aria-label="시리즈 흐름"><span class="on">1장 · 정답표 없이 (거리·표준화)</span><i>→</i><span>2장 · 묶기 (군집화)</span><i>→</i>'
                 '<span>3장 · 접기 (차원 축소)</span><i>→</i><span>4장 · 맞히기 (자기지도)</span><i>→</i><span>실전 연습장</span></div>'
                 '<p>앞 단계의 출력이 다음 단계의 입력이 됩니다. 1장에서 만든 "표준화한 측정값"이 2장의 군집화, 3장의 PCA, 4장의 오토인코더에 그대로 들어갑니다. '
                 '종 이름표는 마지막에 "AI가 찾은 무리가 실제 종과 얼마나 닮았나"를 대조할 때만 다시 꺼냅니다.</p>'
                 '<div class="tw"><table class="tb"><tr><th>이 시리즈의 데이터</th><th>내용</th></tr>'
                 '<tr><td>물고기 수</td><td>1,554마리 (원본 158마리를 종별 평균·분산을 지키며 10배로 늘린 뒤, 무게 0인 행과 똑같은 행을 뺌)</td></tr>'
                 '<tr><td>측정값 6개 (특성)</td><td>무게(g), 길이 세 가지(cm, 재는 기준이 다른 세 값), 높이(cm), 폭(cm)</td></tr>'
                 '<tr><td>덮어 둔 정답표</td><td>종 7가지 — 도미 348 · 파르키 104 · 농어 560 · 강꼬치고기 164 · 로치 192 · 빙어 138 · 흰송어 48</td></tr>'
                 '<tr><td>같은 물고기 묶음</td><td>같은 원본에서 늘린 물고기는 같은 번호(seed_id)를 가집니다. 채점할 때 이 묶음을 갈라 놓지 않습니다</td></tr></table></div>')

    # ── 1-1 세 가지 배우는 법
    s = say('doc', 'think', '상황 하나. 회사에 고객 기록 10만 건이 쌓였는데, 누가 어떤 고객인지 적어 둔 사람이 없다면 어떻게 시작할까요?')
    s += duo(why([('문제 상황', '이름표(정답표)를 붙이려면 사람이 한 건씩 봐야 해서 비싸고 느립니다.'),
                  ('앞 방법의 한계', '지도학습은 이름표가 있어야 시작할 수 있습니다. 이름표가 없으면 아무것도 배우지 못합니다.'),
                  ('해법', '이름표 없이 값들의 모양(가까움, 퍼진 방향, 서로의 관계)에서 규칙을 찾습니다.')],
                 '시험지(정답)가 없어도 문제집 문제들의 생김새만 보고 "이건 같은 단원이네"라고 나눌 수는 있습니다.'),
             pair('일상으로 치면', '선생님이 채점해 주는 공부(지도), 문제끼리 비슷한 것을 스스로 묶어 보는 공부(비지도), 답을 가려 놓고 스스로 맞혀 보는 공부(자기지도)가 있습니다.',
                  '모델에서는', '지도학습은 측정값과 종 이름을 함께 받습니다. 비지도학습은 측정값만 받습니다. 자기지도학습은 측정값 일부를 가리고 나머지로 맞히게 해서, 가린 값을 정답으로 씁니다.'))
    s += sup('물고기마다 측정값 여섯 개와 종 이름이 함께 있었습니다. 모델은 종을 맞히도록 배웠고, 처음 보는 물고기의 정답률(정확도)로 채점했습니다. '
             '같은 방식으로 다시 재면 이웃 하나 보기(KNN) %s, 로지스틱 회귀 %s입니다.' % (pct(sup_['knn1_group_cv']), pct(sup_['logit_group_cv'])),
             '측정값 여섯 개만 씁니다. 목표는 "닮은 것끼리 묶기", "여분을 접기", "가린 값 맞히기"입니다. 정답이 없으니 실루엣 점수, 설명된 분산, 복원 오차 같은 "모양 점수"로 채점합니다.')
    s += talk([('doc', 'think', '이름표를 덮으면 물고기 1,554마리는 그냥 숫자 더미일까요?'),
               ('robo', 'coin', '숫자 더미지! 정답이 없으면 배울 것도 없어. 이번 판은 패스.'),
               ('fly', 'point', '성급해. 아래에서 "이름표 덮기"를 눌러 봐. 점들이 아무렇게나 흩어져 있나?'),
               ('asst', 'report', '덮어도 점들이 줄을 서 있어요. 길이가 길면 무게도 무거운 띠 모양이 보여요.')])
    s += panel('p11', '실험 · 같은 물고기, 세 가지 배우는 법', '실제 데이터 1,554마리',
               '<div class="ctrl"><div class="group"><span class="glabel">배우는 법</span>'
               '<button class="bt" data-m="sup" aria-pressed="true">지도학습 · 이름표 보기</button>'
               '<button class="bt" data-m="unsup" aria-pressed="false">비지도학습 · 이름표 덮기</button>'
               '<button class="bt" data-m="self" aria-pressed="false">자기지도학습 · 무게 가리기</button></div></div>'
               + canvas('cv11', 340, '길이1(가로)과 무게(세로)로 그린 물고기 1,554마리 산점도') +
               '<div class="legend" id="lg11"></div><section class="kpis" id="k11" aria-label="숫자 요약"></section>'
               '<div class="insight" id="in11" aria-live="polite"></div>', real=True)
    s += explain(['지도학습은 점마다 색(종 이름)을 보고, 색을 맞히는 규칙을 배웁니다.',
                  '비지도학습은 색이 없습니다. 그래도 점들이 모인 곳과 비어 있는 곳, 길게 뻗은 방향은 그대로 남아 있습니다.',
                  '자기지도학습은 값 하나(무게)를 가리고 나머지로 맞힙니다. 가린 값은 원래 데이터에 있으니 사람이 정답을 만들 필요가 없습니다.'],
                 '비지도학습이 찾는 것은 "닮음"이지 "정체"가 아닙니다. 같은 무리에 다른 종이 섞일 수 있고, 그 무리가 무엇인지 이름을 붙이는 일은 결국 사람이 합니다.')
    s += codefold([('X = df[FEATS]', '측정값 여섯 열만 꺼냅니다. 비지도학습은 여기서 시작합니다.'),
                   ('y = df["species"]', '종 이름 열. 지도학습 때만 썼고, 이 시리즈에서는 마지막 대조에만 씁니다.')])
    s += quiz('q11')
    b += step('s1', '1-1', '배우는 법은 세 가지 — 정답표를 누가, 언제 만드나', ['방법: 지도 · 비지도 · 자기지도', '일상: 시험지가 있는 공부와 없는 공부'], s)

    # ── 1-2 거리
    s = say('doc', 'think', '두 물고기가 얼마나 닮았는지 숫자 하나로 말해야 한다면, 무엇을 재면 될까요?')
    s += recap('피타고라스 정리', '<p>직각삼각형에서 빗변의 길이는 √(가로² + 세로²)입니다. 가로 3, 세로 4면 빗변은 √(9+16) = 5입니다. 아래 "거리"는 이 빗변을 재는 일입니다.</p>')
    s += duo(why([('문제 상황', '사람은 눈으로 "이 둘은 비슷하네"라고 하지만, 컴퓨터에는 그 느낌을 숫자로 줘야 합니다.'),
                  ('앞 방법의 한계', '눈대중은 사람마다 다르고, 1,554마리를 하나하나 비교할 수 없습니다.'),
                  ('해법', '물고기 한 마리를 숫자 여섯 개의 좌표로 보고, 두 좌표 사이의 거리를 잽니다. 거리가 짧으면 닮은 것입니다.')],
                 '지도 위 두 마을이 가까우면 "가깝다"고 하듯, 측정값이 비슷한 물고기는 좌표 공간에서 가깝습니다.'),
             mathbox('√, Δ, 제곱이 한꺼번에 나와요. 이걸 어떻게 읽어요?', '피타고라스 정리(중학교 3학년) — 두 점 사이의 거리',
                     'd = √( Δ무게² + Δ길이² )',
                     [('d', '디', '거리(distance). 두 물고기가 떨어진 정도'), ('Δ', '델타', '두 값의 차이. Δ무게 = 무게A − 무게B'),
                      ('²', '제곱', '차이를 자기 자신과 곱함. 음수도 양수로 바뀝니다'), ('√', '루트', '제곱을 되돌림. 넓이를 길이로 바꿉니다')],
                     '원본 도미 두 마리: 무게 242g과 290g(Δ = 48), 길이1 23.2cm와 24.0cm(Δ = 0.8). '
                     'd = √(48² + 0.8²) = √(2,304 + 0.64) = √2,304.64 ≈ <b>48.0</b>. 여섯 값을 모두 넣어도 %s입니다.' % num(de['raw'], 2),
                     '변수가 여섯 개면 차이의 제곱을 여섯 개 더하고 루트를 씌우면 되는 거네요. 그런데 48 중 거의 전부가 무게에서 나왔어요!'))
    s += pair('일상으로 치면', '새가 날아가는 직선 거리(유클리드)와, 골목길을 가로로 갔다가 세로로 가는 거리(맨해튼)가 다릅니다. 무엇으로 재느냐에 따라 "가까운 집"이 바뀝니다.',
              '모델에서는', '유클리드 거리가 기본입니다. 맨해튼 거리는 차이의 절댓값을 그냥 더해서 큰 차이 하나에 덜 흔들립니다. 크기를 빼고 생김새만 보려면 "높이 ÷ 길이" 같은 체형 비율로 잽니다.')
    s += sup('가장 가까운 이웃의 종 이름을 그대로 답하는 KNN이 바로 이 거리를 썼습니다. 이웃이 누구냐가 곧 답이었습니다.',
             '같은 거리를 쓰지만, 이웃의 이름표는 보지 않습니다. "누가 누구와 가까운가"라는 관계 자체가 배울 거리입니다.')
    s += talk([('doc', 'board', '도미 두 마리의 거리 48. 이 숫자가 "닮음"을 잘 말해 준다고 볼까요?'),
               ('robo', 'coin', '당연하지. 숫자는 거짓말을 안 해. 48이면 48만큼 다른 거야.'),
               ('fly', 'point', '48 중에 무게가 몇 %인지 봐. 아래에서 두 물고기를 바꿔 가며 "차이의 몫" 막대를 눌러 봐.'),
               ('asst', 'report', '무게 몫이 거의 100%예요. 길이·높이 차이는 거리에 거의 안 들어가요.')])
    s += panel('p12', '실험 · 두 물고기 사이의 거리', '실제 측정값',
               '<div class="ctrl"><div class="group"><span class="glabel">물고기 A</span><select class="sel" id="a12sp"></select><input type="range" id="a12i" min="0" max="0" value="0" aria-label="물고기 A 번호"><span class="val" id="a12v"></span></div>'
               '<div class="group"><span class="glabel">물고기 B</span><select class="sel" id="b12sp"></select><input type="range" id="b12i" min="0" max="0" value="1" aria-label="물고기 B 번호"><span class="val" id="b12v"></span></div></div>'
               + canvas('cv12', 230, '두 물고기를 실제 길이와 높이 비율로 그린 그림') +
               '<div class="tw"><table class="tb mini-table" id="t12"></table></div><section class="kpis" id="k12" aria-label="거리 요약"></section>'
               '<div class="insight" id="in12" aria-live="polite"></div>', real=True)
    s += explain(['물고기 한 마리 = 숫자 여섯 개의 좌표. 두 좌표의 차이를 제곱해 더하고 루트를 씌우면 유클리드 거리입니다.',
                  '맨해튼 거리는 차이의 절댓값을 더합니다. 숫자는 다르지만, 둘 다 무게 차이가 대부분을 차지합니다.',
                  '체형 비율(높이 ÷ 길이1)의 차이는 크기를 뺀 생김새만 봅니다. 큰 도미와 작은 도미가 가까워집니다.'],
                 '원 단위(그램·센티미터) 그대로 재면 숫자가 큰 무게가 거리를 거의 혼자 정합니다. 이 문제를 다음 단계의 표준화가 풉니다. 어떤 자로 잴지는 사람이 고르고, 그 자로 계산하는 일은 AI가 합니다.')
    s += codefold([('np.linalg.norm(a - b)', '두 물고기 a, b의 유클리드 거리. 차이의 제곱합에 루트'),
                   ('np.abs(a - b).sum()', '맨해튼 거리. 차이의 절댓값 합')])
    s += quiz('q12')
    b += step('s2', '1-2', '"비슷하다"를 숫자로 — 두 물고기 사이의 거리', ['방법: 유클리드 · 맨해튼 · 체형 비율', '일상: 직선 길과 골목길'], s)

    # ── 1-3 표준화
    s = say('doc', 'think', '키(센티미터)와 연봉(원)을 그대로 더해서 "비슷한 사람"을 찾으면 어떻게 될까요? 연봉만 보고 찾게 됩니다. 물고기도 같습니다.')
    s += recap('평균과 표준편차', '<p>평균은 값들의 가운데, 표준편차는 값들이 평균에서 보통 얼마나 떨어져 있는지입니다. 이 데이터의 무게는 평균 %sg, 표준편차 %sg입니다.</p>' % (
        num(R['desc']['weight_g']['mean'], 1), num(R['desc']['weight_g']['std'], 1)))
    s += duo(why([('문제 상황', '무게는 수천 그램, 폭은 한 자리 센티미터입니다. 같은 1이라도 무게 1g과 폭 1cm는 무게가 전혀 다릅니다.'),
                  ('앞 방법의 한계', '원 단위 그대로 거리를 재면 무게가 거리의 대부분을 차지합니다. 생김새 정보가 묻힙니다.'),
                  ('해법', '변수마다 평균을 빼고 표준편차로 나눠, 모든 변수를 "평균 0, 표준편차 1"이라는 같은 눈금으로 바꿉니다.')],
                 '시험 점수를 "반 평균보다 몇 걸음 위인가"로 바꾸면, 국어 점수와 수학 점수를 나란히 비교할 수 있습니다.'),
             mathbox('z, x, 평균, 표준편차… 기호가 네 개나 돼요. 무슨 순서로 계산해요?', '확률과 통계(고등학교) — 표준화(평균 0, 표준편차 1로 바꾸기)',
                     'z = (x − 평균) ÷ 표준편차',
                     [('x', '엑스', '원래 값. 예: 무게 242g'), ('평균', '', '그 변수 전체의 가운데 값'), ('표준편차', '', '보통 떨어진 거리. 눈금 한 걸음'),
                      ('z', '제트', '표준화한 값. "평균에서 몇 걸음 떨어졌나"')],
                     '무게 242g → (242 − %s) ÷ %s ≈ <b>−0.43</b> (평균보다 0.43걸음 가벼움). '
                     '길이1 23.2cm → (23.2 − %s) ÷ %s ≈ <b>−0.30</b>.' % (num(R['scaler']['mean'][0], 1), num(R['scaler']['scale'][0], 1),
                                                                         num(R['scaler']['mean'][1], 2), num(R['scaler']['scale'][1], 2)),
                     '빼고 나누면 끝이네요. 이제 무게 걸음과 길이 걸음을 같은 자로 잴 수 있어요.'))
    s += sup('KNN과 로지스틱 회귀 앞에 늘 표준화(StandardScaler)를 붙였습니다. 이유는 같습니다. 단위가 큰 변수가 판단을 독점하지 않게 하려고요.',
             '이름표 없이 거리만 믿고 가기 때문에 표준화가 더 중요합니다. 지도학습은 이름표가 틀린 쪽을 바로잡아 주지만, 비지도학습은 바로잡아 줄 정답이 없습니다.')
    s += talk([('doc', 'think', '표준화를 하면 무엇이 달라지는지, 숫자로 확인해 볼까요?'),
               ('robo', 'coin', '큰 숫자가 중요한 숫자야. 무게가 크니까 무게만 보면 되지!'),
               ('fly', 'point', '그 말이 맞는지 "표준화" 버튼을 눌러 봐. 무게가 차지하는 몫이 어떻게 바뀌나.'),
               ('asst', 'report', '이웃 거리에서 무게 몫이 %s에서 %s로 줄었어요. 다른 다섯 값이 목소리를 내기 시작해요.' % (pct(ws['raw']), pct(ws['std'])))])
    s += panel('p13', '실험 · 원 단위 그대로 vs 표준화', '실제 데이터로 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">눈금</span><button class="bt" data-s="raw" aria-pressed="true">원 단위 그대로</button>'
               '<button class="bt" data-s="std" aria-pressed="false">표준화</button></div></div>'
               + canvas('cv13', 300, '변수 여섯 개가 퍼진 범위를 같은 눈금 위에 그린 그림') +
               '<h4 style="margin-top:14px">가장 가까운 이웃과의 거리에서 각 변수가 차지하는 몫</h4><div class="vbars" id="vb13"></div>'
               '<section class="kpis" id="k13" aria-label="숫자 요약"></section><div class="insight" id="in13" aria-live="polite"></div>', real=True)
    s += explain(['표준화는 변수마다 "평균 0, 한 걸음 = 표준편차 1"로 눈금을 다시 매깁니다.',
                  '원 단위에서는 거리의 %s가 무게 차이였습니다. 표준화하면 %s로 줄고, 높이·폭 같은 생김새 정보가 거리에 들어옵니다.' % (pct(ws['raw']), pct(ws['std'])),
                  '이름표를 채점용으로만 꺼내 보면, 가장 가까운 이웃이 같은 종인 비율이 %s에서 %s로 올라갑니다.' % (pct(na['raw']), pct(na['std']))],
                 '표준화는 단위를 지울 뿐, 어떤 변수를 넣을지는 정해 주지 않습니다. 길이 세 값은 서로 상관이 0.99 이상이라, 그대로 넣으면 "길이" 정보가 세 표를 행사합니다. 이 문제는 3장(접기)에서 다룹니다.')
    s += aicheck('주판봇의 "대발견"',
                 '<p>주판봇이 원 단위 측정값 그대로 물고기를 세 무리로 나누고 외쳤습니다. "세 무리가 가벼운 것, 중간, 무거운 것으로 깔끔하게 나뉘었어! 물고기는 무게로 세 종류야!"</p>'
                 '<p><b>확인 질문</b> ① 왜 하필 무게 순서로 나뉘었을까요? ② 이 결론을 믿어도 될까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 원 단위에서는 무게가 거리의 대부분을 차지하니, 어떤 군집 방법을 써도 무게 순서로 나뉘기 쉽습니다. '
                 '② 믿으면 안 됩니다. 그 세 무리를 실제 종 이름과 대조하면 닮은 정도(조정 랜드 지수)가 %s로 거의 0입니다. 무리가 나뉜 이유가 "단위"였지 "물고기"가 아니었습니다.</p></details>' % num(R['raw_k3_ari'], 3))
    s += codefold([('Z = StandardScaler().fit_transform(X)', '여섯 열을 각각 평균 0, 표준편차 1로 바꿉니다'),
                   ('Z.mean(axis=0), Z.std(axis=0)', '바뀐 뒤 평균은 0, 표준편차는 1인지 확인합니다')])
    s += quiz('q13')
    b += step('s3', '1-3', '숫자의 크기는 지우자 — 표준화', ['방법: 표준화(z 점수)', '일상: 국어·수학 점수를 같은 눈금으로'], s)

    b += duel('d1', '표준화를 할까, 말까', '표준화한 여섯 값', '원 단위 그대로 여섯 값',
              '"단위가 다르면 같은 자로 잴 수 없어. 눈금부터 맞추자."', '"무게가 제일 큰 숫자잖아. 큰 숫자가 중요한 숫자야."',
              '가장 가까운 이웃이 같은 종인 비율 (이름표는 채점에만 씀)')

    b += section('sum', '정리 — 세 가지 배우는 법과 두 가지 도구',
                 '<div class="tw"><table class="tb"><tr><th></th><th>지도학습</th><th>비지도학습</th><th>자기지도학습</th></tr>'
                 '<tr><td>받는 것</td><td>측정값 + 종 이름</td><td>측정값만</td><td>측정값 (일부를 가림)</td></tr>'
                 '<tr><td>목표</td><td>종 맞히기</td><td>묶기 · 접기</td><td>가린 값 맞히기</td></tr>'
                 '<tr><td>채점</td><td>정확도 (정답과 비교)</td><td>모양 점수 (실루엣, 설명된 분산)</td><td>복원 오차 (가린 원래 값과 비교)</td></tr>'
                 '<tr><td>이 시리즈의 장</td><td>앞 시리즈</td><td>2장 · 3장</td><td>4장</td></tr></table></div>'
                 '<div class="steps"><div><span class="n">1</span><h4>거리</h4><p>닮음을 숫자로 바꾸는 자. 어떤 자를 고르느냐가 결과를 바꿉니다.</p></div>'
                 '<div><span class="n">2</span><h4>표준화</h4><p>단위를 지워 모든 변수가 같은 눈금으로 목소리를 내게 합니다.</p></div>'
                 '<div><span class="n">3</span><h4>이름표는 대조용</h4><p>이 시리즈에서 종 이름은 배울 때 쓰지 않고, AI가 찾은 것을 맞춰 볼 때만 씁니다.</p></div></div>'
                 + bridge('gen', '생성 AI로 치면', '대형 언어 모델은 문장마다 정답표를 붙이지 않고, 문장의 다음 단어를 가리고 맞히며 배웁니다. 4장에서 배울 자기지도학습이 그 바탕입니다.',
                          '언어 모델의 "거리"는 단어를 바꾼 숫자(임베딩) 사이에서 재며, 물고기 측정값처럼 사람이 뜻을 바로 읽을 수는 없습니다.')
                 + bridge('field', '현장에 옮기면', '센서 값(온도 ℃, 압력 kPa, 진동 mm/s)을 그대로 섞어 군집을 돌리면 숫자가 큰 압력이 모든 것을 정합니다. 표준화를 먼저 하고, 무엇을 넣었는지 기록으로 남깁니다.',
                          '표준화의 평균·표준편차는 학습 때 데이터로 정합니다. 새 데이터에 다시 계산하면 눈금이 흔들립니다.'))

    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 비지도학습은 정답표 없이 데이터의 모양을 읽는다. ② 닮음은 거리로 잰다. ③ 거리를 재기 전에 눈금(표준화)부터 맞춘다.'),
                ('fly', 'arms', '이름표를 덮어도 점들은 줄을 서 있었어. 다만 자를 잘못 고르면 엉뚱한 줄이 보이지.'),
                ('robo', 'sigh', '큰 숫자가 늘 중요한 건 아니었구나. 이번 판은 손절. 2장에서 본전 찾는다.'),
                ('asst', 'spark', '다음 장에서는 이 거리로 물고기를 실제로 주머니에 나눠 담아 볼게요.')],
               '연구실 식구 네 명이 어시장 진열대 앞에서 물고기 자를 들고 서 있는 장면')
    return b


GLOSS = {
    '지도학습': ['지도학습 (supervised learning)', '입력과 정답(이름표)을 함께 주고, 정답을 맞히도록 배우는 방법. 앞 시리즈의 물고기 종 분류가 이것입니다.'],
    '비지도학습': ['비지도학습 (unsupervised learning)', '정답 없이 입력만으로 데이터의 구조(무리, 방향, 관계)를 찾는 방법.'],
    '자기지도학습': ['자기지도학습 (self-supervised learning)', '데이터 일부를 가리고 나머지로 맞히게 해서, 데이터 자신을 정답으로 쓰는 방법.'],
    '정답표': ['정답표 (label, 이름표)', '데이터마다 붙인 정답. 이 시리즈에서는 물고기의 종 이름.'],
    '특성': ['특성 (feature)', '한 마리를 설명하는 숫자 열. 여기서는 무게·길이 세 가지·높이·폭의 여섯 열.'],
    '유클리드 거리': ['유클리드 거리 (Euclidean distance)', '두 점을 잇는 직선 길이. 각 차이를 제곱해 더하고 루트를 씌웁니다.'],
    '맨해튼 거리': ['맨해튼 거리 (Manhattan distance)', '차이의 절댓값을 그냥 더한 거리. 바둑판 골목길을 걷는 거리.'],
    '표준화': ['표준화 (standardization, z 점수)', '평균을 빼고 표준편차로 나눠, 변수마다 평균 0·표준편차 1로 바꾸는 일.'],
    '표준편차': ['표준편차 (standard deviation)', '값들이 평균에서 보통 얼마나 떨어져 있는지 나타내는 수.'],
    '이웃': ['이웃 (neighbor)', '거리로 쟀을 때 가장 가까운 데이터. KNN은 이웃의 이름표로 답합니다.'],
    '실루엣': ['실루엣 점수 (silhouette)', '각 점이 자기 무리에는 붙어 있고 옆 무리와는 떨어져 있는 정도. −1~+1. 2장에서 자세히.'],
    '조정 랜드 지수': ['조정 랜드 지수 (ARI)', 'AI가 나눈 무리와 실제 이름표가 얼마나 같은지 재는 대조 점수. 1이면 완전히 같고, 0이면 우연 수준.'],
}

QUIZ = {
    'q11': [{'q': '비지도학습이 학습할 때 받는 것은?', 'o': ['측정값과 종 이름', '측정값만', '종 이름만'], 'a': 1,
             'why': '비지도학습은 정답(종 이름) 없이 측정값만 받습니다.', 'hint': '"정답표가 없다"가 비지도학습의 뜻입니다.'},
            {'q': '자기지도학습에서 "정답"은 어디서 오나?', 'o': ['사람이 새로 붙인다', '가린 원래 값이 정답이다', '정답이 필요 없다'], 'a': 1,
             'why': '무게를 가리고 맞히면, 가린 무게가 곧 정답입니다. 데이터 안에 이미 있습니다.', 'hint': '가린 값은 어디에 있었나요?'}],
    'q12': [{'q': '원본 도미 두 마리의 유클리드 거리 48.04에서 무게 차이(48)가 차지하는 몫에 가장 가까운 것은?', 'o': ['약 20%', '약 50%', '거의 100%'], 'a': 2,
             'why': '48² = 2,304이고 전체 제곱합이 약 2,307.9이므로 99.8%가 무게입니다.', 'hint': '48²과 0.8²을 비교해 보세요.'},
            {'q': '"높이 ÷ 길이" 같은 체형 비율로 거리를 재면 무엇이 달라지나?', 'o': ['크기를 빼고 생김새만 본다', '무게만 본다', '거리가 늘 0이 된다'], 'a': 0,
             'why': '비율은 크기가 달라도 같은 생김새면 비슷한 값이 나옵니다.', 'hint': '큰 도미와 작은 도미의 높이 ÷ 길이를 생각해 보세요.'}],
    'q13': [{'q': '무게 평균 391.9g, 표준편차 346.2g일 때 무게 738g의 z 값은?', 'o': ['약 0.5', '약 1.0', '약 2.0'], 'a': 1,
             'why': '(738 − 391.9) ÷ 346.2 = 346.1 ÷ 346.2 ≈ 1.0. 평균보다 한 걸음 무겁습니다.', 'hint': '먼저 빼고, 그다음 나눕니다.'},
            {'q': '표준화가 해결하지 못하는 문제는?', 'o': ['단위가 큰 변수가 거리를 독점하는 문제', '거의 같은 정보를 가진 변수가 여러 개 들어가는 문제'], 'a': 1,
             'why': '길이 세 값처럼 같은 정보가 반복되면 표준화 뒤에도 세 표를 행사합니다. 3장의 PCA가 이 문제를 다룹니다.', 'hint': '길이1·길이2·길이3의 상관은 0.99 이상입니다.'}],
}

JS = r'''
var D=FL.load(),X=D.X,N=D.n,SP=FL.SP,SPC=FL.SPC,SPKO=FL.SPKO;
var MS=FL.meanStd(X),Z=FL.standardize(X,MS);
/* 1-1 */
(function(){var cv=$('#cv11'),mode='sup';var hid=0;for(var i=0;i<N;i++){if(D.orig[i]&&D.sp[i]==='Perch'&&X[i][1]>30){hid=i;break;}}
  /* 자기지도: 길이1로 무게 맞히기 (가린 물고기 하나 빼고 로그-로그 직선) */
  var sx=0,sy=0,sxx=0,sxy=0,m=0;for(i=0;i<N;i++){if(D.seed[i]===D.seed[hid])continue;var a=Math.log(X[i][1]),b=Math.log(X[i][0]);sx+=a;sy+=b;sxx+=a*a;sxy+=a*b;m++;}
  var bb=(m*sxy-sx*sy)/(m*sxx-sx*sx),aa=(sy-bb*sx)/m;function pred(L){return Math.exp(aa+bb*Math.log(L));}
  var reveal=false;
  function draw(){var f=fit(cv),g=f.c;var A=FL.axes(g,f.W,f.H,{xmin:0,xmax:70,ymin:0,ymax:2400,xlab:'길이1 (cm)',ylab:'무게 (g)'});
    for(var i=0;i<N;i++){if(mode==='self'&&D.seed[i]===D.seed[hid])continue;FL.dot(g,A.sx(X[i][1]),A.sy(X[i][0]),2.6,mode==='sup'?SPC[D.sp[i]]:'#8a96a3',mode==='sup'?.75:.45);}
    if(mode==='self'){g.strokeStyle='#1f7a52';g.lineWidth=2;g.beginPath();for(var L=6;L<=66;L+=1){var x=A.sx(L),y=A.sy(Math.min(2400,pred(L)));L===6?g.moveTo(x,y):g.lineTo(x,y);}g.stroke();
      var hx=A.sx(X[hid][1]);g.setLineDash([5,4]);g.strokeStyle='#c9302c';g.beginPath();g.moveTo(hx,A.sy(0));g.lineTo(hx,A.sy(2400));g.stroke();g.setLineDash([]);
      FL.dot(g,hx,A.sy(pred(X[hid][1])),6,'#1f7a52',1);g.fillStyle='#c9302c';g.font='700 15px "IBM Plex Sans KR",sans-serif';g.fillText(reveal?'실제':'?',hx+8,A.sy(reveal?X[hid][0]:pred(X[hid][1]))-10);
      if(reveal)FL.dot(g,hx,A.sy(X[hid][0]),6,'#c9302c',1);}
    stamp(g,f.W,mode==='sup'?'실제 데이터 · 색 = 종 이름':mode==='unsup'?'실제 데이터 · 이름표 덮음':'실제 데이터 · 무게 하나 가림');}
  function info(){var p=pred(X[hid][1]);
    if(mode==='sup'){FL.spLegend($('#lg11'));FL.kpis($('#k11'),[['1,554','이름표가 붙은 물고기','g'],['7','맞힐 종 이름','m'],['정확도','채점 방법','i'],['있음','정답표','a']]);
      $('#in11').innerHTML='<p class="g">색이 곧 정답입니다. 지도학습 모델은 "이 위치면 이 색"이라는 규칙을 배웁니다.</p>';}
    else if(mode==='unsup'){$('#lg11').innerHTML='<span><i style="background:#8a96a3"></i>이름표 없는 물고기</span>';FL.kpis($('#k11'),[['1,554','이름표 없는 물고기','g'],['0','맞힐 이름','m'],['모양 점수','채점 방법','i'],['없음','정답표','a']]);
      $('#in11').innerHTML='<p class="m">색이 없어도 점들은 아무렇게나 흩어져 있지 않습니다. 길이가 길수록 무거운 띠가 보이고, 그 띠는 한 줄이 아니라 여러 줄로 갈라져 있습니다. 그 갈래가 2장에서 찾을 "무리"입니다.</p>';}
    else{$('#lg11').innerHTML='<span><i style="background:#1f7a52"></i>길이로 맞힌 무게 곡선</span><span><i style="background:#c9302c"></i>가린 물고기</span>';
      FL.kpis($('#k11'),[[X[hid][1].toFixed(1)+'cm','가린 물고기의 길이1','g'],[FL.fmt(p)+'g','길이로 맞힌 무게','m'],[reveal?FL.fmt(X[hid][0])+'g':'?','가려 둔 실제 무게','a'],[reveal?FL.pct(Math.abs(p-X[hid][0])/X[hid][0]):'?','빗나간 비율','r']]);
      $('#in11').innerHTML='<p class="a">원본 농어 한 마리의 무게를 가리고, 나머지 물고기로 "길이가 이만하면 무게는 이만큼"이라는 곡선을 만들었습니다. 정답은 사람이 붙인 이름표가 아니라 가려 둔 원래 무게입니다. <button class="bt" id="rv11">가린 무게 보기</button></p>';
      $('#rv11').addEventListener('click',function(){reveal=true;info();draw();});}}
  $$('#p11 [data-m]').forEach(function(bt){bt.addEventListener('click',function(){mode=bt.dataset.m;reveal=false;$$('#p11 [data-m]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});info();draw();});});
  info();Loop.add(cv,function(dt,force){if(dt===0)draw();});
})();
/* 1-2 */
(function(){var cv=$('#cv12');var by={};SP.forEach(function(s){by[s]=[];});for(var i=0;i<N;i++)if(D.orig[i])by[D.sp[i]].push(i);
  function setup(p,def,di){var sel=$('#'+p+'12sp');sel.innerHTML=SP.map(function(s){return '<option value="'+s+'">'+SPKO[s]+' '+s+'</option>';}).join('');sel.value=def;var r=$('#'+p+'12i');
    function sync(){r.max=by[sel.value].length-1;}sync();r.value=di;sel.addEventListener('change',function(){sync();r.value=0;upd();});r.addEventListener('input',upd);}
  setup('a','Bream',0);setup('b','Bream',1);
  function cur(p){return by[$('#'+p+'12sp').value][+$('#'+p+'12i').value];}
  function fish(g,cx,cy,L,Hh,Wd,col,sc){var w=L*sc,h=Hh*sc;g.fillStyle=col;g.globalAlpha=.85;g.beginPath();g.ellipse(cx,cy,w/2,h/2,0,0,6.2832);g.fill();g.beginPath();g.moveTo(cx-w/2+2,cy);g.lineTo(cx-w/2-h*.45,cy-h*.38);g.lineTo(cx-w/2-h*.45,cy+h*.38);g.closePath();g.fill();g.globalAlpha=1;g.fillStyle='#fff';g.beginPath();g.arc(cx+w*.33,cy-h*.12,Math.max(2,h*.07),0,6.2832);g.fill();g.fillStyle='#16212b';g.beginPath();g.arc(cx+w*.33,cy-h*.12,Math.max(1,h*.035),0,6.2832);g.fill();}
  function upd(){var a=cur('a'),b=cur('b');$('#a12v').textContent='#'+a;$('#b12v').textContent='#'+b;
    var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var mx=Math.max(X[a][1],X[b][1]),sc=Math.min((f.W/2-50)/mx,(f.H-60)/Math.max(X[a][4],X[b][4]));
    fish(g,f.W*.27,f.H*.5,X[a][1],X[a][4],X[a][5],SPC[D.sp[a]],sc);fish(g,f.W*.75,f.H*.5,X[b][1],X[b][4],X[b][5],SPC[D.sp[b]],sc);
    g.fillStyle='#16212b';g.font='700 13px "IBM Plex Sans KR",sans-serif';g.textAlign='center';g.fillText('A · '+SPKO[D.sp[a]]+' '+X[a][1]+'cm',f.W*.27,f.H-10);g.fillText('B · '+SPKO[D.sp[b]]+' '+X[b][1]+'cm',f.W*.75,f.H-10);g.textAlign='left';
    stamp(g,f.W,'실제 비율로 그린 그림');
    var tot=0,man=0,rows='<tr><th>측정값</th><th class="n">A</th><th class="n">B</th><th class="n">차이 Δ</th><th class="n">Δ²</th><th>거리에서 차지하는 몫</th></tr>',sq=[];
    for(var j=0;j<6;j++){var dd=X[a][j]-X[b][j];sq.push(dd*dd);tot+=dd*dd;man+=Math.abs(dd);}
    for(j=0;j<6;j++){var sh=tot?sq[j]/tot:0;rows+='<tr><td>'+FL.COLS[j]+' ('+FL.UNITS[j]+')</td><td class="n">'+X[a][j]+'</td><td class="n">'+X[b][j]+'</td><td class="n">'+(X[a][j]-X[b][j]).toFixed(2)+'</td><td class="n">'+sq[j].toFixed(2)+'</td><td><span class="swatch" style="width:'+Math.max(2,Math.round(sh*160))+'px;background:#1f7a52"></span>'+FL.pct(sh)+'</td></tr>';}
    $('#t12').innerHTML=rows;var ra=X[a][4]/X[a][1],rb=X[b][4]/X[b][1];
    FL.kpis($('#k12'),[[Math.sqrt(tot).toFixed(2),'유클리드 거리 (원 단위)','g'],[man.toFixed(2),'맨해튼 거리 (원 단위)','i'],[Math.abs(ra-rb).toFixed(3),'체형 비율(높이÷길이1) 차이','m'],[FL.pct(tot?sq[0]/tot:0),'유클리드 거리 중 무게 몫','a']]);
    $('#in12').innerHTML='<p class="'+(sq[0]/tot>.9?'r':'g')+'">'+(sq[0]/tot>.9?'무게 차이가 거리의 '+FL.pct(sq[0]/tot)+'를 차지합니다. 나머지 다섯 값은 거의 목소리가 없습니다.':'이 쌍은 무게 차이가 작아서 다른 값들도 거리에 들어갑니다. 그래도 원 단위에서는 숫자가 큰 변수가 유리합니다.')+'</p>'
      +'<p class="m">체형 비율은 A '+ra.toFixed(3)+', B '+rb.toFixed(3)+'입니다. 크기가 달라도 생김새가 같으면 이 차이는 작습니다.</p>';}
  Loop.add(cv,function(dt){if(dt===0)upd();});
})();
/* 1-3 */
var NNraw=null,NNstd=null;
function nnAll(M){var out={near:[],nearOther:[]};for(var i=0;i<N;i++){var b=-1,bd=Infinity,o=-1,od=Infinity;for(var j=0;j<N;j++){if(j===i)continue;var d=FL.d2(M[i],M[j]);if(d<bd){bd=d;b=j;}if(D.seed[j]!==D.seed[i]&&d<od){od=d;o=j;}}out.near.push(b);out.nearOther.push(o);}return out;}
function stats(M,nn){var share=[0,0,0,0,0,0],tot=0,ok=0;for(var i=0;i<N;i++){var j=nn.near[i];for(var k=0;k<6;k++){var t=M[i][k]-M[j][k];share[k]+=t*t;tot+=t*t;}if(D.sp[nn.nearOther[i]]===D.sp[i])ok++;}return {share:share.map(function(v){return v/tot;}),agree:ok/N};}
var ST=null;function getST(){if(!ST){NNraw=nnAll(X);NNstd=nnAll(Z);ST={raw:stats(X,NNraw),std:stats(Z,NNstd)};}return ST;}
(function(){var cv=$('#cv13'),sc='raw';
  function draw(){var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=90,R=20,T=18,rowH=(f.H-T-36)/6;var M=sc==='raw'?X:Z;
    var lo=sc==='raw'?0:-3.5,hi=sc==='raw'?2400:4.5;function sx(v){return L+(v-lo)/(hi-lo)*(f.W-L-R);}
    g.font='13px "IBM Plex Sans KR",sans-serif';
    for(var j=0;j<6;j++){var y=T+rowH*j+rowH/2;g.fillStyle='#16212b';g.textAlign='right';g.fillText(FL.COLS[j],L-10,y+4);g.strokeStyle='#e3e8ee';g.beginPath();g.moveTo(L,y);g.lineTo(f.W-R,y);g.stroke();
      for(var i=0;i<N;i+=3){FL.dot(g,sx(M[i][j]),y+((i*7)%9-4),2,j===0?'#c9302c':'#1f7a52',.35);}}
    g.fillStyle='#5b6874';g.textAlign='center';FL.niceTicks(lo,hi,6).forEach(function(t){g.fillText(t,sx(t),f.H-12);});g.textAlign='left';
    stamp(g,f.W,sc==='raw'?'실제 데이터 · 원 단위 눈금':'실제 데이터 · 표준화 눈금');}
  function info(){var s=getST()[sc];$('#vb13').innerHTML=s.share.map(function(v,j){return '<div class="vb"><span>'+FL.COLS[j]+'</span><div class="tr"><div class="fl" style="width:'+(v*100).toFixed(1)+'%;background:'+(j===0?'#c9302c':'#1f7a52')+'"></div></div><span class="v">'+FL.pct(v)+'</span></div>';}).join('');
    FL.kpis($('#k13'),[[FL.pct(s.share[0]),'이웃 거리 중 무게 몫','r'],[FL.pct(s.agree),'가장 가까운 이웃이 같은 종 (채점용)','g'],[sc==='raw'?'0 ~ 2,285':'약 −2 ~ +5','눈금 범위','a'],[sc==='raw'?'g · cm 섞임':'단위 없음','단위','i']]);
    $('#in13').innerHTML=sc==='raw'?'<p class="r">원 단위에서는 무게 줄만 길게 퍼지고, 길이·높이·폭은 왼쪽 끝에 뭉쳐 보입니다. 거리도 그대로 무게가 정합니다.</p>':'<p class="g">표준화하면 여섯 줄이 같은 폭으로 퍼집니다. 무게 몫이 줄고 높이·폭이 거리에 들어오면서, 이웃이 같은 종일 확률이 올라갑니다.</p>';}
  $$('#p13 [data-s]').forEach(function(bt){bt.addEventListener('click',function(){sc=bt.dataset.s;$$('#p13 [data-s]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});info();draw();});});
  Loop.add(cv,function(dt){if(dt===0){draw();}});setTimeout(info,30);
})();
Duel({el:'#d1',run:function(){var s=getST();return {fly:s.std.agree,robo:s.raw.agree};},fmt:function(v){return FL.pct(v);},scale:1,bigGap:.1,
  report:function(r){return '가장 가까운 이웃이 같은 종인 비율은 초파리 쪽(표준화) '+FL.pct(r.fly)+', 주판봇 쪽(원 단위) '+FL.pct(r.robo)+'예요. 같은 원본에서 늘린 물고기는 이웃에서 뺐어요.';},
  verdict:{fly:'눈금을 맞추자 거리가 물고기의 생김새를 보기 시작했다. 초파리 승.',robo:'이번 데이터에서는 원 단위가 더 나았다. 주판봇 승.',draw:'차이가 없다. 이번 판은 나눠 갖는다.'}});
'''


def main():
    USED.update(['fly_arms', 'fly_coffee', 'fly_cry', 'robo_sigh', 'robo_happy', 'robo_meh', 'fly_point', 'robo_coin'])
    hero_html = hero('1장 · 비지도학습 물고기 연구실', '정답표 없이 배운다 — 거리와 표준화',
                     '종 이름표를 덮어도, 숫자만으로 "닮은 물고기"를 찾을 수 있을까?',
                     '앞 시리즈에서는 물고기마다 종 이름이 붙어 있었고, 모델은 그 이름을 맞히도록 배웠습니다(지도학습). 이번에는 이름표를 덮습니다. '
                     '손에 남는 것은 무게·길이·높이·폭 같은 숫자 여섯 개뿐입니다. 이 장에서는 세 가지 배우는 법을 나란히 보고, 정답 없이 배우는 모든 방법이 쓰는 두 도구, <b>거리</b>와 <b>표준화</b>를 직접 만져 봅니다.',
                     [('1,554', '어시장에서 잰 물고기 (원본 158마리 × 증강)', 'g'), ('6', '측정값: 무게·길이 세 가지·높이·폭', 'i'),
                      ('7 → 덮음', '종 이름표 (마지막 대조에만 씀)', 'm'), ('0.99+', '길이 세 값끼리의 상관 (같은 이야기를 반복)', 'a')],
                     [('doc', 'front', '지도학습 때는 물고기마다 종 이름표가 붙어 있었죠. 오늘은 그 이름표를 덮고 시작합니다.'),
                      ('asst', 'shock', '이름표 없이 뭘 배워요? 정답이 없으면 채점도 못 하잖아요.'),
                      ('fly', 'point', '정답이 없으면 더 조심해야지. 숫자가 그럴듯한지부터 의심하자.'),
                      ('robo', 'coin', '숫자 여섯 개면 충분해. 제일 큰 숫자부터 보면 답이 나온다고!')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → 지도학습 시리즈 저장소 <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a>의 증강본 fish_market_x10.csv'),
                 ('원자료', '안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 (2026, 35쪽)'),
                 ('지도학습 비교 수치', 'code/analysis.py로 다시 계산 (scikit-learn 1.9.1, 물고기 단위 5겹 교차검증)'),
                 ('표준화·거리', 'Hastie, Tibshirani, Friedman (2009). The Elements of Statistical Learning, 14장')],
                ['1-1의 길이→무게 곡선(가린 물고기 하나를 빼고 로그 직선으로 맞춤)', '1-2의 물고기 그림(실제 길이·높이 비율, 모양은 설명용)', '대결의 승패 문장(숫자는 실제 계산)'],
                prev=('index.html', '목차'), nxt=('02_grouping.html', '2장 · 묶기 — 군집화'))
    return build(P, title='1장 · 정답표 없이 배운다 — 비지도학습 물고기 연구실',
                 desc='물고기 1,554마리의 종 이름표를 덮고, 비지도학습의 두 도구인 거리와 표준화를 직접 만져 본다. 지도학습과 나란히 비교.',
                 nav=[('#first', '3줄'), ('#s1', '1-1 세 가지'), ('#s2', '1-2 거리'), ('#s3', '1-3 표준화'), ('#duel', '대결'), ('#sum', '정리')],
                 cover_html=cover('cover_01', '1장 · 정답표 없이', '정답표 없이 배운다 — 거리와 표준화'),
                 hero=hero_html, body=b, gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_01')


if __name__ == '__main__':
    print(main())
