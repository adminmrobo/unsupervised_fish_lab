# -*- coding: utf-8 -*-
"""2장 · 묶기 — 군집화 (k-평균, 엘보, 실루엣, 계층 군집, 체형 세 갈래)"""
from lib import *

P = '02_grouping.html'
kr = R['kmr']; k6 = R['km6']; t3 = R['ratio_k3_table']; hrs = R['hr_by_species']


def body():
    b = three([
        ('무엇을', '이름표 없는 물고기 1,554마리를 "주머니(군집)" 몇 개에 나눠 담습니다. 담는 법(k-평균, 계층 군집)과 주머니 수를 고르는 법(엘보, 실루엣)을 봅니다.'),
        ('왜 중요한가', '데이터를 처음 받으면 "몇 종류가 섞여 있나"부터 알고 싶습니다. 군집화는 그 첫 질문에 답하는 도구입니다.'),
        ('업무에서는', '고객을 구매 패턴으로 묶어 맞춤 안내를 보내거나, 설비를 진동 패턴으로 묶어 점검 순서를 정할 때 씁니다.')],
        '코드·수식을 몰라도 됩니다. 원자료 슬라이드의 "무대"를 이 시리즈에서는 "주머니"라고 부릅니다(같은 뜻, 군집).',
        [('k-means', 'k-평균. 주머니 k개의 중심을 반복해서 다시 잡는 군집화'), ('ARI', 'Adjusted Rand Index, 조정 랜드 지수 (이름표와의 대조 점수)'), ('Ward', '워드 연결법. 합쳤을 때 흩어짐이 가장 적게 느는 쌍부터 합침')])

    b += section('map', '큰 그림 — 1장의 거리로 주머니를 나눈다',
                 '<div class="mapbar"><span>1장 · 거리·표준화</span><i>→</i><span class="on">2장 · 묶기</span><i>→</i><span>3장 · 접기</span><i>→</i><span>4장 · 맞히기</span><i>→</i><span>실전 연습장</span></div>'
                 + say('sia', 'explain', '순서대로 말씀드릴게요. 2-1에서 주머니에 담는 네 걸음을 보고, 2-2·2-3에서 주머니 수를 고르고, 2-4에서 다른 담는 법을 보고, 2-5에서 결과를 이름표와 대조합니다.')
                 + '<p>이 장은 <b>체형 비율 두 개</b>로 물고기를 나눕니다. 높이 ÷ 길이1(몸이 얼마나 납작한가)과 폭 ÷ 길이1(몸이 얼마나 두꺼운가)입니다. '
                 '1장에서 본 것처럼 원 단위 측정값을 그대로 쓰면 크기(무게)가 모든 것을 정하기 때문에, 크기를 뺀 생김새로 자를 바꿨습니다. 두 비율도 표준화한 뒤 거리를 잽니다.</p>')

    # 2-1 k-means
    s = say('doc', 'think', '상황 하나. 어시장 진열대가 세 개 있습니다. 이름표 없이 생김새만 보고 물고기를 진열대 세 곳에 나눠 놓으려면, 어디서부터 시작할까요?')
    s += duo(why([('문제 상황', '1,554마리를 몇 무리로 나누고 싶은데, 어떤 무리가 있는지 알려 줄 사람이 없습니다.'),
                  ('앞 방법의 한계', '1장의 거리는 "두 마리가 얼마나 닮았나"만 알려 줍니다. 전체를 몇 무리로 나눌지는 말해 주지 않습니다.'),
                  ('해법', '주머니 중심 k개를 놓고, 각 물고기를 가장 가까운 중심의 주머니에 넣고, 주머니 평균으로 중심을 옮기는 일을 반복합니다(k-평균).')],
                 '친구들이 운동장에 흩어져 있을 때 깃발 세 개를 꽂고 "가까운 깃발로 모여!"를 외친 뒤, 모인 무리의 한가운데로 깃발을 옮기기를 되풀이하는 것과 같습니다.'),
             mathbox('중심을 "평균 위치로 옮긴다"는 게 무슨 계산이에요?', '평균(초등 5학년) + 두 점 사이의 거리(중학교 3학년)',
                     '새 중심 = 주머니 안 점들의 평균',
                     [('중심', '센트로이드', '주머니를 대표하는 점'), ('배정', '', '각 점을 가장 가까운 중심의 주머니에 넣기'),
                      ('안쪽 거리 합', '이너셔(inertia)', '각 점과 자기 중심 사이 거리 제곱의 합. 작을수록 주머니가 촘촘함')],
                     '수직선 위 점 1, 2, 9와 중심 0, 10. ① 배정: 1과 2는 0 쪽, 9는 10 쪽. ② 새 중심: (1+2)÷2 = <b>1.5</b>, 9 ÷ 1 = <b>9</b>. '
                     '③ 다시 배정해도 그대로라 멈춥니다. 안쪽 거리 합 = 0.5² + 0.5² + 0² = <b>0.5</b>.',
                     '평균 내고, 가까운 데 넣고, 다시 평균 내고. 더 안 움직이면 끝이네요!'))
    s += sup('KNN의 k는 "이웃 몇 마리를 볼까"였습니다. 새 물고기 둘레의 이름표 붙은 이웃 k마리가 투표했습니다.',
             'k-평균의 k는 "주머니 몇 개로 나눌까"입니다. 이름은 같은 k지만 뜻이 전혀 다릅니다. 투표할 이름표도 없습니다.')
    s += talk([('doc', 'board', '깃발(중심)을 처음 어디에 꽂느냐에 따라 결과가 달라질까요?'),
               ('robo', 'coin', '어디 꽂든 반복하면 똑같아지지. 계산은 거짓말 안 해!'),
               ('fly', 'point', '"중심 다시 놓기"를 여러 번 눌러 봐. k를 5로 올리고 눌러 보면 더 잘 보여.'),
               ('asst', 'report', 'k가 3일 때는 거의 늘 같은 곳에 멈추는데, k를 올리면 시작 위치에 따라 안쪽 거리 합이 달라져요.')])
    s += panel('p21', '실험 · k-평균 네 걸음', '실제 데이터 · 계산은 이 페이지가 직접',
               '<div class="ctrl"><div class="group"><span class="glabel">주머니 수 k</span><input type="range" id="k21" min="2" max="6" value="3" aria-label="주머니 수"><span class="val" id="k21v">3</span></div>'
               '<div class="group"><button class="bt" id="i21">중심 다시 놓기</button><button class="bt" id="s21">한 걸음</button><button class="bt primary" id="r21">끝까지</button></div></div>'
               '<div class="flow" id="f21"><span class="s" data-f="0">① 중심 놓기</span><i>→</i><span class="s" data-f="1">② 가까운 중심에 배정</span><i>→</i><span class="s" data-f="2">③ 평균으로 중심 옮기기</span><i>→</i><span class="s" data-f="3">④ 안 움직이면 멈춤</span></div>'
               + canvas('cv21', 360, '높이÷길이1(가로)과 폭÷길이1(세로)로 그린 물고기와 주머니 중심') +
               '<section class="kpis" id="kp21" aria-label="숫자 요약"></section><div class="insight" id="in21" aria-live="polite"></div>', real=True)
    s += explain(['중심 k개를 놓습니다. 이 페이지는 서로 멀리 떨어지게 뽑는 방법(k-means++)을 씁니다.',
                  '물고기마다 가장 가까운 중심의 주머니에 넣습니다. 거리는 1장의 유클리드 거리입니다.',
                  '주머니마다 들어온 물고기의 평균 위치로 중심을 옮깁니다. 2와 3을 되풀이하다가 더는 움직이지 않으면 멈춥니다.'],
                 'k를 사람이 정해야 하고, 시작 위치에 따라 다른 답에 닿을 수 있습니다. 또 둥근 덩어리는 잘 찾지만 반달처럼 휘었거나 서로 감싼 모양은 잘 못 찾습니다.')
    s += codefold([('KMeans(n_clusters=3, n_init=10, random_state=42)', '주머니 3개. 시작 위치를 10번 바꿔 가장 촘촘한 답을 고름. 시작 순서는 42번으로 고정'),
                   ('labels = km.fit_predict(Z)', '물고기마다 주머니 번호(0, 1, 2)를 받습니다'),
                   ('km.inertia_', '안쪽 거리 합')])
    s += quiz('q21')
    b += step('s1', '2-1', 'k-평균 — 깃발 꽂고, 모이고, 옮기고', ['방법: k-평균(k-means)', '일상: 운동장 깃발 모이기'], s)

    # 2-2 elbow
    s = say('doc', 'think', '주머니를 몇 개로 할지 정해 주는 사람이 없습니다. 주머니 수를 늘리면 무엇이 좋아지고, 무엇을 잃을까요?')
    s += duo(why([('문제 상황', 'k-평균은 k를 사람이 정해야 합니다. 그런데 몇 종류가 섞였는지 모르는 것이 출발점이었습니다.'),
                  ('앞 방법의 한계', '안쪽 거리 합은 k를 늘릴수록 무조건 줄어듭니다. 1,554개로 나누면 0입니다. 작은 것만 고르면 늘 "최대한 많이"가 답이 됩니다.'),
                  ('해법', 'k를 1부터 늘리며 안쪽 거리 합이 "줄어드는 폭"이 꺾이는 지점(팔꿈치, 엘보)을 찾습니다.')],
                 '반찬을 한 가지 더 할 때마다 만족이 늘지만, 어느 순간부터는 늘어나는 만족이 확 작아집니다. 그 꺾이는 곳에서 멈춥니다.'),
             mathbox('"꺾인다"는 걸 숫자로는 어떻게 봐요?', '줄어든 양 비교 — 이웃한 두 값의 차(계차)',
                     '줄어든 폭 = 안쪽 거리 합(k−1) − 안쪽 거리 합(k)',
                     [('k', '케이', '주머니 수'), ('안쪽 거리 합(k)', '', '주머니 k개일 때의 촘촘함'), ('줄어든 폭', '', '주머니를 하나 더 만들어 얻은 것')],
                     '체형 비율 두 개로 잰 값: k=1 %s → k=2 %s → k=3 %s → k=4 %s. 줄어든 폭은 %s, %s, 그다음엔 %s뿐입니다. '
                     'k=3 다음부터 얻는 것이 확 줄어듭니다.' % (num(kr['1']['inertia'], 1), num(kr['2']['inertia'], 1), num(kr['3']['inertia'], 1), num(kr['4']['inertia'], 1),
                                                     num(kr['1']['inertia'] - kr['2']['inertia'], 1), num(kr['2']['inertia'] - kr['3']['inertia'], 1), num(kr['3']['inertia'] - kr['4']['inertia'], 1)),
                     '빼기만 했는데 팔꿈치가 보여요. 1,894 → 805 → 153으로 얻는 게 확 줄었어요.'))
    s += sup('이웃 수 k를 정할 때는 검증 데이터의 정답률이 가장 높은 k를 골랐습니다. 정답이 있으니 기준이 분명했습니다.',
             '정답률이 없으니 엘보(줄어드는 폭)와 실루엣(2-3) 같은 모양 점수를 봅니다. 둘이 같은 k를 가리키면 더 믿을 만합니다.')
    s += talk([('doc', 'think', '측정값 여섯 개로 재든, 체형 비율 두 개로 재든 팔꿈치가 똑같이 보일까요?'),
               ('robo', 'coin', '변수가 많을수록 정보가 많으니까 여섯 개 쪽이 더 또렷하겠지!'),
               ('fly', 'point', '아래 "자" 버튼을 바꿔 봐. 어느 쪽 곡선이 진짜로 꺾이나.'),
               ('asst', 'report', '여섯 개 쪽은 완만하게 휘어서 어디가 팔꿈치인지 흐려요. 체형 비율 쪽은 k=3에서 확 꺾여요.')])
    s += panel('p22', '실험 · 엘보와 실루엣 한눈에', 'scikit-learn 값 (code/analysis.py)',
               '<div class="ctrl"><div class="group"><span class="glabel">자(무엇으로 재나)</span><button class="bt" data-r="ratio" aria-pressed="true">체형 비율 2개 (표준화)</button>'
               '<button class="bt" data-r="six" aria-pressed="false">측정값 6개 (표준화)</button></div></div>'
               + canvas('cv22', 320, '주머니 수에 따른 안쪽 거리 합(선)과 실루엣 점수(막대)') +
               '<div class="legend"><span><i style="background:#1f7a52"></i>안쪽 거리 합 (왼쪽 눈금)</span><span><i style="background:#1e55c8"></i>실루엣 점수 (오른쪽 눈금)</span></div>'
               '<div class="insight" id="in22" aria-live="polite"></div>', real=True)
    s += explain(['안쪽 거리 합은 k가 커질수록 늘 줄어듭니다. 그래서 "가장 작은 k"가 아니라 "꺾이는 k"를 봅니다.',
                  '체형 비율로 재면 k=3에서 또렷이 꺾이고, 실루엣도 k=3에서 %s로 가장 높습니다.' % num(kr['3']['sil'], 3),
                  '측정값 여섯 개로 재면 곡선이 완만하고, 실루엣은 k=2(%s)가 가장 높습니다. 크기(큰 물고기·작은 물고기)로 둘로 나누는 답입니다.' % num(k6['2']['sil'], 3)],
                 '엘보는 대략적인 힌트일 뿐 정답이 아닙니다. 꺾임이 흐리면 실루엣 점수와 현장의 뜻(이 주머니들이 쓸모 있나)을 함께 봅니다. 숫자가 아니라 판단입니다.')
    s += aicheck('"주머니 1,554개면 완벽!"',
                 '<p>주판봇이 보고서를 냈습니다. "주머니를 1,554개로 나눴더니 안쪽 거리 합이 0이 됐어. 오차 0, 완벽한 군집이야!"</p>'
                 '<p><b>확인 질문</b> 안쪽 거리 합이 0인데 왜 쓸모가 없을까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>물고기마다 자기 혼자 주머니에 들어가면 거리가 0이 되는 게 당연합니다. 아무것도 묶지 않았습니다. '
                 '안쪽 거리 합은 k를 늘리면 무조건 줄어드는 숫자라서, 그것만 보고 k를 고르면 안 됩니다. 지도학습에서 훈련 데이터 정답률 100%가 "외웠다"는 뜻이었던 것과 닮았습니다.</p></details>')
    s += codefold([('[KMeans(k).fit(Z).inertia_ for k in range(1, 9)]', 'k를 1부터 8까지 바꿔 가며 안쪽 거리 합을 모읍니다'),
                   ('plt.plot(range(1, 9), inertias)', '그 값을 선으로 그려 팔꿈치를 찾습니다')])
    s += quiz('q22')
    b += step('s2', '2-2', '주머니는 몇 개인가 — 엘보 방법', ['방법: 엘보(elbow)', '일상: 반찬 하나 더의 만족'], s)

    # 2-3 silhouette
    s = say('doc', 'think', '주머니를 나눈 뒤 "잘 나눴다"를 숫자로 말하려면, 물고기 한 마리에게 무엇을 물어보면 될까요?')
    s += duo(why([('문제 상황', '주머니를 나눴지만 잘 나눴는지 채점해 줄 정답표가 없습니다.'),
                  ('앞 방법의 한계', '엘보는 주머니 안쪽만 봅니다. 옆 주머니와 얼마나 떨어져 있는지는 보지 않습니다.'),
                  ('해법', '점마다 "내 주머니 친구들과의 평균 거리(a)"와 "가장 가까운 옆 주머니와의 평균 거리(b)"를 재서 비교합니다(실루엣).')],
                 '같은 반 친구들 곁에 붙어 있고 옆 반과는 떨어져 있으면, 반 나누기가 잘된 것입니다.'),
             mathbox('a, b, max… max는 뭐예요?', '분수와 큰 값 고르기 — 차이를 큰 쪽으로 나눠 −1~+1로 맞추기',
                     '실루엣 s = (b − a) ÷ max(a, b)',
                     [('a', '에이', '내 주머니 친구들까지 평균 거리'), ('b', '비', '가장 가까운 옆 주머니까지 평균 거리'),
                      ('max(a, b)', '맥스', 'a와 b 중 큰 값'), ('s', '에스', '+1에 가까우면 잘 나뉨, 0 근처면 경계, 음수면 잘못 들어감')],
                     'a = 0.4, b = 1.6이면 s = (1.6 − 0.4) ÷ 1.6 = <b>0.75</b> (잘 나뉨). a = 1.0, b = 1.1이면 s = 0.1 ÷ 1.1 ≈ <b>0.09</b> (경계에 섬).',
                     '"옆 반까지 거리"에서 "우리 반까지 거리"를 빼서 비교하는 거군요. 아래 그림에서 점을 눌러 직접 재 볼게요.'))
    s += sup('정답률이 채점표였습니다. 맞으면 1, 틀리면 0을 매겨 평균을 냈습니다.',
             '실루엣이 채점표입니다. 정답 없이 점마다 −1~+1 점수를 매겨 평균을 냅니다. 다만 높다고 "종을 맞혔다"는 뜻은 아닙니다.')
    s += talk([('doc', 'board', '주머니 경계에 서 있는 물고기는 실루엣이 어떻게 나올까요?'),
               ('robo', 'coin', '어느 주머니에 들어갔든 들어갔으면 된 거지. 다 1점!'),
               ('fly', 'point', '두 주머니 사이에 낀 점을 눌러 봐. a와 b가 얼마나 비슷한지.'),
               ('asst', 'report', '경계 점은 a와 b가 비슷해서 0 근처가 나와요. 가운데 점은 0.8을 넘고요.')])
    s += panel('p23', '실험 · 점 하나의 실루엣 재기', '실제 데이터 · 계산은 이 페이지가 직접',
               '<p class="small muted">그림 속 점을 누르거나 탭하면 그 물고기의 a, b, s를 계산합니다. 주머니는 2-1과 같은 k-평균(k=3) 결과입니다.</p>'
               + canvas('cv23', 340, '주머니 셋으로 나눈 물고기, 고른 점과 a·b를 잰 선') +
               '<section class="kpis" id="kp23" aria-label="숫자 요약"></section><div class="insight" id="in23" aria-live="polite"></div>', real=True)
    s += explain(['a는 내 주머니 안 다른 물고기들까지의 평균 거리, b는 가장 가까운 옆 주머니 물고기들까지의 평균 거리입니다.',
                  's = (b − a) ÷ max(a, b). 모든 물고기의 s를 평균 내면 주머니 나누기 전체의 점수가 됩니다.',
                  '체형 비율로 나눈 k=3의 평균 실루엣은 %s입니다(scikit-learn 값). 이 페이지의 계산도 같은 자리에서 나옵니다.' % num(kr['3']['sil'], 3)],
                 '실루엣이 가장 높은 k가 현장에서 늘 쓸모 있는 k는 아닙니다. 주머니 다섯 개가 현장에서 쓸모없는 다섯 개라면, 주머니 세 개가 답일 수 있습니다.')
    s += codefold([('silhouette_score(Z, labels)', '모든 점의 실루엣 평균'),
                   ('silhouette_samples(Z, labels)', '점 하나하나의 실루엣')])
    s += quiz('q23')
    b += step('s3', '2-3', '나눠 놓고 검증하기 — 실루엣 점수', ['방법: 실루엣(silhouette)', '일상: 우리 반과 옆 반'], s)

    # 2-4 hierarchical
    s = say('doc', 'think', '주머니 수를 처음부터 정하지 않고, 가까운 것끼리 하나씩 합쳐 가다가 "여기서 자르자"고 정하는 방법은 없을까요?')
    s += duo(why([('문제 상황', 'k-평균은 k를 먼저 정해야 하고, 시작 위치에 따라 답이 흔들립니다.'),
                  ('앞 방법의 한계', '"왜 하필 3개인가"를 그림으로 설명하기 어렵습니다.'),
                  ('해법', '물고기 한 마리씩 주머니로 시작해, 합쳤을 때 흩어짐이 가장 적게 느는 두 주머니부터 계속 합칩니다. 합친 기록이 족보 나무(덴드로그램)가 됩니다.')],
                 '집안 족보처럼, 가까운 형제끼리 먼저 묶이고, 사촌, 육촌 순으로 묶입니다. 어느 촌수에서 자르느냐가 주머니 수를 정합니다.'),
             mathbox('"흩어짐이 가장 적게 느는 쌍"은 어떻게 골라요?', '평균과 거리의 제곱 — 두 무리를 합칠 때 늘어나는 안쪽 거리 합',
                     '합치는 비용 = (n<sub>A</sub>·n<sub>B</sub> ÷ (n<sub>A</sub>+n<sub>B</sub>)) × (중심 거리)²',
                     [('n<sub>A</sub>, n<sub>B</sub>', '엔 에이, 엔 비', '두 주머니에 든 물고기 수'), ('중심 거리', '', '두 주머니 평균 위치 사이의 거리')],
                     '수직선 위 점 1, 2, 9. {1}과 {2}를 합치면 (1·1÷2) × 1² = <b>0.5</b>. {1, 2}(중심 1.5)와 {9}를 합치면 (2·1÷3) × 7.5² = <b>37.5</b>. 비용이 작은 1과 2를 먼저 합칩니다.',
                     '멀리 떨어진 무리를 합치면 비용이 확 커지니까, 나무의 높은 가지가 되는 거네요.'))
    s += sup('결정나무는 위에서 아래로 "높이 ÷ 길이가 0.4보다 큰가?" 같은 질문으로 나눴습니다. 질문은 정답을 잘 가르는 쪽으로 골랐습니다.',
             '계층 군집은 거꾸로 아래에서 위로 합칩니다. 질문도 정답도 없이 거리만 봅니다. 어디서 자를지는 사람이 나무를 보고 정합니다.')
    s += talk([('doc', 'think', '나무 어디서 자르면 좋을까요?'),
               ('robo', 'coin', '많이 자를수록 자세하니까 맨 아래에서 잘게 자르자!'),
               ('fly', 'point', '가지가 길게 뻗은 곳을 봐. 자르는 줄을 움직여서 긴 가지를 끊어 봐.'),
               ('asst', 'report', '세 갈래로 자를 때 가지가 가장 길어요. 그 위로는 한참 올라가야 합쳐져요.')])
    s += panel('p24', '실험 · 족보 나무(덴드로그램) 자르기', '원본 158마리 · 계산은 이 페이지가 직접',
               '<div class="ctrl"><div class="group"><span class="glabel">자르는 높이 → 주머니 수</span><input type="range" id="k24" min="2" max="7" value="3" aria-label="주머니 수"><span class="val" id="k24v">3</span></div>'
               '<div class="group"><button class="bt" id="lb24" aria-pressed="false">이름표 대조하기</button></div></div>'
               + canvas('cv24', 360, '원본 물고기 158마리를 워드 방법으로 합친 족보 나무와 자르는 선', wide=True) +
               '<section class="kpis" id="kp24" aria-label="숫자 요약"></section><div class="insight" id="in24" aria-live="polite"></div>', real=True)
    s += explain(['처음에는 물고기 158마리가 각자 주머니입니다. 합치는 비용이 가장 작은 두 주머니를 합치기를 157번 되풀이합니다.',
                  '나무의 높이는 합칠 때 늘어난 흩어짐입니다. 높이가 크게 뛰는 곳 바로 아래에서 자르면, 서로 멀리 떨어진 무리가 남습니다.',
                  'k를 미리 정하지 않아도 "왜 여기서 잘랐는지"를 그림으로 설명할 수 있습니다.'],
                 '한 번 합친 것은 되돌릴 수 없습니다. 데이터가 크면 느립니다(1,554마리 전체 대신 원본 158마리로 그린 이유). 초기의 작은 합침 하나가 전체 모양을 정할 수 있습니다.')
    s += codefold([('AgglomerativeClustering(n_clusters=3, linkage="ward")', '워드 방법으로 아래에서부터 합쳐 세 주머니에서 멈춤'),
                   ('scipy.cluster.hierarchy.dendrogram(linkage(Z, "ward"))', '족보 나무 그림')])
    s += quiz('q24')
    b += step('s4', '2-4', '족보로 보는 묶기 — 계층 군집', ['방법: 계층 군집(워드 연결)', '일상: 집안 족보'], s)

    # 2-5 result
    def row(sp):
        t = t3[sp]
        return '<tr><td><span class="swatch" data-sp="%s"></span>%s (%s)</td><td class="n">%s</td><td class="n">%d</td><td class="n">%d</td><td class="n">%d</td></tr>' % (
            sp, {'Bream': '도미', 'Parkki': '파르키', 'Perch': '농어', 'Pike': '강꼬치고기', 'Roach': '로치', 'Smelt': '빙어', 'Whitefish': '흰송어'}[sp], sp,
            num(hrs[sp][0], 3), t['flat'], t['mid'], t['long'])
    tbl = ('<div class="tw"><table class="tb"><tr><th>종 (마지막에 꺼낸 이름표)</th><th class="n">높이÷길이1 평균</th><th class="n">납작한 주머니</th><th class="n">중간 주머니</th><th class="n">길쭉한 주머니</th></tr>'
           + ''.join(row(sp) for sp in ['Bream', 'Parkki', 'Whitefish', 'Roach', 'Perch', 'Smelt', 'Pike']) + '</table></div>')
    s = say('doc', 'think', '드디어 덮어 둔 이름표를 꺼낼 시간입니다. AI가 나눈 세 주머니는 실제 종과 얼마나 닮았을까요?')
    s += '<p>체형 비율 두 개로 k-평균(k=3)을 돌리고, 그 뒤에 이름표를 꺼내 표로 맞춰 봤습니다(scikit-learn 값).</p>' + tbl
    s += sup('일곱 종을 하나하나 맞혔습니다. 물고기 단위로 나눠 채점한 정답률이 KNN %s였습니다.' % pct(R['supervised']['knn1_group_cv']),
             '일곱 종이 아니라 체형 세 갈래가 나왔습니다. 도미와 파르키는 생김새가 거의 같아 한 주머니에 들어갔고, 농어·로치·흰송어도 한 주머니입니다. 이름표와의 대조 점수(조정 랜드 지수)는 %s입니다.' % num(kr['3']['ari'], 3))
    s += talk([('doc', 'think', '세 주머니면 일곱 종을 못 맞힌 실패일까요?'),
               ('robo', 'coin', '일곱 개 중 세 개면 43%야. 낙제지!'),
               ('fly', 'point', '물어본 게 다르잖아. "이름표 대조하기"를 켜고 주머니 안을 봐. 섞인 종들이 서로 닮았나?'),
               ('asst', 'report', '납작한 주머니엔 도미와 파르키만, 길쭉한 주머니엔 강꼬치고기와 빙어가 모였어요. 생김새로는 정말 같은 무리예요.')])
    s += panel('p25', '실험 · 주머니와 이름표 대조', '실제 데이터',
               '<div class="ctrl"><div class="group"><span class="glabel">색</span><button class="bt" data-c="cl" aria-pressed="true">AI가 나눈 주머니</button><button class="bt" data-c="sp" aria-pressed="false">덮어 둔 종 이름표</button></div>'
               '<div class="group"><span class="glabel">자</span><button class="bt" data-f="ratio" aria-pressed="true">체형 비율 2개</button><button class="bt" data-f="six" aria-pressed="false">측정값 6개 (표준화)</button><button class="bt" data-f="raw" aria-pressed="false">측정값 6개 (원 단위)</button></div></div>'
               + canvas('cv25', 340, '체형 비율 평면 위 물고기, 주머니 색 또는 종 색') +
               '<div class="legend" id="lg25"></div><section class="kpis" id="kp25" aria-label="숫자 요약"></section><div class="insight" id="in25" aria-live="polite"></div>', real=True)
    s += '<div class="steps"><div><span class="n">1</span><h4>주머니 ≠ 종</h4><p>같은 주머니에 다른 종이, 같은 종이 다른 주머니에 있을 수 있습니다. 군집은 "닮음"이지 "정체"가 아닙니다.</p></div>' \
         '<div><span class="n">2</span><h4>원인이 아니다</h4><p>"이 주머니는 먹이 때문에 생겼다"는 말은 군집만으로는 뒷받침되지 않습니다. 닮음 위에 이야기를 얹는 순간 조심해야 합니다.</p></div>' \
         '<div><span class="n">3</span><h4>경계는 임의적</h4><p>두 주머니 사이의 점은 어느 쪽으로든 갈 수 있습니다(빙어 4마리가 중간 주머니로 갔습니다). 그 점들 때문에 결론이 뒤집히지 않는지 봅니다.</p></div></div>'
    s += explain(['체형 비율로 나누면 납작한(도미·파르키), 중간(농어·로치·흰송어), 길쭉한(강꼬치고기·빙어) 세 갈래가 이름표 없이 나옵니다.',
                  '같은 k=3이라도 자를 바꾸면 결과가 완전히 달라집니다. 측정값 여섯 개(표준화)로 나누면 이름표와의 대조 점수가 %s, 원 단위면 %s로 떨어집니다. 크기로 나뉘기 때문입니다.' % (num(k6['3']['ari'], 3), num(R['raw_k3_ari'], 3)),
                  '"어떤 자로 잴까"는 사람이 고르고, 그 자로 나누는 일은 AI가 합니다. 이 장의 가장 큰 교훈입니다.'],
                 '세 주머니 안에 섞인 종(예: 농어·로치·흰송어)은 체형 비율 두 개로는 가를 수 없습니다. 다음 장에서는 숫자를 "접어서" 다른 방향의 차이를 찾아봅니다.')
    s += quiz('q25')
    b += step('s5', '2-5', '체형으로만 나눠 본 결과 — 주머니와 이름표', ['결과: 체형 세 갈래', '일상: 진열대 정리'], s)

    b += duel('d2', '주머니 몇 개로 나눌까', '주머니 3개 (엘보·실루엣이 가리킨 수)', '주머니 7개 (종 수만큼)',
              '"팔꿈치가 3에서 꺾였어. 데이터가 말한 수를 따르자."', '"종이 일곱이면 주머니도 일곱! 많이 나눌수록 정확하지."',
              '평균 실루엣 점수 (이름표 없이 재는 모양 점수)')

    b += section('sum', '정리 — 묶기의 도구들',
                 '<div class="tw"><table class="tb"><tr><th>도구</th><th>하는 일</th><th>정해야 할 것</th><th>조심할 것</th></tr>'
                 '<tr><td>k-평균</td><td>중심 k개를 반복해서 옮기며 나눔</td><td>k, 자(어떤 변수로 잴지)</td><td>시작 위치, 둥글지 않은 모양</td></tr>'
                 '<tr><td>엘보</td><td>k에 따른 안쪽 거리 합의 꺾임</td><td>—</td><td>꺾임이 흐릴 수 있음</td></tr>'
                 '<tr><td>실루엣</td><td>점마다 a·b 비교, −1~+1</td><td>—</td><td>높다고 정체를 맞힌 것은 아님</td></tr>'
                 '<tr><td>계층 군집</td><td>가까운 것부터 합쳐 족보 나무</td><td>자르는 높이</td><td>되돌릴 수 없음, 큰 데이터에 느림</td></tr></table></div>'
                 + bridge('gen', '생성 AI로 치면', '검색 증강 생성(RAG)은 문서를 숫자로 바꾼 뒤 비슷한 문서끼리 묶거나, 질문과 가까운 문서를 찾아 씁니다. 그 "가까움"이 이 장의 거리입니다.',
                          '문서 묶음은 사람이 뜻을 바로 읽기 어려워, 주머니마다 대표 문서를 사람이 읽어 이름을 붙여야 합니다.')
                 + bridge('field', '현장에 옮기면', '고객 군집을 만들면 주머니마다 대표 고객 몇 명의 실제 기록을 읽어 보고 이름을 붙입니다. 이름 붙이기는 AI가 아니라 담당자의 일입니다.',
                          '군집은 시간이 지나면 바뀝니다. 몇 달마다 다시 돌려 주머니가 그대로인지 확인합니다.'))
    b += outro([('doc', 'front', '오늘 세 줄 정리. ① k-평균은 깃발 꽂고 모이기를 되풀이한다. ② 주머니 수는 엘보와 실루엣으로 고른다. ③ 주머니는 닮음이지 정체가 아니다.'),
                ('fly', 'arms', '데이터가 3이라고 하면 3이야. 일곱 종이 있어도 생김새는 세 갈래였어.'),
                ('robo', 'sigh', '많이 나눈다고 정확해지는 게 아니었네. 2연패라니… 3장에서는 꼭 본전 찾는다.'),
                ('asst', 'spark', '다음 장에서는 숫자 여섯 개를 두 개로 접어서, 주머니 안에 섞인 종들을 다시 볼게요.')],
               '연구실 식구 네 명이 진열대 세 곳에 체형별로 나뉜 물고기를 가리키는 장면')
    return b


