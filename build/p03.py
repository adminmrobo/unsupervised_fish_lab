# -*- coding: utf-8 -*-
"""3장 · 접기 — 차원 축소 (PCA: 가장 긴 방향, 네 걸음, 물고기 지도, 복원)"""
from lib import *

P = '03_folding.html'
pc = R['pca']; evr = pc['evr']; eig = pc['eig']; ld = pc['load']; rec = R['pca_recon_mse']; nap = R['nn_agree_pc']; corr = R['corr']


def body():
    b = three([
        ('무엇을', '측정값 여섯 개를 숫자 두 개로 "접어" 종이 한 장 위의 물고기 지도를 그립니다. 주성분 분석(PCA)이라고 부릅니다.'),
        ('왜 중요한가', '사람은 2~3방향까지만 그림으로 봅니다. 접어야 볼 수 있고, 접으면 같은 이야기를 반복하는 변수들이 하나로 정리됩니다.'),
        ('업무에서는', '설문 문항 수십 개를 "만족도 축" 몇 개로 줄이거나, 센서 수백 개를 대시보드의 지도 한 장으로 요약할 때 씁니다.')],
        '코드·수식을 몰라도 됩니다. "접었더니 얼마나 남았나"를 늘 숫자(분산 몇 %)로 확인하는 것이 이 장의 약속입니다.',
        [('PCA', 'Principal Component Analysis, 주성분 분석'), ('PC1, PC2', '첫째·둘째 주성분 (가장 많이 흔들리는 방향, 그다음 방향)'), ('MSE', 'Mean Squared Error, 평균 제곱 오차')])
    b += section('map', '큰 그림 — 묶기에서 접기로',
                 '<div class="mapbar"><span>1장 · 거리·표준화</span><i>→</i><span>2장 · 묶기</span><i>→</i><span class="on">3장 · 접기</span><i>→</i><span>4장 · 맞히기</span><i>→</i><span>실전 연습장</span></div>'
                 + say('sia', 'explain', '2장은 체형 비율 두 개라는 자를 사람이 직접 골랐습니다. 3장은 여섯 측정값 전체에서 "가장 많이 흔들리는 방향"을 AI가 스스로 찾게 합니다.')
                 + '<p>1장 끝에서 남긴 숙제가 있었습니다. 길이 세 값은 서로 상관이 0.99를 넘어 같은 이야기를 세 번 합니다. '
                 '접기는 이렇게 겹친 정보를 하나로 모으고, 남은 차이를 순서대로 줄 세우는 일입니다. 접은 결과(물고기 지도)는 4장의 이웃 찾기와 범위 밖 판단에 그대로 쓰입니다.</p>')

    # 3-1
    names = ['무게', '길이1', '길이2', '길이3', '높이', '폭']
    s = say('doc', 'think', '상황 하나. 고객 설문 문항이 서른 개인데, 그중 열 개가 사실상 "가격이 마음에 드나"를 다르게 물은 것이라면, 서른 개를 다 따로 볼 필요가 있을까요?')
    s += recap('상관계수', '<p>두 값이 함께 오르내리는 정도를 −1~+1로 나타낸 수입니다. +1에 가까우면 한쪽이 크면 다른 쪽도 큽니다. 이 데이터에서 길이1과 길이2의 상관은 %s입니다.</p>' % num(corr[1][2], 3))
    s += duo(why([('문제 상황', '물고기 한 마리는 숫자 여섯 개, 즉 여섯 방향의 공간에 있는 점입니다. 종이에는 두 방향만 그릴 수 있습니다.'),
                  ('앞 방법의 한계', '2장처럼 두 변수를 사람이 골라 그리면, 고르지 않은 넷의 정보는 버려집니다. 무엇을 고를지도 사람마다 다릅니다.'),
                  ('해법', '여섯 변수를 섞어 "가장 많이 흔들리는 새 방향"부터 차례로 만들고, 앞의 두세 방향만 남깁니다(PCA).')],
                 '두꺼운 책을 요약할 때 문장을 몇 개 고르는 대신, 여러 문장에 겹친 뜻을 모아 새 문장 두 줄로 다시 쓰는 것과 같습니다.'),
             pair('일상으로 치면', '그림자 놀이에서 손 모양을 벽에 비추면 3차원 손이 2차원 그림자가 됩니다. 손을 잘 돌려 비추면 그림자만 보고도 무슨 동물인지 알아봅니다.',
                  '모델에서는', 'PCA는 데이터를 비출 "가장 잘 보이는 벽의 방향"을 찾습니다. 그림자가 가장 넓게 퍼지는 방향이 첫째 주성분(PC1), 그다음이 둘째(PC2)입니다.'))
    s += sup('측정값 여섯 개를 모두 모델에 넣었습니다. 변수가 서로 닮아도 모델이 알아서 가중치를 나눠 가졌고, 정답률이 판단 기준이었습니다.',
             '정답이 없으니 "겹친 정보"를 먼저 정리해야 거리가 공정해집니다. 길이 세 값이 거리에서 세 표를 행사하는 문제를 접기로 풉니다.')
    s += talk([('doc', 'board', '여섯 변수끼리 얼마나 닮았는지 표로 볼까요?'),
               ('robo', 'coin', '변수가 여섯이면 정보도 여섯 배지. 하나도 버릴 수 없어!'),
               ('fly', 'point', '아래 표에서 길이1·2·3이 만나는 곳을 봐. 진한 초록이 몇 개야?'),
               ('asst', 'report', '길이끼리는 전부 0.99 이상이에요. 이름만 셋이지, 거의 한 변수예요.')])
    s += panel('p31', '실험 · 여섯 측정값의 상관표', '실제 데이터로 직접 계산',
               canvas('cv31', 330, '여섯 측정값 사이의 상관계수를 색으로 칠한 표') + '<div class="insight" id="in31" aria-live="polite"></div>', real=True)
    s += explain(['상관표는 여섯 변수를 두 개씩 짝지어 함께 오르내리는 정도를 칠한 것입니다.',
                  '길이1·길이2·길이3은 서로 0.99 이상입니다. 무게도 길이와 0.9 이상입니다. 여섯 값의 상당수가 "크기"라는 같은 이야기를 반복합니다.',
                  '반면 높이는 길이와 0.6~0.7 정도라, 크기와는 다른 이야기(생김새)를 조금 더 담고 있습니다.'],
                 '상관은 직선으로 함께 움직이는 정도만 잽니다. 무게처럼 길이의 세제곱에 가깝게 휘며 자라는 관계는 상관이 0.9여도 직선으로는 다 설명되지 않습니다(4장에서 다시 만납니다).')
    s += quiz('q31')
    b += step('s1', '3-1', '여섯 개의 축은 사람이 못 본다 — 겹친 정보', ['방법: 상관표', '일상: 그림자 놀이'], s)

    # 3-2
    s = say('doc', 'think', '구름처럼 퍼진 점들에 막대 하나를 대고 돌린다고 해 봅시다. 막대 위로 떨어진 그림자가 가장 넓게 퍼지는 방향은 어디일까요?')
    s += duo(why([('문제 상황', '"가장 많이 흔들리는 방향"이라는 말은 그럴듯하지만, 어떻게 찾는지가 막연합니다.'),
                  ('앞 방법의 한계', '가로축(무게)이나 세로축(높이) 하나만 보면, 구름이 비스듬히 퍼진 진짜 방향을 놓칩니다.'),
                  ('해법', '방향을 조금씩 돌려 가며 점들을 그 방향에 비춘 그림자(투영)가 얼마나 퍼지는지(분산) 재고, 가장 넓은 방향을 고릅니다.')],
                 '손전등을 돌리며 벽에 비친 그림자가 가장 길어지는 각도를 찾는 일입니다.'),
             mathbox('"방향에 비춘다"는 계산이 뭐예요? 화살표끼리 곱해요?', '벡터의 내적(고등학교 기하) — 그림자 길이 = 좌표와 방향을 자리끼리 곱해 더하기',
                     '그림자 = x × u<sub>1</sub> + y × u<sub>2</sub>',
                     [('(x, y)', '', '물고기의 표준화한 좌표'), ('(u<sub>1</sub>, u<sub>2</sub>)', '유 일, 유 이', '방향을 나타내는 길이 1짜리 화살표'),
                      ('그림자', '투영(projection)', '그 방향 위로 떨어진 위치')],
                     '좌표 (2, 1)을 방향 (0.6, 0.8)에 비추면 2 × 0.6 + 1 × 0.8 = <b>2.0</b>. 같은 점을 방향 (1, 0)에 비추면 <b>2</b>, (0, 1)에 비추면 <b>1</b>입니다. 방향마다 그림자 위치가 다릅니다.',
                     '모든 물고기의 그림자를 구해서 얼마나 퍼졌는지(분산) 재면 되는군요. 가장 넓게 퍼지는 방향이 PC1!'))
    s += sup('결정 경계는 "이름표가 다른 물고기를 가장 잘 가르는 선"이었습니다. 이름표가 방향을 정했습니다.',
             'PCA의 방향은 이름표와 상관없이 "가장 많이 흔들리는 방향"입니다. 그 방향이 종을 잘 가를 수도, 아닐 수도 있습니다. 이 차이를 꼭 기억하세요.')
    s += talk([('doc', 'think', '막대를 몇 도로 돌리면 그림자가 가장 넓게 퍼질까요?'),
               ('robo', 'coin', '무게가 제일 중요하니까 가로(0도)가 정답이지!'),
               ('fly', 'point', '각도 막대를 직접 돌려 봐. "흔들림" 숫자가 언제 제일 커지나.'),
               ('asst', 'report', '0도보다 45도 근처에서 흔들림이 더 커요. 무게와 높이를 섞은 비스듬한 방향이에요.')])
    s += panel('p32', '실험 · 그림자가 가장 넓은 방향 찾기', '실제 데이터 (무게·높이, 표준화)',
               '<div class="ctrl"><div class="group"><span class="glabel">막대 각도</span><input type="range" id="a32" min="0" max="179" value="0" aria-label="방향 각도"><span class="val" id="a32v">0°</span></div>'
               '<div class="group"><button class="bt primary" id="b32">가장 넓은 방향 찾기</button></div></div>'
               + canvas('cv32', 360, '표준화한 무게와 높이 산점도, 돌릴 수 있는 방향 막대와 그림자') +
               '<section class="kpis" id="kp32" aria-label="숫자 요약"></section><div class="insight" id="in32" aria-live="polite"></div>', real=True)
    s += explain(['막대 방향을 정하면, 물고기마다 그 방향 위로 그림자(투영)가 떨어집니다.',
                  '그림자들이 퍼진 정도(분산)가 가장 큰 방향이 첫째 주성분(PC1)입니다. 둘째 주성분(PC2)은 PC1과 직각인 방향 중에서 남은 흔들림이 가장 큰 방향입니다.',
                  '변수가 여섯 개여도 원리는 같습니다. 다만 각도를 돌려 찾는 대신, 다음 단계의 계산으로 한 번에 찾습니다.'],
                 '"많이 흔들리는 방향 = 중요한 방향"이라는 가정입니다. 측정 오차가 크게 흔들리면 오차가 PC1이 될 수도 있습니다. 그래서 표준화와 변수 선택이 먼저입니다.')
    s += quiz('q32')
    b += step('s2', '3-2', '가장 길게 뻗은 방향 — 첫째 주성분', ['방법: 투영과 분산', '일상: 손전등과 그림자'], s)

    # 3-3
    total = sum(eig)
    s = say('doc', 'think', '각도를 하나씩 돌려 보는 건 두 변수일 때나 가능합니다. 여섯 변수에서는 어떻게 한 번에 찾을까요?')
    s += duo(why([('문제 상황', '여섯 방향 공간에서는 돌려 볼 각도가 너무 많습니다.'),
                  ('앞 방법의 한계', '눈으로 돌려 찾기는 두 변수까지만 됩니다.'),
                  ('해법', '변수끼리 함께 흔들리는 정도를 표(공분산 표)로 만들고, 그 표를 분해하면 방향(고유벡터)과 흔들림 크기(고유값)가 한꺼번에 나옵니다.')],
                 '시험 성적표를 과목 사이의 관계표로 바꾸면, "전체적으로 공부를 잘함", "이과·문과 쪽" 같은 큰 흐름이 순서대로 보이는 것과 같습니다.'),
             mathbox('고유값, 고유벡터… 이름부터 어려워요!', '비율(초등 6학년) — 전체 흔들림 중 그 방향이 차지하는 몫',
                     '설명된 분산 = 그 방향의 고유값 ÷ 고유값 전체 합',
                     [('고유벡터', '', '방향. 여섯 변수를 얼마씩 섞었는지 적은 화살표'), ('고유값', '', '그 방향으로 흔들리는 크기(분산)'),
                      ('설명된 분산', '', '전체 흔들림 중 그 방향이 차지하는 비율')],
                     '고유값은 %s, %s, %s, %s, %s, %s이고 합은 %s입니다. PC1의 몫 = %s ÷ %s ≈ <b>%s</b>, PC1+PC2 = <b>%s</b>.' % (
                         num(eig[0], 3), num(eig[1], 3), num(eig[2], 3), num(eig[3], 3), num(eig[4], 4), num(eig[5], 4), num(total, 3),
                         num(eig[0], 3), num(total, 3), pct(evr[0]), pct(evr[0] + evr[1])),
                     '고유값은 "흔들림 크기", 고유벡터는 "방향". 이름만 어렵지 몫을 나누는 계산이네요.'))
    s += note('원자료 슬라이드는 첫 방향의 몫을 87.8%로 적었습니다. 같은 1,554마리로 다시 계산하면 87.6%가 나와, 이 페이지에서는 <b>87.6%</b>로 바꿉니다. PC1+PC2 약 96%는 같습니다.', warn=True)
    s += sup('표준화는 했지만, 변수를 섞어 새 변수를 만들지는 않았습니다. 변수 여섯 개가 그대로 모델에 들어갔습니다.',
             'PCA는 여섯 변수를 섞어 새 변수(주성분)를 만듭니다. 새 변수는 서로 겹치지 않고(상관 0), 흔들림이 큰 순서로 줄을 섭니다.')
    s += talk([('doc', 'board', '네 걸음을 차례로 눌러 보세요. 표 하나가 방향 여섯 개로 바뀝니다.'),
               ('robo', 'coin', '여섯 방향이 나오면 여섯 개 다 중요하겠지!'),
               ('fly', 'point', '④까지 누르고 막대 길이를 봐. 다섯째, 여섯째 방향에 뭐가 남았어?'),
               ('asst', 'report', '다섯째·여섯째는 합쳐서 0.04%예요. 길이 세 값의 작은 차이가 남은 거라 거의 비어 있어요.')])
    s += panel('p33', '실험 · PCA 네 걸음', '실제 데이터로 직접 계산',
               '<div class="ctrl"><div class="group"><button class="bt" data-g="0" aria-pressed="true">① 단위 맞추기</button><button class="bt" data-g="1" aria-pressed="false">② 흔들림 표</button>'
               '<button class="bt" data-g="2" aria-pressed="false">③ 방향 찾기</button><button class="bt" data-g="3" aria-pressed="false">④ 새 좌표로 쓰기</button></div></div>'
               '<div id="o33"></div><div class="insight" id="in33" aria-live="polite"></div>', real=True)
    s += explain(['① 표준화로 단위를 지웁니다. 이 걸음을 건너뛰면 무게가 PC1을 혼자 차지합니다.',
                  '② 변수 쌍마다 함께 흔들리는 정도를 표(공분산 표)로 만듭니다. 표준화했으므로 상관표와 같습니다.',
                  '③ 표를 분해해 방향 여섯 개와 그 흔들림 크기를 구합니다. ④ 물고기마다 앞 두 방향의 그림자 좌표 두 개로 다시 씁니다.'],
                 '주성분은 변수를 섞은 것이라 이름이 없습니다. "PC1 = 크기"처럼 이름을 붙이는 일은 섞은 비율(고유벡터)을 보고 사람이 합니다.')
    s += aicheck('"PC1 하나면 87.6%를 맞힌다!"',
                 '<p>주판봇이 외칩니다. "PC1이 흔들림의 87.6%%를 설명하니까, PC1 하나만 있으면 물고기 종의 87.6%%를 맞힐 수 있어!"</p>'
                 '<p><b>확인 질문</b> "설명된 분산 87.6%%"와 "종을 87.6%% 맞힌다"는 같은 말일까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>다른 말입니다. 설명된 분산은 "흔들림을 얼마나 남겼나"이고, 종을 맞히는 것과는 상관이 없습니다. '
                 'PC1 하나만으로 지도를 만들면 가장 가까운 이웃이 같은 종인 비율이 %s밖에 안 됩니다. PC1은 주로 "크기"라서, 크기가 비슷한 다른 종을 이웃으로 붙여 버립니다.</p></details>' % pct(nap['pc1']))
    s += codefold([('pca = PCA().fit(Z)', '표준화한 여섯 열로 주성분 여섯 개를 구합니다'),
                   ('pca.explained_variance_ratio_', '방향마다 설명된 분산의 몫 (0.876, 0.085, …)'),
                   ('pca.components_', '방향마다 여섯 변수를 섞은 비율 (고유벡터)')])
    s += quiz('q33')
    b += step('s3', '3-3', 'PCA는 네 걸음 — 표 하나를 방향 여섯 개로', ['방법: 주성분 분석(PCA)', '일상: 성적표의 큰 흐름'], s)

    # 3-4
    sm = R['pca_species_mean']
    s = say('doc', 'think', '여섯 숫자를 두 숫자로 접었습니다. 이제 물고기 1,554마리를 종이 한 장 위의 지도로 그려 볼까요?')
    s += duo(why([('문제 상황', '주성분은 이름 없는 방향입니다. 지도를 그려도 가로·세로가 무슨 뜻인지 모르면 읽을 수 없습니다.'),
                  ('앞 방법의 한계', '섞은 비율 표만 보면 숫자가 여섯 개씩이라 한눈에 뜻이 안 들어옵니다.'),
                  ('해법', '섞은 비율에서 큰 값을 찾아 축에 이름을 붙이고, 지도 위 물고기 위치로 그 이름이 맞는지 확인합니다.')],
                 '처음 가 본 도시 지도에서 "위쪽이 북쪽"이라는 것만 알아도 길을 찾을 수 있습니다. 축 이름이 그 역할을 합니다.'),
             mathbox('PC1 섞은 비율이 전부 0.4쯤이면 무슨 뜻이에요?', '가중 평균 — 여러 값을 비슷한 비율로 섞으면 "전체 크기"가 된다',
                     'PC1 ≈ %s×무게 + %s×길이1 + %s×길이2 + %s×길이3 + %s×높이 + %s×폭' % tuple(num(v, 2) for v in ld[0]),
                     [('PC1', '첫째 주성분', '여섯 값을 거의 같은 비율로 더함 → 전체 크기'),
                      ('PC2', '둘째 주성분', '높이 +%s, 길이1 %s → 길이에 비해 높이가 큰가 (체형)' % (num(ld[1][4], 2), num(ld[1][1], 2)))],
                     '표준화 값이 모두 +1인 큰 물고기는 PC1 ≈ 0.42×6 ≈ <b>2.5</b>, 모두 −1인 작은 물고기는 <b>−2.5</b>. 실제로 빙어 평균은 PC1 %s, 강꼬치고기는 %s입니다.' % (num(sm['Smelt'][0], 2), num(sm['Pike'][0], 2)),
                     'PC1은 "얼마나 큰가", PC2는 "얼마나 납작한가"였군요. 이름 없는 방향에 이름이 생겼어요.'))
    s += sup('물고기를 평면에 그릴 때는 이름표 색으로 칠했고, 그 위에 모델이 그은 경계선을 봤습니다.',
             '이름표 없이 그린 지도인데도 같은 종이 한곳에 모입니다. 이름표는 지도를 다 그린 뒤 "잘 그렸나" 대조할 때만 켭니다.')
    s += talk([('doc', 'think', '이름표를 켜기 전에, 지도만 보고 무리가 몇 개로 보이나요?'),
               ('robo', 'coin', '그냥 한 덩어리 띠잖아. 접으니까 다 뭉개졌네!'),
               ('fly', 'point', '"2장 주머니 색"을 켜 봐. 그다음 "이름표"를 켜서 위아래로 갈라진 걸 봐.'),
               ('asst', 'report', '위쪽엔 납작한 도미·파르키, 아래쪽엔 길쭉한 강꼬치고기·빙어가 있어요. 2장 주머니와 같은 자리예요.')])
    s += panel('p34', '실험 · 이름표 없이 그린 물고기 지도', '실제 데이터 · PCA는 이 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">색</span><button class="bt" data-c="none" aria-pressed="true">색 없음</button>'
               '<button class="bt" data-c="cl" aria-pressed="false">2장 주머니 (체형 k=3)</button><button class="bt" data-c="sp" aria-pressed="false">덮어 둔 종 이름표</button></div></div>'
               + canvas('cv34', 380, 'PC1(가로, 크기)과 PC2(세로, 체형)로 그린 물고기 지도') +
               '<div class="legend" id="lg34"></div><section class="kpis" id="kp34" aria-label="숫자 요약"></section><div class="insight" id="in34" aria-live="polite"></div>', real=True)
    s += explain(['PC1(가로)은 여섯 값을 거의 같은 비율로 섞은 "크기" 축입니다. 왼쪽은 작은 빙어, 오른쪽은 큰 강꼬치고기입니다.',
                  'PC2(세로)는 높이가 크게 +, 길이가 −인 "체형" 축입니다. 위쪽은 납작하고 넓은 도미, 아래쪽은 길고 날렵한 강꼬치고기입니다.',
                  '종 이름표를 한 번도 쓰지 않았는데, 생물학적으로 뜻 있는 두 축(크기·체형)이 스스로 나왔습니다.'],
                 '농어·로치·흰송어는 지도 가운데에서 서로 겹칩니다. 두 축으로 접으면서 이 셋을 가르는 미세한 차이가 일부 사라졌습니다. 접기는 요약이지 원본이 아닙니다.')
    s += codefold([('S = PCA(2).fit_transform(Z)', '물고기마다 PC1, PC2 두 숫자'),
                   ('plt.scatter(S[:, 0], S[:, 1])', '두 숫자로 지도를 그립니다')])
    s += quiz('q34')
    b += step('s4', '3-4', '물고기를 접어 봤다 — 크기 축과 체형 축', ['결과: 물고기 지도', '일상: 지도의 동서남북'], s)

    # 3-5
    s = say('doc', 'think', '두 숫자로 접은 지도에서 원래 여섯 숫자를 다시 펼 수 있을까요? 펼쳤을 때 무엇이 남고 무엇이 사라질까요?')
    s += duo(why([('문제 상황', '"잘 접혔다"는 말만으로는 무엇을 잃었는지 모릅니다.'),
                  ('앞 방법의 한계', '설명된 분산(%)은 전체 몫만 알려 주고, 어느 변수를 얼마나 틀리게 되살리는지는 말해 주지 않습니다.'),
                  ('해법', '접은 좌표에 방향을 곱해 다시 펴고(복원), 원래 값과의 차이(복원 오차)를 잽니다.')],
                 '요약본만 보고 원래 책 내용을 다시 써 본 뒤, 원본과 비교해 무엇이 빠졌는지 확인하는 일입니다.'),
             mathbox('접은 걸 어떻게 다시 펴요? 거꾸로 계산해요?', '벡터의 덧셈(고등학교) — 방향 화살표를 그림자 길이만큼 늘려 더하기',
                     '복원 = PC1 좌표 × PC1 방향 + PC2 좌표 × PC2 방향',
                     [('PC1 좌표', '', '접은 지도의 가로 위치'), ('PC1 방향', '', '여섯 변수 섞은 비율 (고유벡터)'), ('복원 오차', 'MSE', '원래 값과 펼친 값 차이의 제곱 평균')],
                     '축 하나만 쓰면 복원 오차가 %s, 둘이면 %s, 셋이면 %s, 넷이면 %s입니다(표준화 눈금). 넷째에서 거의 0이 되는 것은 남은 두 방향이 비어 있었기 때문입니다.' % (
                         num(rec['1'], 4), num(rec['2'], 4), num(rec['3'], 4), num(rec['4'], 4)),
                     '숫자 두 개만으로도 여섯 숫자를 꽤 되살리네요. 그래도 0은 아니니까, 뭔가 버린 거예요.'))
    s += sup('정답(종)을 얼마나 맞혔는지로 모델을 채점했습니다.',
             '정답이 없으니 "나 자신을 얼마나 되살리나"로 채점합니다. 이 생각이 4장의 오토인코더로 이어집니다.')
    s += talk([('doc', 'board', '축을 두 개만 남기면 어느 변수가 가장 많이 틀릴까요?'),
               ('robo', 'coin', '숫자가 제일 큰 무게는 PC1이 다 잡았으니 무게는 완벽하지!'),
               ('fly', 'point', '물고기를 바꿔 가며 "무게" 줄의 차이를 봐. 큰 물고기에서 특히.'),
               ('asst', 'report', '무게가 가장 많이 틀려요. 큰 물고기는 수백 g씩 빗나가요. 무게는 길이에 곡선으로 따라가서 그래요.')])
    s += panel('p35', '실험 · 접었다가 다시 펴기', '실제 데이터 · 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">남길 축 수</span><input type="range" id="n35" min="1" max="6" value="2" aria-label="남길 축 수"><span class="val" id="n35v">2</span></div>'
               '<div class="group"><span class="glabel">물고기</span><input type="range" id="f35" min="0" max="157" value="20" aria-label="물고기 고르기"><span class="val" id="f35v"></span></div></div>'
               + canvas('cv35', 260, '고른 물고기의 원래 값(막대)과 다시 편 값(점)') +
               '<div class="tw"><table class="tb mini-table" id="t35"></table></div><section class="kpis" id="kp35" aria-label="숫자 요약"></section><div class="insight" id="in35" aria-live="polite"></div>', real=True)
    s += explain(['접은 좌표(두 숫자)에 방향(섞은 비율)을 곱해 더하면 여섯 숫자가 다시 나옵니다. 이것이 복원입니다.',
                  '복원 오차는 축이 늘수록 줄어듭니다. 두 축이면 표준화 눈금에서 평균 %s, 여섯 축이면 0입니다.' % num(rec['2'], 4),
                  '두 축으로 펴면 무게가 가장 많이 틀립니다. 크기와 체형만으로는 "길이가 길면 무게는 세제곱으로 늘어난다"는 휜 관계를 되살리지 못합니다.'],
                 'PCA는 곧은 방향(직선)으로만 접습니다. 무게처럼 휘어진 관계는 곧은 접기로는 놓칩니다. 4장에서 곡선으로도 접을 수 있는 오토인코더와 겨룹니다.')
    s += bridge('gen', '생성 AI로 치면', '얼굴 사진 한 장(가로·세로 32점, 색 3가지)은 숫자 3,072개입니다. 얼굴 수백 장을 같은 방법으로 접으면 "얼굴의 밝기", "눈썹 기울기" 같은 방향(고유 얼굴)이 나오고, 접은 좌표를 조금씩 바꾸면 얼굴이 부드럽게 변합니다. 이미지 생성 모델의 "잠재 공간"이 이 생각의 먼 후손입니다.',
                    '실제 이미지 생성 모델은 곧은 접기(PCA)가 아니라 신경망으로 휘어진 공간을 배웁니다. 지도 밖으로 나가면 세상에 없는 얼굴이 그려집니다.')
    s += codefold([('Z_back = pca.inverse_transform(S)', '접은 두 숫자를 여섯 숫자로 다시 폅니다'),
                   ('((Z - Z_back) ** 2).mean()', '복원 오차(평균 제곱 오차)')])
    s += quiz('q35')
    b += step('s5', '3-5', '접은 것을 다시 펴면 — 복원과 잃어버린 것', ['방법: 복원 오차', '일상: 요약본으로 원본 다시 쓰기'], s)

    b += duel('d3', '지도는 몇 축으로 그릴까', '두 축 지도 (PC1·PC2)', '여섯 축 전부',
              '"두 축이면 흔들림의 96%야. 나머지는 군더더기지."', '"버리긴 왜 버려! 여섯 축 전부 써야 정확하지."',
              '가장 가까운 이웃이 같은 종인 비율 (이름표는 채점에만 씀)')

    b += section('sum', '정리 — 접기의 네 가지 약속',
                 '<div class="steps four"><div><span class="n">1</span><h4>표준화 먼저</h4><p>안 하면 무게가 PC1을 독점합니다.</p></div>'
                 '<div><span class="n">2</span><h4>몫을 숫자로</h4><p>"잘 접혔다" 대신 "두 축이 96.1%를 남겼다".</p></div>'
                 '<div><span class="n">3</span><h4>축에 이름 붙이기</h4><p>섞은 비율을 보고 사람이 붙입니다. PC1 = 크기, PC2 = 체형.</p></div>'
                 '<div><span class="n">4</span><h4>잃은 것 확인</h4><p>복원 오차와 이웃 일치율로 무엇을 버렸는지 봅니다.</p></div></div>'
                 + bridge('field', '현장에 옮기면', '설비 센서 50개를 PCA 두 축으로 요약해 "정상 구름"을 대시보드에 그려 두면, 그 구름에서 벗어나는 점이 이상 신호가 됩니다. 4장의 "배운 범위 밖" 판단이 이것입니다.',
                          '정상 구름은 정상일 때의 데이터로 만들어야 합니다. 고장 데이터가 섞이면 고장이 "정상 방향"이 됩니다.'))
    b += outro([('doc', 'front', '오늘 세 줄 정리. ① PCA는 가장 많이 흔들리는 방향부터 줄 세운다. ② 물고기는 두 축(크기·체형)으로 96.1%가 남았다. ③ 접기는 요약이라, 잃은 것을 숫자로 확인한다.'),
                ('robo', 'happy', '봤지? 여섯 축 전부가 이웃을 더 잘 찾았잖아. 드디어 본전 찾았다!'),
                ('fly', 'cry', '…두 축 지도는 보기 좋은 요약이었을 뿐이었네. 인정. 그래도 사람 눈엔 두 축이 필요해.'),
                ('asst', 'spark', '다음 장에서는 곧은 접기 대신 곡선으로 접는 오토인코더와, 가린 값을 맞히는 자기지도학습을 볼게요.')],
               '연구실 식구 네 명이 큰 종이 지도 위에 물고기 점을 찍는 장면')
    return b