GLOSS = {
    '군집화': ['군집화 (clustering)', '정답 없이 비슷한 것끼리 무리(주머니)로 나누는 일.'],
    '주머니': ['주머니 (군집, cluster)', 'AI가 나눈 무리 하나. 원자료의 "무대"와 같은 뜻.'],
    'k-평균': ['k-평균 (k-means)', '중심 k개를 놓고, 가까운 점 모으기와 평균으로 중심 옮기기를 반복하는 군집화.'],
    '중심': ['중심 (centroid)', '주머니 안 점들의 평균 위치. 주머니를 대표하는 점.'],
    '안쪽 거리 합': ['안쪽 거리 합 (inertia)', '각 점과 자기 주머니 중심 사이 거리 제곱의 합. 작을수록 촘촘함.'],
    '엘보': ['엘보 방법 (elbow method)', 'k를 늘리며 안쪽 거리 합이 줄어드는 폭이 꺾이는 곳을 k 후보로 고르는 방법.'],
    '실루엣': ['실루엣 점수 (silhouette)', '(b − a) ÷ max(a, b). 내 주머니엔 붙고 옆 주머니와는 떨어진 정도, −1~+1.'],
    '계층 군집': ['계층 군집 (hierarchical clustering)', '가까운 주머니부터 차례로 합쳐 족보 나무를 만드는 군집화.'],
    '덴드로그램': ['덴드로그램 (dendrogram)', '계층 군집의 합친 기록을 그린 족보 나무. 높이는 합칠 때 늘어난 흩어짐.'],
    '조정 랜드 지수': ['조정 랜드 지수 (ARI)', 'AI가 나눈 주머니와 실제 이름표가 얼마나 같은지 재는 대조 점수. 1이면 같고 0이면 우연 수준.'],
    '체형 비율': ['체형 비율', '높이 ÷ 길이1, 폭 ÷ 길이1. 크기를 빼고 생김새만 남긴 값.'],
    'KNN': ['KNN (k-최근접 이웃)', '지도학습에서 새 물고기 둘레의 이름표 붙은 이웃 k마리가 투표해 종을 정하는 방법.'],
}

QUIZ = {
    'q21': [{'q': 'k-평균의 한 걸음에서 중심은 어디로 옮기나?', 'o': ['가장 먼 점', '주머니 안 점들의 평균 위치', '전체 데이터의 평균'], 'a': 1,
             'why': '주머니에 들어온 점들의 평균 위치로 옮깁니다.', 'hint': '중심은 주머니를 대표하는 "가운데"입니다.'},
            {'q': 'KNN의 k와 k-평균의 k는?', 'o': ['같은 뜻이다', '다르다: 이웃 수와 주머니 수'], 'a': 1,
             'why': 'KNN의 k는 투표할 이웃 수, k-평균의 k는 나눌 주머니 수입니다.', 'hint': '하나는 이름표가 있고 하나는 없습니다.'}],
    'q22': [{'q': '안쪽 거리 합이 k=2에서 1,214.9, k=3에서 410.3, k=4에서 257.8이다. k=3→4에서 줄어든 폭은?', 'o': ['약 153', '약 805', '약 410'], 'a': 0,
             'why': '410.3 − 257.8 = 152.5. k=2→3의 804.6보다 훨씬 작아 k=3이 팔꿈치입니다.', 'hint': '두 값을 빼 보세요.'},
            {'q': '안쪽 거리 합이 가장 작은 k를 고르면 안 되는 이유는?', 'o': ['k를 늘리면 늘 줄어들어 결국 점 개수만큼 나누게 되니까', '계산이 느려서'], 'a': 0,
             'why': '점마다 주머니 하나면 0이 됩니다. 아무것도 묶지 않은 답입니다.', 'hint': '주머니 1,554개면 어떻게 될까요?'}],
    'q23': [{'q': 'a = 0.5, b = 2.0일 때 실루엣 s는?', 'o': ['0.25', '0.75', '1.5'], 'a': 1,
             'why': '(2.0 − 0.5) ÷ 2.0 = 0.75.', 'hint': '(b − a)를 a, b 중 큰 값으로 나눕니다.'},
            {'q': '실루엣이 음수인 점은?', 'o': ['아주 잘 나뉜 점', '옆 주머니가 더 가까운, 잘못 들어간 점'], 'a': 1,
             'why': 'b < a이면 옆 주머니 친구들이 더 가깝다는 뜻입니다.', 'hint': 'b − a가 음수가 되려면?'}],
    'q24': [{'q': '계층 군집에서 주머니 수를 정하는 것은?', 'o': ['처음에 정한 k', '족보 나무를 자르는 높이'], 'a': 1,
             'why': 'k를 미리 정하지 않고, 다 합친 뒤 나무 어디서 자를지로 정합니다.', 'hint': '나무에 가로줄을 긋습니다.'},
            {'q': '{1}과 {2}를 합치는 비용(0.5)과 {1,2}와 {9}를 합치는 비용(37.5) 중 먼저 합치는 것은?', 'o': ['{1}과 {2}', '{1,2}와 {9}'], 'a': 0,
             'why': '비용이 작은 쌍부터 합칩니다.', 'hint': '흩어짐이 적게 느는 쪽.'}],
    'q25': [{'q': '체형 비율로 나눈 "납작한 주머니"에 함께 들어간 두 종은?', 'o': ['도미와 파르키', '강꼬치고기와 빙어', '농어와 로치'], 'a': 0,
             'why': '도미(높이÷길이1 약 0.50)와 파르키(약 0.48)는 생김새가 거의 같습니다.', 'hint': '높이÷길이1이 0.45를 넘는 두 종.'},
            {'q': '같은 k=3인데 원 단위 측정값 여섯 개로 나누면 이름표와의 대조 점수가 0.109로 낮다. 가장 큰 이유는?', 'o': ['k가 작아서', '무게(크기)가 거리를 정해 크기로 나뉘어서', '데이터가 적어서'], 'a': 1,
             'why': '원 단위에서는 무게가 거리를 독점해 "가벼운/중간/무거운"으로 나뉩니다.', 'hint': '1장의 표준화를 떠올려 보세요.'}],
}