GLOSS = {
    '차원 축소': ['차원 축소 (dimensionality reduction)', '변수(방향) 수를 줄여 데이터를 요약하는 일. 이 장의 "접기".'],
    '주성분 분석': ['주성분 분석 (PCA)', '여섯 변수를 섞어 가장 많이 흔들리는 방향부터 새 축을 만드는 방법.'],
    '주성분': ['주성분 (principal component)', 'PCA가 만든 새 방향. PC1은 가장 많이 흔들리는 방향, PC2는 그다음.'],
    '상관': ['상관계수 (correlation)', '두 값이 직선으로 함께 오르내리는 정도. −1~+1.'],
    '투영': ['투영 (projection)', '점을 어떤 방향 위로 비춘 그림자 위치. 좌표와 방향을 자리끼리 곱해 더한 값.'],
    '분산': ['분산 (variance)', '값들이 평균에서 퍼진 정도. 표준편차의 제곱.'],
    '공분산': ['공분산 (covariance)', '두 변수가 함께 흔들리는 정도. 표준화하면 상관계수와 같습니다.'],
    '고유값': ['고유값 (eigenvalue)', '주성분 방향으로 흔들리는 크기(분산). 클수록 그 방향이 정보를 많이 담음.'],
    '고유벡터': ['고유벡터 (eigenvector)', '주성분의 방향. 여섯 변수를 얼마씩 섞었는지 적은 화살표.'],
    '설명된 분산': ['설명된 분산 (explained variance ratio)', '전체 흔들림 중 그 방향이 차지하는 몫. PC1은 87.6%.'],
    '복원': ['복원 (reconstruction)', '접은 좌표를 다시 원래 변수 개수로 펴는 일.'],
    '잠재 공간': ['잠재 공간 (latent space)', '데이터를 접어 얻은 낮은 차원의 좌표 공간. 여기서의 거리가 원래의 닮음을 대신합니다.'],
}