JS = r'''
var D=FL.load(),X=D.X,N=D.n,SP=FL.SP,SPC=FL.SPC,SPKO=FL.SPKO,CLC=FL.CLC;
var RAT=X.map(function(r){return [r[4]/r[1],r[5]/r[1]];});var RMS=FL.meanStd(RAT),ZR=FL.standardize(RAT,RMS);
var KR=__KR__,K6=__K6__;
$$('.swatch[data-sp]').forEach(function(s){s.style.background=SPC[s.dataset.sp];});
function ratioAxes(g,W,H){return FL.axes(g,W,H,{xmin:.12,xmax:.6,ymin:.08,ymax:.24,xlab:'높이 ÷ 길이1 (납작한 정도)',ylab:'폭 ÷ 길이1 (두꺼운 정도)',padL:58});}
function zToRaw(c){return [c[0]*RMS.s[0]+RMS.m[0],c[1]*RMS.s[1]+RMS.m[1]];}
/* 이름 붙이기: 높이비 평균이 큰 순 → 납작/중간/길쭉 (k=3일 때) */
var BASE3=FL.kmeans(ZR,3,5,7);
/* 2-1 */
(function(){var cv=$('#cv21'),k=3,seed=11,C=null,lab=null,phase=0,it=0,moved=0,inertia=0,timer=null;
  function init(){C=FL.ppInit(ZR,k,seed);var a=FL.assign(ZR,C);lab=null;phase=0;it=0;moved=0;inertia=a.inertia;}
  function stepOnce(){if(lab===null){var a=FL.assign(ZR,C);lab=a.lab;inertia=a.inertia;phase=1;moved=N;return true;}
    if(phase===1){C=FL.recenter(ZR,lab,k,C);phase=2;return true;}
    var a2=FL.assign(ZR,C);moved=0;for(var i=0;i<N;i++)if(a2.lab[i]!==lab[i])moved++;lab=a2.lab;inertia=a2.inertia;it++;phase=moved?1:3;return moved>0;}
  function draw(){var f=fit(cv),g=f.c,A=ratioAxes(g,f.W,f.H);
    for(var i=0;i<N;i++)FL.dot(g,A.sx(RAT[i][0]),A.sy(RAT[i][1]),2.6,lab?CLC[lab[i]]:'#8a96a3',lab?.7:.45);
    C.forEach(function(c,j){var p=zToRaw(c),x=A.sx(p[0]),y=A.sy(p[1]);g.fillStyle='#fff';g.strokeStyle='#16212b';g.lineWidth=2;g.beginPath();g.moveTo(x,y-11);g.lineTo(x+11,y);g.lineTo(x,y+11);g.lineTo(x-11,y);g.closePath();g.fill();g.stroke();g.fillStyle=CLC[j];g.beginPath();g.arc(x,y,5,0,6.2832);g.fill();});
    stamp(g,f.W,'실제 데이터 · 다이아몬드 = 중심');}
  function info(){$$('#f21 .s').forEach(function(s){var n=+s.dataset.f;s.classList.toggle('on',n===(lab===null?0:phase));});
    FL.kpis($('#kp21'),[[k,'주머니 수 k','g'],[it,'반복한 걸음','i'],[inertia.toFixed(1),'안쪽 거리 합','a'],[phase===3?'멈춤':(lab?moved+'마리':'—'),phase===3?'상태':'이번에 주머니를 바꾼 물고기','m']]);
    var t=phase===3?'<p class="g">더는 주머니를 바꾸는 물고기가 없어 멈췄습니다. 안쪽 거리 합 '+inertia.toFixed(1)+'. "중심 다시 놓기"로 다른 시작에서 다시 해 보세요.</p>':lab===null?'<p class="a">중심 '+k+'개를 놓았습니다. 아직 물고기는 어느 주머니에도 들어가지 않았습니다(회색). "한 걸음"을 누르세요.</p>':phase===1?'<p class="m">물고기마다 가장 가까운 중심의 색으로 칠했습니다. 다음 걸음에서 중심이 평균 위치로 옮겨 갑니다.</p>':'<p class="m">중심을 주머니 평균 위치로 옮겼습니다. 다음 걸음에서 물고기들이 새 중심을 보고 주머니를 다시 고릅니다.</p>';
    $('#in21').innerHTML=t;}
  function all(){if(timer){clearInterval(timer);timer=null;}if(REDUCED){var n=0;while(phase!==3&&n++<200)stepOnce();draw();info();return;}timer=setInterval(function(){var go=stepOnce();draw();info();if(phase===3){clearInterval(timer);timer=null;}},260);}
  $('#k21').addEventListener('input',function(){k=+this.value;$('#k21v').textContent=k;init();draw();info();});
  $('#i21').addEventListener('click',function(){seed+=37;init();draw();info();});$('#s21').addEventListener('click',function(){if(phase!==3)stepOnce();draw();info();});$('#r21').addEventListener('click',all);
  init();info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-2 */
(function(){var cv=$('#cv22'),which='ratio';
  function draw(){var f=fit(cv),g=f.c,T=which==='ratio'?KR:K6,ks=[1,2,3,4,5,6,7,8];var mx=T['1'].inertia;
    var A=FL.axes(g,f.W,f.H,{xmin:.5,xmax:8.5,ymin:0,ymax:mx*1.05,xlab:'주머니 수 k',ylab:'안쪽 거리 합',xt:8,padR:46});
    ks.forEach(function(k){if(k<2)return;var s=T[k].sil,x=A.sx(k),y0=A.sy(0),h=(s/1)*(f.H-54);g.fillStyle=k===(which==='ratio'?3:2)?'rgba(30,85,200,.55)':'rgba(30,85,200,.22)';g.fillRect(x-12,y0-h,24,h);g.fillStyle='#1e55c8';g.font='12px "IBM Plex Sans KR",sans-serif';g.textAlign='center';g.fillText(s.toFixed(2),x,y0-h-4);});
    g.strokeStyle='#1f7a52';g.lineWidth=2.5;g.beginPath();ks.forEach(function(k,i){var x=A.sx(k),y=A.sy(T[k].inertia);i?g.lineTo(x,y):g.moveTo(x,y);});g.stroke();
    ks.forEach(function(k){FL.dot(g,A.sx(k),A.sy(T[k].inertia),4.5,'#1f7a52',1);});
    if(which==='ratio'){var x=A.sx(3),y=A.sy(T[3].inertia);g.strokeStyle='#c9302c';g.lineWidth=2;g.beginPath();g.arc(x,y,13,0,6.2832);g.stroke();g.fillStyle='#c9302c';g.textAlign='left';g.fillText('팔꿈치',x+16,y-8);}
    g.textAlign='right';g.fillStyle='#1e55c8';g.fillText('실루엣 0~1',f.W-4,14);stamp(g,f.W-70,'scikit-learn 값');}
  function info(){$('#in22').innerHTML=which==='ratio'?'<p class="g">체형 비율 두 개로 재면 k=2→3에서 크게 줄고(804.6), 그다음부터는 조금씩만 줄어듭니다. 실루엣도 k=3이 '+KR[3].sil.toFixed(3)+'로 가장 높습니다. 두 신호가 같은 k를 가리킵니다.</p>':'<p class="r">측정값 여섯 개로 재면 곡선이 완만하게 휘어 팔꿈치가 흐립니다. 실루엣은 k=2가 '+K6[2].sil.toFixed(3)+'로 가장 높은데, 이는 "큰 물고기와 작은 물고기" 둘로 나눈 답입니다. 같은 데이터라도 자가 달라지면 답도 달라집니다.</p>';}
  $$('#p22 [data-r]').forEach(function(bt){bt.addEventListener('click',function(){which=bt.dataset.r;$$('#p22 [data-r]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();info();});});
  info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-3 */
(function(){var cv=$('#cv23'),lab=BASE3.lab,sel=-1,A=null,meanS=null;
  var hrMean=[0,0,0],cnt=[0,0,0];for(var i=0;i<N;i++){hrMean[lab[i]]+=RAT[i][0];cnt[lab[i]]++;}
  function draw(){var f=fit(cv),g=f.c;A=ratioAxes(g,f.W,f.H);for(var i=0;i<N;i++)FL.dot(g,A.sx(RAT[i][0]),A.sy(RAT[i][1]),2.6,CLC[lab[i]],.55);
    if(sel>=0){var r=FL.silOne(ZR,lab,3,sel),x=A.sx(RAT[sel][0]),y=A.sy(RAT[sel][1]);
      [lab[sel],r.near].forEach(function(c,ci){var m=[0,0],n=0;for(var j=0;j<N;j++)if(lab[j]===c){m[0]+=RAT[j][0];m[1]+=RAT[j][1];n++;}m[0]/=n;m[1]/=n;g.setLineDash(ci?[6,4]:[]);g.strokeStyle=ci?'#c9302c':'#16212b';g.lineWidth=2;g.beginPath();g.moveTo(x,y);g.lineTo(A.sx(m[0]),A.sy(m[1]));g.stroke();g.setLineDash([]);g.fillStyle=g.strokeStyle;g.font='700 13px "IBM Plex Sans KR",sans-serif';g.fillText(ci?'b':'a',(x+A.sx(m[0]))/2+6,(y+A.sy(m[1]))/2-6);});
      g.strokeStyle='#16212b';g.lineWidth=3;g.beginPath();g.arc(x,y,8,0,6.2832);g.stroke();}
    stamp(g,f.W,'실제 데이터 · 점을 눌러 보세요');}
  function info(){if(meanS===null)meanS=FL.silhouette(ZR,lab,3);
    if(sel<0){FL.kpis($('#kp23'),[['—','a (내 주머니까지)','g'],['—','b (옆 주머니까지)','r'],['—','이 점의 실루엣 s','m'],[meanS.toFixed(3),'전체 평균 실루엣','a']]);$('#in23').innerHTML='<p class="a">점을 하나 눌러 보세요. 주머니 가운데 점과 경계 점을 번갈아 눌러 비교하면 좋습니다.</p>';return;}
    var r=FL.silOne(ZR,lab,3,sel);FL.kpis($('#kp23'),[[r.a.toFixed(3),'a (내 주머니까지 평균 거리)','g'],[r.b.toFixed(3),'b (가장 가까운 옆 주머니까지)','r'],[r.s.toFixed(3),'이 점의 실루엣 s','m'],[meanS.toFixed(3),'전체 평균 실루엣','a']]);
    $('#in23').innerHTML='<p class="'+(r.s>.5?'g':r.s>0?'a':'r')+'">s = ('+r.b.toFixed(3)+' − '+r.a.toFixed(3)+') ÷ '+Math.max(r.a,r.b).toFixed(3)+' = <b>'+r.s.toFixed(3)+'</b>. '+(r.s>.5?'자기 주머니 한가운데에 있는 물고기입니다.':r.s>0?'두 주머니 경계 가까이에 있습니다. 어느 쪽에 넣을지 애매한 물고기입니다.':'옆 주머니가 더 가깝습니다. 잘못 들어간 물고기입니다.')+' (이 물고기의 이름표: '+SPKO[D.sp[sel]]+')</p>';}
  cv.addEventListener('pointerdown',function(e){if(!A)return;var r=cv.getBoundingClientRect(),px=e.clientX-r.left,py=e.clientY-r.top,b=-1,bd=1e9;for(var i=0;i<N;i++){var dx=A.sx(RAT[i][0])-px,dy=A.sy(RAT[i][1])-py,d=dx*dx+dy*dy;if(d<bd){bd=d;b=i;}}if(bd<400){sel=b;draw();info();}});
  setTimeout(info,50);Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-4 계층 군집 (워드, 원본 158마리) */
(function(){var cv=$('#cv24'),idx=[];for(var i=0;i<N;i++)if(D.orig[i])idx.push(i);var n=idx.length;
  var R2=idx.map(function(i){return RAT[i];}),ms=FL.meanStd(R2),Zo=FL.standardize(R2,ms);
  /* 워드 합치기 (중심·크기로 비용 계산) */
  var cl=Zo.map(function(z,i){return {c:z.slice(),n:1,members:[i],id:i};}),merges=[],nextId=n;
  while(cl.length>1){var bi=0,bj=1,bc=Infinity;for(var a=0;a<cl.length;a++)for(var b2=a+1;b2<cl.length;b2++){var A1=cl[a],B1=cl[b2],cost=A1.n*B1.n/(A1.n+B1.n)*FL.d2(A1.c,B1.c);if(cost<bc){bc=cost;bi=a;bj=b2;}}
    var P=cl[bi],Q=cl[bj],nn=P.n+Q.n,c=P.c.map(function(v,k){return (v*P.n+Q.c[k]*Q.n)/nn;});merges.push({a:P.id,b:Q.id,h:Math.sqrt(2*bc),size:nn});
    var M={c:c,n:nn,members:P.members.concat(Q.members),id:nextId++};cl.splice(bj,1);cl.splice(bi,1,M);}
  /* 잎 순서 */
  var kids={};merges.forEach(function(m,t){kids[n+t]=[m.a,m.b];});function leaves(id){return id<n?[id]:leaves(kids[id][0]).concat(leaves(kids[id][1]));}
  var order=leaves(nextId-1),pos={};order.forEach(function(l,i){pos[l]=i;});var hmax=merges[merges.length-1].h;
  function cut(k){var lab=new Array(n).fill(-1),roots=[nextId-1];while(roots.length<k){roots.sort(function(a,b){return (b<n?0:merges[b-n].h)-(a<n?0:merges[a-n].h);});var r=roots.shift();roots.push(kids[r][0],kids[r][1]);}
    roots.forEach(function(r,ci){leaves(r).forEach(function(l){lab[l]=ci;});});var hcut=(merges[n-1-k].h+merges[n-k].h)/2;
    /* 색을 높이비 평균이 큰 순으로 */
    var mh=roots.map(function(r,ci){var s=0,c2=0;for(var i=0;i<n;i++)if(lab[i]===ci){s+=R2[i][0];c2++;}return s/c2;});var rk=mh.map(function(v,i){return i;}).sort(function(a,b){return mh[b]-mh[a];});var remap={};rk.forEach(function(o,i){remap[o]=i;});
    return {lab:lab.map(function(l){return remap[l];}),h:hcut};}
  var k=3,showLab=false;
  function draw(){var f=fit(cv),g=f.c,L=40,R=16,T=16,B=46;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var res=cut(k);
    function xOf(id){if(id<n)return L+(pos[id]+.5)/n*(f.W-L-R);var m=merges[id-n];return (xOf(m.a)+xOf(m.b))/2;}
    function yOf(id){return id<n?f.H-B:f.H-B-(merges[id-n].h/hmax)*(f.H-B-T);}
    var xs={};function X2(id){if(xs[id]===undefined)xs[id]=xOf(id);return xs[id];}
    merges.forEach(function(m,t){var id=n+t,y=yOf(id),xa=X2(m.a),xb=X2(m.b);var la=leaves(id),c0=res.lab[la[0]],same=la.every(function(l){return res.lab[l]===c0;});
      g.strokeStyle=same?CLC[c0]:'#8a96a3';g.lineWidth=same?1.6:1.2;g.beginPath();g.moveTo(xa,yOf(m.a));g.lineTo(xa,y);g.lineTo(xb,y);g.lineTo(xb,yOf(m.b));g.stroke();});
    var yc=f.H-B-(res.h/hmax)*(f.H-B-T);g.setLineDash([7,5]);g.strokeStyle='#c9302c';g.lineWidth=2;g.beginPath();g.moveTo(L,yc);g.lineTo(f.W-R,yc);g.stroke();g.setLineDash([]);
    g.fillStyle='#c9302c';g.font='700 12px "IBM Plex Sans KR",sans-serif';g.fillText('여기서 자르기',L+4,yc-6);
    for(var i=0;i<n;i++){var x=L+(pos[i]+.5)/n*(f.W-L-R);g.fillStyle=showLab?SPC[D.sp[idx[i]]]:CLC[res.lab[i]];g.fillRect(x-2,f.H-B+4,4,showLab?16:8);}
    g.fillStyle='#5b6874';g.font='12px "IBM Plex Sans KR",sans-serif';g.fillText(showLab?'아래 색: 덮어 둔 종 이름표':'아래 색: 자른 주머니',L,f.H-8);
    g.save();g.translate(13,(T+f.H-B)/2);g.rotate(-Math.PI/2);g.textAlign='center';g.fillText('합칠 때 늘어난 흩어짐',0,0);g.restore();stamp(g,f.W,'원본 158마리 · 직접 계산');
    var sp=idx.map(function(i){return D.sp[i];});var a=FL.ari(sp,res.lab);var sizes=[];for(var c=0;c<k;c++)sizes.push(res.lab.filter(function(l){return l===c;}).length);
    FL.kpis($('#kp24'),[[k,'주머니 수','g'],[sizes.join(' · '),'주머니별 물고기 수','i'],[res.h.toFixed(2),'자른 높이','a'],[a.toFixed(3),'이름표와의 대조 점수 (채점용)','m']]);
    $('#in24').innerHTML='<p class="'+(k===3?'g':'a')+'">'+(k===3?'세 갈래로 자르면 가지가 가장 길게 남습니다. 그 위로는 한참 올라가야 다시 합쳐집니다. 원본 158마리로 다시 계산해도 이름표와의 대조 점수가 '+a.toFixed(3)+'로, 1,554마리 k-평균(0.609)과 비슷합니다.':'자르는 높이를 바꾸면 주머니 수가 바뀝니다. 짧은 가지를 끊으면 주머니가 잘게 쪼개지지만, 쪼갠 주머니끼리는 서로 가까워 구분이 흐립니다.')+'</p>';}
  $('#k24').addEventListener('input',function(){k=+this.value;$('#k24v').textContent=k;draw();});
  $('#lb24').addEventListener('click',function(){showLab=!showLab;this.setAttribute('aria-pressed',showLab?'true':'false');draw();});
  Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 2-5 */
(function(){var cv=$('#cv25'),col='cl',feat='ratio',cache={};
  function labs(){if(cache[feat])return cache[feat];var Zf=feat==='ratio'?ZR:feat==='six'?FL.standardize(X):X;var r=feat==='ratio'?BASE3:FL.kmeans(Zf,3,5,7);
    var mh=[0,0,0],cn=[0,0,0];for(var i=0;i<N;i++){mh[r.lab[i]]+=feat==='ratio'?RAT[i][0]:X[i][0];cn[r.lab[i]]++;}for(var c=0;c<3;c++)mh[c]/=cn[c];var rk=[0,1,2].sort(function(a,b){return mh[b]-mh[a];}),remap={};rk.forEach(function(o,i){remap[o]=i;});
    cache[feat]={lab:r.lab.map(function(l){return remap[l];}),ari:FL.ari(D.sp,r.lab)};return cache[feat];}
  function draw(){var f=fit(cv),g=f.c,A=ratioAxes(g,f.W,f.H),L=labs();for(var i=0;i<N;i++)FL.dot(g,A.sx(RAT[i][0]),A.sy(RAT[i][1]),2.6,col==='sp'?SPC[D.sp[i]]:CLC[L.lab[i]],.65);stamp(g,f.W,col==='sp'?'실제 데이터 · 종 이름표 색':'실제 데이터 · 주머니 색');}
  function info(){var L=labs();if(col==='sp')FL.spLegend($('#lg25'));else FL.legend($('#lg25'),feat==='ratio'?[['납작한 주머니',CLC[0]],['중간 주머니',CLC[1]],['길쭉한 주머니',CLC[2]]]:[['무거운 쪽 주머니',CLC[0]],['중간 주머니',CLC[1]],['가벼운 쪽 주머니',CLC[2]]]);
    var nm={ratio:'체형 비율 2개',six:'측정값 6개 (표준화)',raw:'측정값 6개 (원 단위)'}[feat];
    FL.kpis($('#kp25'),[[nm,'자','i'],['3','주머니 수','g'],[L.ari.toFixed(3),'이름표와의 대조 점수','m'],[feat==='ratio'?'생김새':'크기','주머니를 가른 기준','a']]);
    $('#in25').innerHTML=feat==='ratio'?'<p class="g">체형 평면에서 주머니 색과 종 색을 번갈아 보세요. 납작한 주머니는 도미·파르키, 길쭉한 주머니는 강꼬치고기·빙어와 거의 겹칩니다.</p>':'<p class="r">같은 k=3이지만 '+nm+'로 나누면 체형 평면 위에서 색이 뒤섞입니다. 주머니가 생김새가 아니라 크기(무게)로 갈렸기 때문입니다. 대조 점수가 '+L.ari.toFixed(3)+'로 떨어집니다.</p>';}
  $$('#p25 [data-c]').forEach(function(bt){bt.addEventListener('click',function(){col=bt.dataset.c;$$('#p25 [data-c]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();info();});});
  $$('#p25 [data-f]').forEach(function(bt){bt.addEventListener('click',function(){feat=bt.dataset.f;$$('#p25 [data-f]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();info();});});
  info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
Duel({el:'#d2',run:function(){var r7=FL.kmeans(ZR,7,5,7);var s3=FL.silhouette(ZR,BASE3.lab,3),s7=FL.silhouette(ZR,r7.lab,7);window._d2={a3:FL.ari(D.sp,BASE3.lab),a7:FL.ari(D.sp,r7.lab)};return {fly:s3,robo:s7};},
  fmt:function(v){return v.toFixed(3);},scale:1,bigGap:.1,
  report:function(r){return '평균 실루엣은 초파리 쪽(주머니 3개) '+r.fly.toFixed(3)+', 주판봇 쪽(주머니 7개) '+r.robo.toFixed(3)+'이에요. 덤으로 이름표와 대조해 보니 '+window._d2.a3.toFixed(3)+' 대 '+window._d2.a7.toFixed(3)+'로, 일곱 개로 나눠도 종을 더 잘 맞히지 않았어요.';},
  verdict:{fly:'주머니 수는 데이터의 모양이 정한다. 종의 수가 아니다. 초파리 승.',robo:'이번에는 일곱 주머니가 더 또렷했다. 주판봇 승.',draw:'두 나누기가 비슷하다. 이번 판은 나눠 갖는다.'}});
'''.replace('__KR__', json.dumps(kr)).replace('__K6__', json.dumps(k6))


def main():
    USED.update(['fly_arms', 'fly_coffee', 'fly_cry', 'robo_sigh', 'robo_happy', 'robo_meh', 'fly_point', 'robo_coin'])
    hero_html = hero('2장 · 비지도학습 물고기 연구실', '묶기 — 군집화', '이름표 없이, 어떤 물고기끼리 같은 주머니에 담을까?',
                     '1장에서 "닮음"을 거리로 재는 법을 배웠습니다. 이제 그 거리로 1,554마리를 주머니(군집) 몇 개에 나눠 담습니다. '
                     '<b>k-평균</b>으로 담고, <b>엘보</b>와 <b>실루엣</b>으로 주머니 수를 고르고, <b>계층 군집</b>으로 다른 담는 법을 본 뒤, 마지막에야 덮어 둔 종 이름표와 대조합니다.',
                     [('3', '체형 비율로 찾은 주머니 수 (엘보·실루엣)', 'g'), (num(kr['3']['sil'], 3), 'k=3의 평균 실루엣 (체형 비율)', 'i'),
                      (num(kr['3']['ari'], 3), '주머니와 종 이름표의 대조 점수', 'm'), (num(R['raw_k3_ari'], 3), '원 단위 그대로 나눴을 때의 대조 점수', 'r')],
                     [('doc', 'front', '오늘은 물고기를 주머니에 담습니다. 몇 개의 주머니에 담을지도 데이터에게 물어볼 거예요.'),
                      ('asst', 'smile', '종이 일곱이니까 주머니도 일곱 개 아니에요?'),
                      ('fly', 'point', '종 이름은 덮었잖아. 데이터가 몇 갈래로 보이는지부터 재자.'),
                      ('robo', 'coin', '주머니는 많을수록 정확하지! 2장은 내가 이긴다.')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a> 증강본'),
                 ('원자료', '안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 PART 1 군집화 (2026)'),
                 ('엘보·실루엣·대조 점수', 'code/analysis.py (scikit-learn 1.9.1, KMeans n_init=10, random_state=42)'),
                 ('k-평균', 'Lloyd, S. (1982). Least squares quantization in PCM. IEEE Transactions on Information Theory, 28(2), 129–137'),
                 ('실루엣', 'Rousseeuw, P. J. (1987). Silhouettes. Journal of Computational and Applied Mathematics, 20, 53–65'),
                 ('워드 연결', 'Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. JASA, 58(301), 236–244')],
                ['2-1·2-3·대결의 k-평균은 이 페이지가 직접 계산(k-means++ 시작, 5번 중 최선) — scikit-learn 값과 소수 셋째 자리에서 다를 수 있음', '2-4의 족보 나무는 원본 158마리로 직접 계산', '수식 상자의 수직선 점 1, 2, 9는 예시값'],
                prev=('01_no_answer_key.html', '1장 · 정답표 없이 배운다'), nxt=('03_folding.html', '3장 · 접기 — 차원 축소'))
    return build(P, title='2장 · 묶기 — 군집화 · 비지도학습 물고기 연구실',
                 desc='물고기 1,554마리를 k-평균과 계층 군집으로 주머니에 나눠 담고, 엘보와 실루엣으로 주머니 수를 고른 뒤 종 이름표와 대조한다.',
                 nav=[('#first', '3줄'), ('#s1', '2-1 k-평균'), ('#s2', '2-2 엘보'), ('#s3', '2-3 실루엣'), ('#s4', '2-4 계층'), ('#s5', '2-5 결과'), ('#duel', '대결'), ('#sum', '정리')],
                 cover_html=cover('cover_02', '2장 · 묶기', '묶기 — 군집화'), hero=hero_html, body=b, gloss=GLOSS, quizzes=QUIZ, page_js=JS, og='og_02')


if __name__ == '__main__':
    print(main())