QUIZ = {
    'q31': [{'q': '길이1·길이2·길이3의 상관이 모두 0.99 이상이라는 뜻은?', 'o': ['세 값이 거의 같은 정보를 담는다', '세 값이 서로 반대로 움직인다', '세 값이 서로 관계없다'], 'a': 0,
             'why': '함께 오르내리는 정도가 거의 +1이라 사실상 한 변수입니다.', 'hint': '+1에 가까울수록 같이 움직입니다.'},
            {'q': '여섯 변수를 그대로 거리 계산에 넣으면 생기는 일은?', 'o': ['길이 정보가 세 표를 행사한다', '무게가 사라진다'], 'a': 0,
             'why': '같은 정보를 가진 변수 셋이 거리를 세 번 늘립니다.', 'hint': '1장 1-3의 표준화 한계를 떠올려 보세요.'}],
    'q32': [{'q': '좌표 (1, 3)을 방향 (0.6, 0.8)에 비춘 그림자 위치는?', 'o': ['1.8', '3.0', '4.0'], 'a': 1,
             'why': '1 × 0.6 + 3 × 0.8 = 0.6 + 2.4 = 3.0.', 'hint': '자리끼리 곱해서 더합니다.'},
            {'q': 'PC1은 어떤 방향인가?', 'o': ['종을 가장 잘 가르는 방향', '그림자(투영)가 가장 넓게 퍼지는 방향'], 'a': 1,
             'why': 'PCA는 이름표를 보지 않고 흔들림(분산)이 가장 큰 방향을 찾습니다.', 'hint': '이름표는 덮어 두었습니다.'}],
    'q33': [{'q': '고유값이 5.257, 0.511, 0.124, 0.110, 0.002, 0.000일 때(합 6.004) PC1+PC2의 몫은?', 'o': ['약 87.6%', '약 96.1%', '약 100%'], 'a': 1,
             'why': '(5.257 + 0.511) ÷ 6.004 ≈ 0.961.', 'hint': '두 고유값을 더해 합으로 나눕니다.'},
            {'q': 'PCA 네 걸음 중 건너뛰면 "무게가 PC1을 독점"하게 되는 걸음은?', 'o': ['① 단위 맞추기(표준화)', '④ 새 좌표로 쓰기'], 'a': 0,
             'why': '표준화를 안 하면 숫자가 큰 무게가 흔들림을 거의 다 차지합니다.', 'hint': '1장의 교훈과 같습니다.'}],
    'q34': [{'q': 'PC1의 섞은 비율이 여섯 변수 모두 약 0.4일 때 PC1의 뜻은?', 'o': ['전체 크기', '납작한 정도', '측정 오차'], 'a': 0,
             'why': '모든 값을 비슷하게 더하면 "전체적으로 큰가"가 됩니다.', 'hint': '모두 같은 부호, 비슷한 크기.'},
            {'q': '물고기 지도에서 종 이름표는 언제 썼나?', 'o': ['방향을 찾을 때', '다 그린 뒤 대조할 때만'], 'a': 1,
             'why': 'PCA는 이름표 없이 계산했고, 이름표는 지도가 잘 그려졌는지 확인할 때만 켰습니다.', 'hint': '비지도학습의 약속.'}],
    'q35': [{'q': '두 축으로 접었다 펼 때 가장 많이 틀리는 변수는?', 'o': ['길이2', '무게', '폭'], 'a': 1,
             'why': '무게는 길이에 곡선(대략 세제곱)으로 따라가서 곧은 방향 두 개로는 다 되살리지 못합니다.', 'hint': '휘어진 관계를 가진 변수.'},
            {'q': '축을 여섯 개 모두 남기면 복원 오차는?', 'o': ['0', '0.039', '0.124'], 'a': 0,
             'why': '방향 여섯 개를 다 쓰면 아무것도 버리지 않으니 원래대로 돌아옵니다.', 'hint': '버린 방향이 없으면?'}],
}

JS = r'''
var D=FL.load(),X=D.X,N=D.n,SP=FL.SP,SPC=FL.SPC,SPKO=FL.SPKO,CLC=FL.CLC;
var MS=FL.meanStd(X),Z=FL.standardize(X,MS),PC=FL.pca(Z),S=Z.map(function(z){return FL.project(z,PC.vecs,6);});
var NAMES=['무게','길이1','길이2','길이3','높이','폭'];
/* 3-1 상관표 */
(function(){var cv=$('#cv31');var C=FL.cov(Z).map(function(r){return r.map(function(v){return v*(N-1)/N;});});
  function draw(){var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=70,T=34,sz=Math.min((f.W-L-20)/6,(f.H-T-10)/6);
    g.font='13px "IBM Plex Sans KR",sans-serif';for(var a=0;a<6;a++){g.fillStyle='#16212b';g.textAlign='right';g.fillText(NAMES[a],L-8,T+sz*a+sz/2+4);g.textAlign='center';g.fillText(NAMES[a],L+sz*a+sz/2,T-10);
      for(var b=0;b<6;b++){var v=C[a][b];var t=Math.max(0,Math.min(1,(v-.5)/.5));g.fillStyle='rgb('+Math.round(255-t*(255-19))+','+Math.round(255-t*(255-115))+','+Math.round(255-t*(255-58))+')';g.fillRect(L+sz*b+1,T+sz*a+1,sz-2,sz-2);
        g.fillStyle=t>.55?'#fff':'#16212b';g.fillText(v.toFixed(3),L+sz*b+sz/2,T+sz*a+sz/2+4);}}
    g.textAlign='left';stamp(g,f.W,'실제 데이터 · 진할수록 함께 움직임');}
  $('#in31').innerHTML='<p class="g">길이1·길이2·길이3이 만나는 아홉 자리가 모두 0.99를 넘습니다. 무게도 길이들과 0.9 이상이고, 높이만 0.6~0.7로 조금 다른 이야기를 합니다.</p>';
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 3-2 그림자 */
(function(){var cv=$('#cv32'),ang=0;var P2=Z.map(function(z){return [z[0],z[4]];});
  var c2=FL.cov(P2),e2=FL.eig(c2),best=Math.round(Math.atan2(e2.vecs[0][1],e2.vecs[0][0])*180/Math.PI);if(best<0)best+=180;
  function varAt(deg){var r=deg*Math.PI/180,u=[Math.cos(r),Math.sin(r)];return c2[0][0]*u[0]*u[0]+2*c2[0][1]*u[0]*u[1]+c2[1][1]*u[1]*u[1];}
  function draw(){var f=fit(cv),g=f.c,A=FL.axes(g,f.W,f.H,{xmin:-2.5,xmax:5.5,ymin:-2.5,ymax:3.5,xlab:'무게 (표준화)',ylab:'높이 (표준화)'});
    var r=ang*Math.PI/180,u=[Math.cos(r),Math.sin(r)];var ox=A.sx(0),oy=A.sy(0);
    for(var i=0;i<N;i+=2){var p=P2[i];FL.dot(g,A.sx(p[0]),A.sy(p[1]),2.2,'#8a96a3',.35);var t=p[0]*u[0]+p[1]*u[1];FL.dot(g,A.sx(t*u[0]),A.sy(t*u[1]),2.2,'#1f7a52',.5);}
    g.strokeStyle='#c9302c';g.lineWidth=2.5;g.beginPath();g.moveTo(A.sx(-6*u[0]),A.sy(-6*u[1]));g.lineTo(A.sx(6*u[0]),A.sy(6*u[1]));g.stroke();
    stamp(g,f.W,'실제 데이터 · 초록 = 막대 위 그림자');
    var v=varAt(ang),vm=varAt(best);FL.kpis($('#kp32'),[[ang+'°','막대 각도','i'],[v.toFixed(3),'이 방향 그림자의 흔들림(분산)','g'],[vm.toFixed(3),'가장 넓은 방향의 흔들림','a'],[best+'°','가장 넓은 방향(이 두 변수의 PC1)','m']]);
    $('#in32').innerHTML='<p class="'+(Math.abs(ang-best)<4?'g':'a')+'">'+(Math.abs(ang-best)<4?'찾았습니다. 그림자가 가장 넓게 퍼지는 방향입니다. 무게와 높이를 거의 같은 비율로 섞은 비스듬한 방향이 첫째 주성분입니다.':'가로(0°, 무게만)의 흔들림은 '+varAt(0).toFixed(3)+'입니다. 막대를 돌려 이보다 큰 방향을 찾아보세요.')+'</p>';}
  $('#a32').addEventListener('input',function(){ang=+this.value;$('#a32v').textContent=ang+'°';draw();});
  $('#b32').addEventListener('click',function(){var s=ang,e=best;if(REDUCED){ang=e;$('#a32').value=e;$('#a32v').textContent=e+'°';draw();return;}var t0=null;function an(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/700);ang=Math.round(s+(e-s)*k);$('#a32').value=ang;$('#a32v').textContent=ang+'°';draw();if(k<1)requestAnimationFrame(an);}requestAnimationFrame(an);});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 3-3 네 걸음 */
(function(){var g0=0;var C=FL.cov(Z);
  function tbl(M,fmt){return '<div class="tw"><table class="tb mini-table"><tr><th></th>'+NAMES.map(function(n){return '<th class="n">'+n+'</th>';}).join('')+'</tr>'+M.map(function(r,i){return '<tr><td>'+(typeof i==='number'&&M.length===6&&r.length===6?NAMES[i]:'')+'</td>'+r.map(function(v){return '<td class="n">'+fmt(v)+'</td>';}).join('')+'</tr>';}).join('')+'</table></div>';}
  function show(){var o=$('#o33'),ins=$('#in33');
    if(g0===0){o.innerHTML='<div class="tw"><table class="tb mini-table"><tr><th>측정값</th><th class="n">평균</th><th class="n">표준편차</th><th class="n">표준화 뒤 평균</th><th class="n">표준화 뒤 표준편차</th></tr>'+NAMES.map(function(n,j){var m=0,s=0;for(var i=0;i<N;i++)m+=Z[i][j];m/=N;for(i=0;i<N;i++)s+=(Z[i][j]-m)*(Z[i][j]-m);return '<tr><td>'+n+'</td><td class="n">'+MS.m[j].toFixed(2)+'</td><td class="n">'+MS.s[j].toFixed(2)+'</td><td class="n">'+Math.abs(m).toFixed(3)+'</td><td class="n">'+Math.sqrt(s/N).toFixed(3)+'</td></tr>';}).join('')+'</table></div>';
      ins.innerHTML='<p class="g">여섯 변수 모두 평균 0, 표준편차 1이 됐습니다. 이제 어떤 변수도 흔들림을 독점하지 못합니다.</p>';}
    else if(g0===1){o.innerHTML=tbl(C,function(v){return v.toFixed(3);});ins.innerHTML='<p class="m">변수 쌍마다 함께 흔들리는 정도입니다. 표준화했으므로 대각선은 1(자기 자신), 나머지는 3-1의 상관표와 같습니다.</p>';}
    else if(g0===2){o.innerHTML='<div class="vbars">'+PC.evr.map(function(v,i){return '<div class="vb"><span>PC'+(i+1)+'</span><div class="tr"><div class="fl" style="width:'+(v*100).toFixed(1)+'%"></div></div><span class="v">'+FL.pct(v,2)+'</span></div>';}).join('')+'</div>'+
        '<div class="tw"><table class="tb mini-table"><tr><th>방향</th><th class="n">고유값</th>'+NAMES.map(function(n){return '<th class="n">'+n+'</th>';}).join('')+'</tr>'+PC.vecs.slice(0,3).map(function(v,i){return '<tr><td>PC'+(i+1)+'</td><td class="n">'+PC.vals[i].toFixed(3)+'</td>'+v.map(function(x){return '<td class="n">'+x.toFixed(3)+'</td>';}).join('')+'</tr>';}).join('')+'</table></div>';
      ins.innerHTML='<p class="g">방향 여섯 개가 흔들림이 큰 순서로 나왔습니다. PC1 '+FL.pct(PC.evr[0])+', PC2 '+FL.pct(PC.evr[1])+', 둘을 합치면 '+FL.pct(PC.evr[0]+PC.evr[1])+'입니다. 아래 표는 앞 세 방향이 여섯 변수를 섞은 비율(고유벡터)입니다.</p>';}
    else{var ex=[];for(var i=0;i<N&&ex.length<5;i++)if(D.orig[i]&&(ex.length===0||D.sp[i]!==D.sp[ex[ex.length-1]]))ex.push(i);
      o.innerHTML='<div class="tw"><table class="tb mini-table"><tr><th>물고기</th>'+NAMES.map(function(n){return '<th class="n">'+n+'</th>';}).join('')+'<th class="n">→ PC1</th><th class="n">PC2</th></tr>'+ex.map(function(i){return '<tr><td>'+SPKO[D.sp[i]]+'</td>'+X[i].map(function(v){return '<td class="n">'+v+'</td>';}).join('')+'<td class="n"><b>'+S[i][0].toFixed(2)+'</b></td><td class="n"><b>'+S[i][1].toFixed(2)+'</b></td></tr>';}).join('')+'</table></div>';
      ins.innerHTML='<p class="g">물고기마다 숫자 여섯 개가 두 개(PC1, PC2)로 바뀌었습니다. 이 두 숫자가 다음 단계의 지도 좌표입니다.</p>';}}
  $$('#p33 [data-g]').forEach(function(bt){bt.addEventListener('click',function(){g0=+bt.dataset.g;$$('#p33 [data-g]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});show();});});show();
})();
/* 3-4 지도 */
var RAT=X.map(function(r){return [r[4]/r[1],r[5]/r[1]];}),ZR=FL.standardize(RAT),K3=FL.kmeans(ZR,3,5,7);
(function(){var mh=[0,0,0],cn=[0,0,0];for(var i=0;i<N;i++){mh[K3.lab[i]]+=RAT[i][0];cn[K3.lab[i]]++;}for(var c=0;c<3;c++)mh[c]/=cn[c];var rk=[0,1,2].sort(function(a,b){return mh[b]-mh[a];}),rm={};rk.forEach(function(o,i){rm[o]=i;});K3.lab=K3.lab.map(function(l){return rm[l];});})();
(function(){var cv=$('#cv34'),col='none';
  function draw(){var f=fit(cv),g=f.c,A=FL.axes(g,f.W,f.H,{xmin:-5,xmax:8,ymin:-3,ymax:3,xlab:'PC1 · 크기 (작은 쪽 ← → 큰 쪽)',ylab:'PC2 · 체형 (↑ 납작)'});
    for(var i=0;i<N;i++)FL.dot(g,A.sx(S[i][0]),A.sy(S[i][1]),2.6,col==='sp'?SPC[D.sp[i]]:col==='cl'?CLC[K3.lab[i]]:'#8a96a3',col==='none'?.45:.65);
    if(col==='sp'){g.font='700 13px "IBM Plex Sans KR",sans-serif';SP.forEach(function(s){var m=[0,0],n=0;for(var i=0;i<N;i++)if(D.sp[i]===s){m[0]+=S[i][0];m[1]+=S[i][1];n++;}g.fillStyle='#16212b';g.fillText(SPKO[s],A.sx(m[0]/n)+6,A.sy(m[1]/n)-6);});}
    stamp(g,f.W,col==='sp'?'실제 데이터 · 이름표는 대조용':'실제 데이터 · 이름표 없이 그림');}
  function info(){if(col==='sp')FL.spLegend($('#lg34'));else if(col==='cl')FL.legend($('#lg34'),[['납작한 주머니',CLC[0]],['중간 주머니',CLC[1]],['길쭉한 주머니',CLC[2]]]);else $('#lg34').innerHTML='';
    FL.kpis($('#kp34'),[[FL.pct(PC.evr[0]),'PC1(크기)이 남긴 흔들림','g'],[FL.pct(PC.evr[1]),'PC2(체형)가 남긴 흔들림','m'],[FL.pct(PC.evr[0]+PC.evr[1]),'두 축 합계','a'],['0번','종 이름표를 쓴 횟수 (계산할 때)','i']]);
    $('#in34').innerHTML=col==='none'?'<p class="a">색 없이 보면 왼쪽 아래에서 오른쪽으로 뻗은 띠 하나처럼 보입니다. 하지만 띠가 위아래로 세 갈래로 갈라져 있습니다.</p>':col==='cl'?'<p class="m">2장에서 체형 비율로 나눈 세 주머니를 칠했습니다. 세 갈래가 PC2(체형) 방향으로 층을 이룹니다. 2장은 자를 사람이 골랐고, 3장은 PCA가 같은 방향을 스스로 찾았습니다.</p>':'<p class="g">덮어 둔 이름표를 켰습니다. 빙어는 왼쪽(작음), 강꼬치고기는 오른쪽 아래(크고 길쭉), 도미는 오른쪽 위(크고 납작)에 있습니다. 농어·로치·흰송어는 가운데서 겹칩니다.</p>';}
  $$('#p34 [data-c]').forEach(function(bt){bt.addEventListener('click',function(){col=bt.dataset.c;$$('#p34 [data-c]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();info();});});
  info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 3-5 복원 */
(function(){var cv=$('#cv35'),k=2,orig=[];for(var i=0;i<N;i++)if(D.orig[i])orig.push(i);var fi=20;
  function mse(k){var s=0;for(var i=0;i<N;i++){var zb=FL.unproject(S[i].slice(0,k),PC.vecs);for(var j=0;j<6;j++){var t=Z[i][j]-zb[j];s+=t*t;}}return s/(N*6);}
  var MSE={};for(var q=1;q<=6;q++)MSE[q]=mse(q);
  function draw(){var i=orig[fi],zb=FL.unproject(S[i].slice(0,k),PC.vecs),xb=zb.map(function(v,j){return v*MS.s[j]+MS.m[j];});
    $('#f35v').textContent=SPKO[D.sp[i]];var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=70,R=20,T=16,rowH=(f.H-T-20)/6;
    g.font='13px "IBM Plex Sans KR",sans-serif';for(var j=0;j<6;j++){var y=T+rowH*j+rowH/2,lo=Math.min(Z[i][j],zb[j],-2),hi=Math.max(Z[i][j],zb[j],3);function sx(v){return L+(v+3)/7*(f.W-L-R);}
      g.fillStyle='#16212b';g.textAlign='right';g.fillText(NAMES[j],L-8,y+4);g.fillStyle='rgba(31,122,82,.25)';g.fillRect(sx(0),y-7,sx(Z[i][j])-sx(0),14);
      g.strokeStyle='#c9302c';g.lineWidth=2;g.beginPath();g.moveTo(sx(Z[i][j]),y);g.lineTo(sx(zb[j]),y);g.stroke();FL.dot(g,sx(zb[j]),y,5,'#c9302c',1);}
    g.strokeStyle='#8a96a3';g.beginPath();g.moveTo(L+3/7*(f.W-L-R),T);g.lineTo(L+3/7*(f.W-L-R),f.H-10);g.stroke();g.textAlign='left';stamp(g,f.W,'초록 막대 = 원래 값 · 빨간 점 = 다시 편 값 (표준화 눈금)');
    $('#t35').innerHTML='<tr><th>측정값</th><th class="n">원래 값</th><th class="n">다시 편 값</th><th class="n">차이</th></tr>'+NAMES.map(function(n,j){return '<tr><td>'+n+' ('+FL.UNITS[j]+')</td><td class="n">'+X[i][j]+'</td><td class="n">'+xb[j].toFixed(j===0?0:2)+'</td><td class="n">'+(xb[j]-X[i][j]).toFixed(j===0?0:2)+'</td></tr>';}).join('');
    FL.kpis($('#kp35'),[[k,'남긴 축 수','i'],[FL.pct(PC.evr.slice(0,k).reduce(function(a,b){return a+b;},0)),'남긴 흔들림','g'],[MSE[k].toFixed(4),'전체 복원 오차 (평균 제곱)','a'],[Math.abs(xb[0]-X[i][0]).toFixed(0)+'g','이 물고기 무게 오차','r']]);
    $('#in35').innerHTML='<p class="'+(k>=4?'g':'a')+'">'+(k>=4?'축을 넷 이상 남기면 거의 원래대로 돌아옵니다. 남은 두 방향은 길이 세 값의 작은 차이뿐이었습니다.':'축 '+k+'개로 펴면 무게가 가장 많이 틀립니다. 크기·체형의 곧은 방향만으로는 "길이가 길면 무게는 훨씬 빨리 늘어난다"는 휜 관계를 다 되살리지 못합니다.')+'</p>';}
  $('#n35').addEventListener('input',function(){k=+this.value;$('#n35v').textContent=k;draw();});$('#f35').addEventListener('input',function(){fi=+this.value;draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 대결: 이웃 일치율 (같은 원본 묶음 제외) */
function agree(M){var ok=0;for(var i=0;i<N;i++){var o=-1,od=Infinity;for(var j=0;j<N;j++){if(j===i||D.seed[j]===D.seed[i])continue;var d=FL.d2(M[i],M[j]);if(d<od){od=d;o=j;}}if(D.sp[o]===D.sp[i])ok++;}return ok/N;}
Duel({el:'#d3',run:function(){var two=S.map(function(s){return s.slice(0,2);});return {fly:agree(two),robo:agree(Z)};},fmt:function(v){return FL.pct(v);},scale:1,bigGap:.1,
  report:function(r){return '가장 가까운 이웃이 같은 종인 비율은 초파리 쪽(두 축) '+FL.pct(r.fly)+', 주판봇 쪽(여섯 축) '+FL.pct(r.robo)+'예요. 차이는 '+((r.robo-r.fly)*100).toFixed(1)+'%p예요.';},
  verdict:{fly:'두 축으로도 이웃을 더 잘 찾았다. 초파리 승.',robo:'접으면 보기 쉬워지지만 잃는 것도 있다. 지도는 요약이지 원본이 아니다. 주판봇 승.',draw:'차이가 없다. 이번 판은 나눠 갖는다.'}});
'''


def main():
    USED.update(['fly_arms', 'fly_coffee', 'fly_cry', 'robo_sigh', 'robo_happy', 'robo_meh', 'fly_point', 'robo_coin'])
    hero_html = hero('3장 · 비지도학습 물고기 연구실', '접기 — 차원 축소', '숫자 여섯 개를 두 개로 접어도, 물고기의 모양은 남아 있을까?',
                     '물고기 한 마리는 숫자 여섯 개, 사람이 그릴 수 없는 여섯 방향의 점입니다. 이 장에서는 <b>주성분 분석(PCA)</b>으로 가장 많이 흔들리는 방향부터 줄을 세워, '
                     '종이 한 장 위의 <b>물고기 지도</b>를 그립니다. 그리고 접었다가 다시 펴 보며 무엇이 남고 무엇을 잃었는지 숫자로 확인합니다.',
                     [(pct(evr[0]), 'PC1(크기)이 남긴 흔들림', 'g'), (pct(evr[0] + evr[1]), 'PC1+PC2가 남긴 흔들림', 'i'),
                      (num(rec['2'], 4), '두 축으로 접었다 편 복원 오차 (표준화 눈금)', 'a'), (pct(nap['pc2']), '두 축 지도에서 이웃이 같은 종인 비율', 'm')],
                     [('doc', 'front', '오늘은 숫자를 접습니다. 접었는데도 모양이 남는지, 무엇을 잃는지 둘 다 숫자로 봅니다.'),
                      ('asst', 'smile', '여섯 개를 두 개로요? 그럼 넷은 버리는 거예요?'),
                      ('fly', 'point', '버리는 게 아니라 겹친 걸 모으는 거야. 길이 세 값은 사실상 한 값이었잖아.'),
                      ('robo', 'coin', '난 하나도 안 버릴 거야. 2연패는 여기서 끝낸다!')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a> 증강본'),
                 ('원자료', '안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 PART 2 차원 축소 (2026)'),
                 ('PCA 수치', 'code/analysis.py (scikit-learn 1.9.1)와 이 페이지의 직접 계산(야코비 방법)이 같은 값'),
                 ('주성분 분석', 'Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. Philosophical Magazine, 2(11), 559–572'),
                 ('고유 얼굴', 'Turk, M., & Pentland, A. (1991). Eigenfaces for recognition. Journal of Cognitive Neuroscience, 3(1), 71–86')],
                ['수식 상자의 좌표 (2, 1)과 방향 (0.6, 0.8)은 예시값', '3-5의 "물고기 고르기"는 원본 158마리 중에서 고름', '얼굴 이야기(생성 AI로 치면)는 그림 없이 말로만 설명'],
                prev=('02_grouping.html', '2장 · 묶기 — 군집화'), nxt=('04_guessing.html', '4장 · 맞히기 — 자기지도학습'))
    return build(P, title='3장 · 접기 — 차원 축소 · 비지도학습 물고기 연구실',
                 desc='물고기 측정값 여섯 개를 주성분 분석(PCA)으로 두 축(크기·체형)으로 접어 지도를 그리고, 다시 펴서 잃은 것을 확인한다.',
                 nav=[('#first', '3줄'), ('#s1', '3-1 겹친 정보'), ('#s2', '3-2 긴 방향'), ('#s3', '3-3 네 걸음'), ('#s4', '3-4 지도'), ('#s5', '3-5 복원'), ('#duel', '대결'), ('#sum', '정리')],
                 cover_html=cover('cover_03', '3장 · 접기', '접기 — 차원 축소'), hero=hero_html, body=b, gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_03')


if __name__ == '__main__':
    print(main())
