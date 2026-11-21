# -*- coding: utf-8 -*-
"""4장 · 맞히기 — 자기지도학습 (가린 무게, 오토인코더, 이웃 찾기, 배운 범위 밖)"""
from lib import *

P = '04_guessing.html'
mw = R['mask_weight']; av = R['ae_vs_pca']; km = R['knn_map']; od = R['ood']; sp_ = R['supervised']; sp_split = R['split']; o4 = R['pca4_ood']


def body():
    b = three([
        ('무엇을', '측정값 일부를 가리고 나머지로 맞히게 해서, 사람이 만든 정답표 없이 데이터 자신을 선생님으로 삼는 자기지도학습을 봅니다.'),
        ('왜 중요한가', '대형 언어 모델과 이미지 모델이 이 방식으로 배웁니다. 그리고 "배운 범위 밖에서는 모른다고 말하기"는 모든 AI를 현장에 쓸 때의 안전장치입니다.'),
        ('업무에서는', '빠진 측정값 채우기, 이상한 기록 찾기(복원이 잘 안 되는 기록), 처음 보는 데이터 걸러내기에 씁니다.')],
        '코드·수식을 몰라도 됩니다. 이 장의 채점은 모두 학습에 쓰지 않은 물고기(원본 32마리에서 늘린 %d마리)로 합니다.' % sp_split['test'],
        [('AE', 'Autoencoder, 오토인코더 (접었다 펴는 신경망)'), ('k-NN', 'k-Nearest Neighbors, 가장 가까운 이웃 k개'), ('OOD', 'Out-of-Distribution, 배운 범위 밖 데이터')])
    b += section('map', '큰 그림 — 접은 지도로 맞히고, 판단한다',
                 '<div class="mapbar"><span>1장 · 거리·표준화</span><i>→</i><span>2장 · 묶기</span><i>→</i><span>3장 · 접기</span><i>→</i><span class="on">4장 · 맞히기</span><i>→</i><span>실전 연습장</span></div>'
                 + say('sia', 'explain', '순서대로 말씀드릴게요. 4-1 가린 무게 맞히기, 4-2 곡선으로 접는 오토인코더, 4-3 지도 위 이웃 찾기, 4-4 배운 범위 밖 알아차리기입니다.')
                 + '<p>이 장부터는 <b>학습용과 시험용</b>을 나눕니다. 지도학습 시리즈와 같은 원칙으로, 같은 원본에서 늘린 물고기는 한쪽에만 둡니다. '
                 '학습용은 원본 %d마리에서 늘린 %s마리, 시험용은 원본 %d마리에서 늘린 %d마리입니다.</p>' % (sp_split['train_groups'], num(sp_split['train']), sp_split['test_groups'], sp_split['test']))

    # 4-1
    s = say('doc', 'think', '상황 하나. 어시장 저울이 고장 나서 오늘 들어온 물고기의 무게를 못 쟀습니다. 자로 잰 길이·높이·폭은 있습니다. 무게를 짐작할 수 있을까요?')
    c = mw['coef']; f = [2 ** v for v in c]
    s += recap('거듭제곱과 로그', '<p>거듭제곱 2³은 2를 세 번 곱한 수(8)입니다. 지수가 소수여도 뜻은 같습니다. "길이가 2배가 되면 그 부분이 몇 배가 되나"로 읽으면 됩니다. '
               '로그는 거듭제곱을 거꾸로 푸는 도구라서, 곱셈으로 얽힌 관계를 덧셈(직선)으로 바꿔 줍니다. 이 단계의 모델은 그래서 "로그를 씌워 직선으로 맞춘" 것입니다.</p>'
               '<div class="tw"><table class="tb mini-table"><tr><th>무엇을 2배로</th><th class="n">무게는</th><th>읽는 법</th></tr>'
               '<tr><td>길이1만</td><td class="n">약 %s배</td><td>2의 %s제곱</td></tr><tr><td>높이만</td><td class="n">약 %s배</td><td>2의 %s제곱</td></tr>'
               '<tr><td>폭만</td><td class="n">약 %s배</td><td>2의 %s제곱</td></tr><tr><td><b>셋 다</b></td><td class="n"><b>약 %s배</b></td><td>2 × 2 × 2 = 8에 가까움 (부피처럼)</td></tr></table></div>' % (
                   num(f[0], 2), num(c[0], 3), num(f[1], 2), num(c[1], 3), num(f[2], 2), num(c[2], 3), num(f[0] * f[1] * f[2], 2)))
    s += duo(why([('문제 상황', '무게라는 값 하나가 빠졌습니다. 정답표를 붙여 줄 사람도 없습니다.'),
                  ('앞 방법의 한계', '군집·접기는 "모양"을 보여 줄 뿐, 빠진 값을 채워 주지는 않습니다.'),
                  ('해법', '이미 잰 물고기들에서 무게를 일부러 가리고, 길이·높이·폭으로 맞히는 연습을 시킵니다. 가린 무게가 곧 정답이라 사람이 정답을 만들 필요가 없습니다(마스크드 모델링).')],
                 '단어 공란 채우기 문제집은 원래 문장에서 단어를 가려 만듭니다. 정답은 원래 문장에 이미 있습니다.'),
             mathbox('무게 = 상수 × 길이<sup>1.36</sup>…? 지수가 소수예요!', '지수법칙과 거듭제곱(중학교 2학년·고등학교) — 부피는 길이 × 높이 × 폭',
                     '무게 ≈ %s × 길이1<sup>%s</sup> × 높이<sup>%s</sup> × 폭<sup>%s</sup>' % (num(2.718281828 ** mw['intercept'], 3), num(mw['coef'][0], 3), num(mw['coef'][1], 3), num(mw['coef'][2], 3)),
                     [('길이1<sup>1.364</sup>', '길이1의 1.364제곱', '길이가 2배면 이 부분은 약 2.6배'), ('지수 합', '', '%s + %s + %s = %s ≈ 3' % (num(mw['coef'][0], 3), num(mw['coef'][1], 3), num(mw['coef'][2], 3), num(sum(mw['coef']), 3)))],
                     '원자료의 예(길이1 31.2cm, 높이 12.5cm, 폭 4.3cm)를 넣으면 약 <b>%sg</b>입니다. 세 지수를 더하면 약 3, 즉 무게가 "길이 × 높이 × 폭"(부피)처럼 자란다는 것을 데이터가 스스로 찾았습니다.' % num(mw['example']),
                     '정답표 없이 가린 무게만으로 배웠는데, 부피 공식 같은 게 나왔어요!'))
    s += sup('정답(종 이름)은 사람이 붙인 것이었습니다. 이름표가 없는 물고기로는 배울 수 없었습니다.',
             '정답(가린 무게)은 데이터 안에 원래 있던 값입니다. 측정값만 있으면 얼마든지 문제를 만들 수 있습니다. 질문도 정답도 데이터가 만듭니다.')
    s += talk([('doc', 'board', '가린 무게를 얼마나 잘 맞히는지, 처음 보는 시험 물고기로 확인해 볼까요?'),
               ('robo', 'coin', '그냥 평균 무게 %sg으로 다 찍어도 반은 맞겠지!' % num(R['desc']['weight_g']['mean'])),
               ('fly', 'point', '"시험 물고기 뽑기"를 몇 번 눌러 봐. 평균으로 찍은 값하고 비교해서.'),
               ('asst', 'report', '모델은 평균 %sg 빗나가는데, 평균으로 찍으면 %sg 빗나가요. 여섯 배 넘게 차이 나요.' % (num(mw['mae_g'], 1), num(mw['baseline_mae_g'], 1)))])
    s += panel('p41', '실험 · 가린 무게 맞히기', '시험 물고기 = 학습에 쓰지 않은 묶음',
               '<div class="ctrl"><div class="group"><span class="glabel">길이1</span><input type="range" id="l41" min="7" max="64" step=".1" value="31.2" aria-label="길이1"><span class="val" id="l41v"></span></div>'
               '<div class="group"><span class="glabel">높이</span><input type="range" id="h41" min="1.5" max="20" step=".1" value="12.5" aria-label="높이"><span class="val" id="h41v"></span></div>'
               '<div class="group"><span class="glabel">폭</span><input type="range" id="w41" min=".9" max="9" step=".1" value="4.3" aria-label="폭"><span class="val" id="w41v"></span></div>'
               '<div class="group"><button class="bt primary" id="t41">시험 물고기 뽑기</button><button class="bt" id="r41">가린 무게 보기</button></div></div>'
               + canvas('cv41', 300, '시험 물고기들의 실제 무게(가로)와 맞힌 무게(세로)') +
               '<section class="kpis" id="kp41" aria-label="숫자 요약"></section><div class="insight" id="in41" aria-live="polite"></div>', real=True)
    s += explain(['학습용 물고기마다 무게를 가리고, 길이1·높이·폭으로 무게를 맞히는 규칙을 찾았습니다(로그를 씌운 직선 맞추기).',
                  '시험 물고기 %d마리에서 평균 %sg, 비율로는 중앙값 %s 빗나갑니다. 평균 무게로 찍으면 %sg 빗나갑니다.' % (sp_split['test'], num(mw['mae_g'], 1), pct(mw['median_ape']), num(mw['baseline_mae_g'], 1)),
                  '그래프에서 점이 대각선에 붙어 있을수록 잘 맞힌 것입니다. 정답은 사람이 아니라 가려 둔 원래 무게였습니다.'],
                 '맞히는 규칙은 길이·높이·폭과 무게 사이의 관계만 배웠습니다. 속이 빈 물고기, 알을 밴 물고기처럼 관계가 다른 물고기는 틀립니다. 자기지도로 배운 것도 데이터에 있던 관계까지만입니다.')
    s += codefold([('LinearRegression().fit(np.log(X[["길이1","높이","폭"]]), np.log(무게))', '로그를 씌우면 거듭제곱 관계가 직선이 되어 쉽게 맞춥니다'),
                   ('np.exp(model.predict(...))', '로그를 다시 풀어 그램 단위 무게로 바꿉니다')])
    s += quiz('q41')
    b += step('s1', '4-1', '가린 절반을 맞혀라 — 마스크드 모델링', ['방법: 가리고 맞히기(자기지도)', '일상: 공란 채우기 문제'], s)

    # 4-2
    s = say('doc', 'think', '3장에서 접었다 펴는 PCA는 무게를 많이 틀렸습니다. 곡선으로 휘어 접을 수 있는 "접었다 펴는 상자"가 있다면 어떨까요?')
    s += duo(why([('문제 상황', '두 숫자로 접었다 펴면 무게가 많이 틀립니다(3-5).'),
                  ('앞 방법의 한계', 'PCA는 곧은 방향으로만 접습니다. 무게처럼 길이에 휘어서 따라가는 관계를 곧은 접기로는 다 담지 못합니다.'),
                  ('해법', '신경망으로 "여섯 값 → 두 숫자(메모) → 여섯 값"을 지나며 원래 값을 되살리도록 훈련합니다. 접는 방향까지 곡선으로 스스로 찾습니다(오토인코더).')],
                 '긴 이야기를 쪽지 두 줄로 줄여 친구에게 넘기고, 친구가 쪽지만 보고 이야기를 다시 들려주는 놀이입니다. 쪽지가 좁을수록 핵심만 남겨야 합니다.'),
             mathbox('인코더, 디코더, 병목… 상자가 몇 개예요?', '합성함수(고등학교) — 접는 함수 뒤에 펴는 함수를 이어 붙이기',
                     '복원 = 디코더( 인코더( 원래 여섯 값 ) )',
                     [('인코더', '접기', '여섯 값을 숫자 두 개(메모)로 줄이는 함수'), ('병목', '보틀넥', '가운데의 좁은 자리. 여기서는 숫자 2개'),
                      ('디코더', '펴기', '메모 두 개로 여섯 값을 다시 그리는 함수'), ('복원 오차', '', '원래 값과 다시 그린 값의 차이. 이것을 줄이도록 배움')],
                     'f(x) = 2x로 접고 g(y) = y ÷ 2로 펴면 g(f(3)) = 3으로 그대로 돌아옵니다. 그런데 여섯 값을 두 값으로 줄이면 다 담을 수 없으니, 무엇을 남길지 배워야 합니다. '
                     '시험 물고기 복원 오차는 오토인코더 <b>%s</b>, PCA <b>%s</b>입니다.' % (num(av['ae_test_mse'], 4), num(av['pca2_test_mse'], 4)),
                     '정답표 대신 "나 자신을 잘 되살리기"가 목표군요. 그래서 이것도 정답표 없이 배우는 거고요.'))
    s += note('원자료 슬라이드는 "물고기 데이터처럼 대개 직선으로 접히면 PCA면 충분하다"고 적었습니다. 같은 1,554마리로 재 보니 오토인코더(6-16-2-16-6)의 시험 복원 오차가 %s, PCA(두 축)가 %s로 오토인코더가 약 %s배 작았습니다. '
              '무게가 길이에 곡선으로 따라가기 때문입니다. 이 페이지에서는 그 문장을 <b>"무게처럼 휜 관계가 있으면 곡선 접기(오토인코더)가 복원에 유리하다"</b>로 바꿉니다.' % (
                  num(av['ae_test_mse'], 4), num(av['pca2_test_mse'], 4), num(av['pca2_test_mse'] / av['ae_test_mse'], 1)), warn=True)
    s += sup('신경망은 정답(종 이름)을 맞히도록 배웠습니다. 마지막 층은 종 일곱 개의 확률이었습니다.',
             '같은 신경망인데 마지막 층이 "원래 여섯 값"입니다. 입력이 곧 정답이라 이름표가 필요 없습니다. 가운데 좁은 자리의 두 숫자가 새 지도 좌표가 됩니다.')
    s += talk([('doc', 'board', '곧은 접기(PCA)와 곡선 접기(오토인코더), 어느 쪽이 무게를 더 잘 되살릴까요?'),
               ('robo', 'coin', '신경망이 크고 복잡하니까 당연히 신경망이지! 큰 게 이긴다!'),
               ('fly', 'point', '크다고 늘 이기진 않아. 물고기를 바꿔 가며 "무게" 줄을 비교해 봐.'),
               ('asst', 'report', '큰 물고기에서 PCA는 수백 g 틀리는데 오토인코더는 수십 g이에요. 변수별로 봐도 무게 오차가 %s 대 %s예요.' % (num(av['pca_var'][0], 3), num(av['ae_var'][0], 3)))])
    s += panel('p42', '실험 · 접었다 펴는 상자 두 개', '시험 물고기 · 학습한 가중치로 이 페이지가 직접 계산',
               '<div class="ctrl"><div class="group"><span class="glabel">시험 물고기</span><input type="range" id="f42" min="0" max="0" value="0" aria-label="시험 물고기 고르기"><span class="val" id="f42v"></span></div></div>'
               + canvas('cv42', 230, '오토인코더 구조: 여섯 값, 16, 2, 16, 여섯 값') + canvas('cv42b', 250, '고른 물고기의 원래 값과 두 방법으로 다시 편 값') +
               '<div class="legend"><span><i style="background:rgba(31,122,82,.35)"></i>원래 값</span><span><i style="background:#1e55c8"></i>PCA로 다시 편 값</span><span><i style="background:#c9302c"></i>오토인코더로 다시 편 값</span></div>'
               '<div class="tw"><table class="tb mini-table" id="t42"></table></div><section class="kpis" id="kp42" aria-label="숫자 요약"></section><div class="insight" id="in42" aria-live="polite"></div>', real=True)
    s += explain(['인코더는 여섯 값을 16개로 넓혔다가 2개(병목)로 좁힙니다. 디코더는 2개를 16개로 넓혔다가 여섯 값으로 되돌립니다.',
                  '가운데를 넓게 두면 모든 정보를 그대로 실어 나르기만 해서 아무것도 배우지 않습니다. 좁혀야 중요한 것만 남기는 법을 배웁니다.',
                  '너무 좁으면 종을 가르는 정보까지 버리고, 너무 넓으면 압축이 안 됩니다. 넓이는 사람이 정하는 설계 결정입니다.'],
                 '오토인코더의 두 숫자는 PCA처럼 "크기 축·체형 축"이라는 이름이 바로 붙지 않습니다. 복원은 더 잘하지만 해석은 더 어렵습니다. 학습에도 시간이 들고, 시작값에 따라 결과가 조금씩 다릅니다.')
    s += codefold([('MLPRegressor(hidden_layer_sizes=(16, 2, 16), activation="tanh")', '6 → 16 → 2 → 16 → 6 모양의 신경망'),
                   ('ae.fit(Z_train, Z_train)', '입력과 정답에 같은 데이터를 줍니다. 이것이 "자기 자신을 되살리기"'),
                   ('((ae.predict(Z_test) - Z_test) ** 2).mean()', '시험 물고기의 복원 오차')])
    s += quiz('q42')
    b += step('s2', '4-2', '접었다 펴는 상자 — 오토인코더와 병목', ['방법: 오토인코더', '일상: 쪽지 두 줄로 이야기 전하기'], s)

    # 4-3
    s = say('doc', 'think', '새 물고기가 들어왔는데 종을 말해 줄 사람이 없습니다. 지도 위에서 가장 가까운 이웃이 누구였는지 보면 짐작할 수 있지 않을까요?')
    s += duo(why([('문제 상황', '새 물고기의 종을 알고 싶은데, 학습할 때는 이름표를 쓰지 않았습니다.'),
                  ('앞 방법의 한계', '지도와 주머니는 "누구와 닮았나"까지만 알려 주고, 이름은 알려 주지 않습니다.'),
                  ('해법', '이름표는 판단할 때만 참고합니다. 지도 위에서 새 물고기의 가장 가까운 이웃 k마리를 찾고, 그 이웃들의 이름표로 다수결합니다.')],
                 '이사 온 동네에서 길을 물을 때, 가장 가까운 집 다섯 곳에 물어보고 가장 많이 나온 답을 따르는 것과 같습니다.'),
             mathbox('다수결인데 "확신"은 어떻게 숫자로 말해요?', '비율(초등 6학년) — 이웃 중 같은 답의 몫',
                     '확신 = 가장 많은 답을 한 이웃 수 ÷ k',
                     [('k', '케이', '물어볼 이웃 수 (여기서는 5)'), ('다수결', '', '가장 많이 나온 이름표'), ('확신', '', '그 이름표의 몫. 5마리 중 3마리면 60%')],
                     '이웃 다섯이 빙어·빙어·빙어·강꼬치고기·빙어면 답은 빙어, 확신은 4 ÷ 5 = <b>80%</b>. 셋·둘로 갈리면 60%로, 경계에 선 물고기입니다.',
                     '이웃이 한목소리면 믿고, 갈리면 조심하면 되겠네요.'))
    s += sup('KNN은 이름표 붙은 학습 물고기 전부를 이웃 후보로 두고, 측정값 여섯 개(표준화)의 거리로 이웃을 찾았습니다. 물고기 단위 교차검증 정답률 %s였습니다.' % pct(sp_['knn1_group_cv']),
             '이름표 없이 그린 두 축 지도 위에서 이웃을 찾습니다. 이름표는 투표할 때만 봅니다. 시험 정답률은 %s입니다. 지도가 요약이라 조금 낮습니다.' % pct(km['pc2_k5_test_acc']))
    s += talk([('doc', 'think', '만약 이름표가 종마다 딱 한 장(7장)만 있다면, 이웃 찾기가 얼마나 될까요?'),
               ('robo', 'coin', '일곱 장이면 찍는 거나 마찬가지지. 7분의 1, 14%!'),
               ('fly', 'point', '"이름표 7장만" 버튼을 눌러서 정답률을 직접 봐.'),
               ('asst', 'report', '이름표 7장만으로도 찍기(14%)의 세 배쯤 나와요. 지도가 닮은 물고기를 이미 모아 놨기 때문이에요.')])
    s += panel('p43', '실험 · 지도 위에서 이웃에게 묻기', '학습용으로 그린 지도 · 시험 물고기로 채점',
               '<div class="ctrl"><div class="group"><span class="glabel">이름표 붙은 이웃 후보</span><button class="bt" data-l="all" aria-pressed="true">학습 물고기 전부</button><button class="bt" data-l="seven" aria-pressed="false">이름표 7장만 (종마다 1장)</button></div>'
               '<div class="group"><span class="glabel">시험 물고기</span><input type="range" id="f43" min="0" max="0" value="0" aria-label="시험 물고기 고르기"><span class="val" id="f43v"></span></div></div>'
               + canvas('cv43', 380, '두 축 물고기 지도 위 시험 물고기와 가장 가까운 이웃들') +
               '<section class="kpis" id="kp43" aria-label="숫자 요약"></section><div class="insight" id="in43" aria-live="polite"></div>', real=True)
    s += explain(['지도는 학습 물고기로만 그렸습니다(이름표 없이). 시험 물고기도 같은 방향으로 접어 지도 위에 놓습니다.',
                  '이웃 5마리의 이름표로 다수결합니다. 시험 물고기 %d마리 정답률은 두 축 지도에서 %s, 접지 않은 여섯 값에서 %s입니다.' % (sp_split['test'], pct(km['pc2_k5_test_acc']), pct(km['all6_k5_test_acc'])),
                  '이름표 7장만 있을 때도 지도 덕분에 찍기보다 훨씬 낫습니다. 모델이 배운 것은 이름이 아니라 지도 위의 거리입니다.'],
                 '이 방법은 지도의 품질에 전적으로 기댑니다. 지도가 좋으면 이웃도 좋고, 지도가 나쁘면 이웃도 엉뚱합니다. 그리고 이웃이 아무리 멀어도 다수결은 늘 답을 냅니다(다음 단계).')
    s += codefold([('KNeighborsClassifier(5).fit(S_train, y_train)', '지도 좌표와 이름표로 이웃 다섯 마리 투표를 준비합니다'),
                   ('knn.predict(S_test)', '시험 물고기마다 다수결 답')])
    s += quiz('q43')
    b += step('s3', '4-3', '이름표 없이 알아보기 — 지도 위 이웃 찾기', ['방법: 이웃 찾기(k-NN)', '일상: 이웃집에 길 묻기'], s)

    # 4-4
    s = say('doc', 'think', '이 지도는 길이 7~64cm 물고기로 그렸습니다. 1m가 넘는 커다란 물고기가 들어오면, 이웃 찾기는 뭐라고 답할까요?')
    s += duo(why([('문제 상황', '이웃 찾기와 다수결은 이웃이 아무리 멀어도 늘 답을 냅니다. 처음 보는 물고기에도 자신 있게 틀립니다.'),
                  ('앞 방법의 한계', '답만 보고는 그 답이 배운 범위 안에서 나왔는지 알 수 없습니다.'),
                  ('해법', '두 가지를 잽니다. ① 지도 위 기존 구름에서 얼마나 떨어졌나(지도 거리). ② 네 축으로 접었다 폈을 때 원래대로 돌아오나(복원 오차). 둘 중 하나라도 학습 물고기보다 훨씬 크면 "배운 범위 밖"으로 표시하고 답을 보류합니다.')],
                 '동네 길은 잘 알아도, 처음 가는 도시에서는 "잘 모르겠어요"라고 말하는 것이 정직한 길 안내입니다.'),
             mathbox('"훨씬 멀다"의 기준은 누가 정해요?', '백분위수(고등학교 통계) — 학습 데이터 거리 중 상위 1% 지점을 문턱으로',
                     '경보 = (지도 거리 > 거리 문턱) 또는 (복원 오차 > 복원 문턱)',
                     [('거리 문턱', '', '학습 물고기끼리 잰 지도 위 이웃 거리의 상위 1%% 지점. 여기서는 %s' % num(od['thr_q99'], 3)), ('복원 문턱', '', '학습 물고기를 네 축으로 접었다 편 오차의 상위 1%% 지점. 여기서는 %s' % num(o4['thr_q99'], 5)), ('또는', '', '둘 중 하나만 넘어도 경보')],
                     '길이1 1m·무게 9kg인 가상의 물고기는 지도 위 가장 가까운 학습 물고기까지 거리가 %s입니다. %s ÷ %s ≈ <b>%s배</b>, 문턱을 한참 넘습니다.' % (
                         num(od['big_fish']['nn_dist'], 2), num(od['big_fish']['nn_dist'], 2), num(od['thr_q99'], 3), num(od['big_fish']['times_thr'], 1)),
                     '자 하나로는 빈틈이 생기니까, 자 두 개로 재는 거군요.'))
    s += sup('시험 정답률이 높으면 믿었습니다. 하지만 시험 물고기도 같은 어시장에서 잰 물고기였습니다.',
             '답과 함께 "그 답이 배운 범위 안에서 나왔나"를 늘 같이 봅니다. 범위 확인이 없으면 답은 운입니다.')
    s += talk([('doc', 'board', '배운 범위 밖의 물고기를 넣어 볼까요?'),
               ('robo', 'coin', '이웃이 있잖아. 어떤 물고기든 답은 나와. 답이 나오면 된 거지!'),
               ('fly', 'point', '"1m 큰 물고기"와 "다른 바다 물고기"를 눌러 봐. 답은 나오는데, 두 자로 재면?'),
               ('asst', 'report', '큰 물고기는 지도 거리가 문턱의 %s배예요. 다른 바다 물고기는 지도 거리로는 문턱 안인데, 복원 오차가 문턱의 %s배라 경보가 떠요.' % (num(od['big_fish']['times_thr'], 0), num(o4['sea_times'], 0)))])
    s += panel('p44', '실험 · 배운 범위 밖 알아차리기', '문턱: 학습 물고기 이웃 거리 상위 1%',
               '<div class="ctrl"><div class="group"><span class="glabel">물고기 고르기</span><button class="bt" data-p="perch" aria-pressed="true">보통 농어</button>'
               '<button class="bt" data-p="big" aria-pressed="false">1m 큰 물고기</button><button class="bt" data-p="sea" aria-pressed="false">다른 바다 (길이를 다르게 잰 물고기)</button></div></div>'
               '<div class="ctrl"><div class="group"><span class="glabel">길이1 배율</span><input type="range" id="s44" min="0.8" max="1.3" step="0.01" value="1" aria-label="길이1 배율"><span class="val" id="s44v"></span></div></div>'
               + canvas('cv44', 360, '물고기 지도 위 학습 구름과 새 물고기, 가장 가까운 이웃까지의 거리') +
               '<section class="kpis" id="kp44" aria-label="숫자 요약"></section><div class="insight" id="in44" aria-live="polite"></div>', real=True)
    s += explain(['새 물고기를 학습 때와 같은 눈금(표준화)과 같은 방향(PCA)으로 접어 지도에 놓습니다. 지도 거리가 문턱(%s)을 넘으면 경보입니다. 1m 큰 물고기가 여기에 걸립니다.' % num(od['thr_q99'], 3),
                  '지도는 두 축만 남겨서, 길이 세 값의 관계처럼 버린 방향의 이상은 못 봅니다. 그래서 네 축으로 접었다 편 복원 오차도 봅니다(3-5에서 네 축이면 거의 원래대로 돌아왔지요). 길이1 항목에 다른 길이를 적은 물고기는 지도 거리는 %s로 문턱 안이지만, 복원 오차가 문턱의 %s배입니다.' % (num(R['ae_ood']['sea_perch']['map_dist'], 3), num(o4['sea_times'], 1)),
                  '정상인 시험 물고기 %d마리 중에서도 지도 거리로 %d마리, 복원 오차로 %d마리가 문턱을 넘었습니다. 학습에 없던 묶음이라 조금 떨어져 있기 때문입니다. 경보는 판결이 아니라 "사람이 한 번 더 보라"는 신호입니다.' % (od['test_n'], od['test_over_thr'], o4['test_over_thr'])],
                 '두 자도 완벽하지 않습니다. 길이·높이·폭·무게가 모두 학습 물고기처럼 그럴듯하게 틀리면(예: 다른 종을 같은 비율로 잘못 적음) 두 자 모두 통과합니다. 문턱(상위 1%)도 정하기 나름입니다.')
    s += aicheck('"다른 바다 물고기는 농어 100%!"',
                 '<p>다른 바다에서 온 물고기는 측정 기준이 달라 길이1 항목에 꼬리 끝까지 잰 값이 적혔습니다. 주판봇의 보고: "이웃 다섯 마리가 모두 농어라서 농어 확신 100%야!"</p>' +
                 '<p><b>확인 질문</b> ① 이웃이 한목소리인데 왜 믿으면 안 될까요? ② 무엇을 함께 봐야 했을까요?</p>'
                 '<details><summary>생각해 본 뒤 열어 보기</summary><p>① 다수결 확신은 "이웃끼리 의견이 같다"는 뜻일 뿐, 그 물고기가 정상이라는 뜻이 아닙니다. '
                 '② 이 물고기는 지도 거리로는 문턱 안이라 거리만 보면 놓칩니다. 길이1이 길이2보다 길게 적혀 길이 세 값의 관계가 깨졌고, 네 축으로 접었다 펴면 원래대로 돌아오지 않습니다(복원 오차가 문턱의 %s배). 답 옆에는 지도 거리와 복원 오차를 함께 붙입니다.</p></details>' % num(o4['sea_times'], 1))
    s += bridge('gen', '생성 AI로 치면', '대형 언어 모델도 배운 범위 밖의 질문(아주 최근 일, 학습 자료에 없던 전문 지식)에 그럴듯하게 틀린 답을 냅니다. "모르는 것을 모른다고 말하게 하기"는 지금도 중요한 연구 주제입니다.',
                '언어 모델은 물고기 지도처럼 거리를 바로 재 보기 어렵습니다. 그래서 답의 근거 문서를 함께 보여 주게 하는 방법(RAG)을 씁니다.')
    s += bridge('field', '현장에 옮기면', '정면 사진으로 만든 얼굴 지도에 옆모습 사진을 넣으면, 지도 어디에도 없는 자리로 접힙니다. 공장에서 센서를 바꾸거나 측정 방법이 바뀌면 같은 일이 생깁니다. 모델 출력 옆에 "배운 범위 안인가" 표시를 늘 붙이고, 경보가 잦아지면 다시 학습합니다.',
                '문턱(상위 1%)은 정하기 나름입니다. 문턱을 낮추면 경보가 많아지고, 높이면 놓치는 것이 늘어납니다.')
    s += codefold([('NearestNeighbors(n_neighbors=1).fit(S_train)', '지도 위 학습 물고기 목록'),
                   ('dist, _ = nn.kneighbors(S_new); dist > threshold', '가장 가까운 학습 물고기까지 거리가 문턱을 넘는지')])
    s += quiz('q44')
    b += step('s4', '4-4', '배운 것 밖에서는 말하지 않는다 — 범위 밖 경보', ['방법: 이웃 거리 문턱', '일상: 처음 가는 도시의 길 안내'], s)

    b += duel('d4', '곧은 접기 vs 곡선 접기', 'PCA 두 축 (곧은 접기)', '오토인코더 6-16-2-16-6 (곡선 접기)',
              '"물고기 데이터는 곧게 접혀. 단순한 PCA면 충분해."', '"신경망이 크고 복잡하니까 더 잘 되살리지. 큰 게 이긴다!"',
              '시험 물고기의 복원 오차 (작을수록 좋음)')

    b += section('sum', '정리 — 오늘의 전체 그림',
                 '<div class="mapbar"><span>원시 데이터<br><small>측정값 6개 · 이름표 없음</small></span><i>→</i><span>표준화<br><small>단위 지우기 (1장)</small></span><i>→</i>'
                 '<span>묶기 + 접기<br><small>주머니 · 지도 (2·3장)</small></span><i>→</i><span>자기지도<br><small>가리고 맞히며 관계 배우기 (4장)</small></span><i>→</i><span class="on">판단<br><small>이웃 보기 + 범위 확인</small></span></div>'
                 '<p>각 단계가 다음 단계의 안전장치입니다. 표준화가 없으면 군집이 단위에 휘어지고, 지도가 없으면 이웃 찾기가 여섯 방향에서 어렵고, 범위 확인이 없으면 마지막 판단은 운이 됩니다.</p>'
                 '<div class="tw"><table class="tb"><tr><th>내가 묻는 질문</th><th>먼저 돌리는 도구</th><th>왜</th></tr>'
                 '<tr><td>데이터 안에 몇 무리가 있나?</td><td>군집화 (k-평균 → 계층)</td><td>거리와 주머니 수로 직접 나눈다</td></tr>'
                 '<tr><td>변수가 너무 많아 그림으로 못 본다</td><td>PCA</td><td>곧게 접히면 가장 싸고 해석이 분명하다</td></tr>'
                 '<tr><td>빠진 값을 채우거나, 휜 관계까지 접고 싶다</td><td>가리고 맞히기 · 오토인코더</td><td>정답표 없이도 학습 목표를 만들 수 있다</td></tr>'
                 '<tr><td>새 데이터가 기존과 같은 무리인가?</td><td>이웃 찾기 + 범위 확인</td><td>지도 위의 거리와 "배운 범위 안인가"를 함께 본다</td></tr></table></div>'
                 '<p><b>순서보다 원칙</b> 어떤 순서든 표준화는 늘 먼저, 마지막 판단에는 늘 "배운 범위 안인가" 확인이 붙습니다. 이 두 가지만 지키면 도구 선택이 자유로워집니다.</p>'
                 + say('doc', 'magic', '정답표를 만드는 비용이 가장 비싼 곳에서, 정답표 없이 배우는 방법을 씁니다. 비지도학습은 정답이 없는 학습이 아니라, 정답의 위치가 다른 학습입니다. 정답은 데이터의 모양 안에 이미 들어 있습니다.'))
    b += outro([('doc', 'front', '오늘 세 줄 정리. ① 가리고 맞히면 데이터가 스스로 정답이 된다. ② 휜 관계는 곡선 접기(오토인코더)가 더 잘 되살린다. ③ 답 옆에는 늘 "배운 범위 안인가"를 붙인다.'),
                ('robo', 'happy', '큰 신경망이 이겼어! 2승 2패, 드디어 본전이다!'),
                ('fly', 'cry', '…곡선이었네. 인정. 대신 그 두 숫자에 이름 붙이는 건 내가 PCA로 할게.'),
                ('asst', 'spark', '이제 실전 연습장에서 어시장을 직접 운영하며 배운 걸 써 볼게요. 다 같이 가요!')],
               '연구실 식구 네 명이 어시장 검수대에서 물고기를 재고 경보등을 가리키는 장면')
    return b


GLOSS = {
    '자기지도학습': ['자기지도학습 (self-supervised learning)', '데이터 일부를 가리고 나머지로 맞히게 해서, 데이터 자신을 정답으로 쓰는 학습.'],
    '마스크드 모델링': ['마스크드 모델링 (masked modeling)', '일부를 가리고(마스크) 맞히게 하는 자기지도 방법. 정답표 비용이 들지 않음.'],
    '오토인코더': ['오토인코더 (autoencoder)', '입력을 작은 숫자로 접었다가(인코더) 다시 펴도록(디코더) 배우는 신경망.'],
    '인코더': ['인코더 (encoder)', '여섯 값을 작은 메모(숫자 두 개)로 줄이는 부분.'],
    '디코더': ['디코더 (decoder)', '작은 메모로 여섯 값을 다시 그려 내는 부분.'],
    '병목': ['병목 (bottleneck)', '오토인코더 가운데의 좁은 자리. 좁아야 중요한 것만 남깁니다.'],
    '복원 오차': ['복원 오차 (reconstruction error)', '원래 값과 다시 편 값의 차이를 제곱해 평균 낸 것.'],
    '다수결': ['다수결 (majority vote)', '이웃들의 이름표 중 가장 많이 나온 것을 답으로 고르기.'],
    '배운 범위 밖': ['배운 범위 밖 (out-of-distribution)', '학습 데이터 구름에서 멀리 떨어진 새 데이터. 답을 믿으면 안 됨.'],
    '문턱': ['문턱 (threshold)', '경보를 울리는 기준값. 여기서는 학습 물고기 이웃 거리의 상위 1% 지점.'],
    '시험 물고기': ['시험 물고기 (test set)', '학습에 쓰지 않고 채점에만 쓰는 물고기. 같은 원본에서 늘린 물고기는 한쪽에만 둡니다.'],
    '잠재': ['잠재 표현 (latent)', '접은 뒤 남은 작은 좌표. 오토인코더 병목의 두 숫자.'],
}

QUIZ = {
    'q41': [{'q': '가린 무게 맞히기에서 "정답"은 누가 만들었나?', 'o': ['전문가가 새로 붙였다', '원래 데이터에 있던 무게', '정답이 없다'], 'a': 1,
             'why': '무게를 일부러 가렸을 뿐, 정답은 데이터 안에 원래 있었습니다.', 'hint': '가린 값은 어디서 왔나요?'},
            {'q': '맞히는 규칙의 세 지수(1.364, 0.638, 0.991)를 더하면 약 3이다. 무슨 뜻인가?', 'o': ['무게가 부피(길이×높이×폭)처럼 자란다', '무게가 길이에 비례한다'], 'a': 0,
             'why': '세 길이를 곱한 부피의 차원(3)과 같습니다. 데이터가 스스로 찾은 관계입니다.', 'hint': '길이 × 높이 × 폭의 지수 합은?'}],
    'q42': [{'q': '오토인코더를 학습할 때 정답으로 주는 것은?', 'o': ['종 이름', '입력과 같은 여섯 값', '무게 하나'], 'a': 1,
             'why': '자기 자신을 되살리는 것이 목표라 입력이 곧 정답입니다.', 'hint': 'fit(Z, Z).'},
            {'q': '병목을 아주 넓게(예: 숫자 6개 이상) 두면?', 'o': ['더 중요한 것만 남긴다', '그대로 실어 나르기만 해서 압축을 배우지 않는다'], 'a': 1,
             'why': '좁혀야 버릴 것을 고르는 법을 배웁니다.', 'hint': '여섯 값을 여섯 자리에 그대로 넣으면?'}],
    'q43': [{'q': '이웃 5마리가 농어·농어·로치·농어·흰송어일 때 답과 확신은?', 'o': ['농어, 60%', '농어, 100%', '로치, 20%'], 'a': 0,
             'why': '농어가 3표, 3 ÷ 5 = 60%.', 'hint': '가장 많은 이름표의 몫.'},
            {'q': '이 단계에서 이름표는 언제 썼나?', 'o': ['지도를 그릴 때', '이웃이 투표할 때만'], 'a': 1,
             'why': '지도는 이름표 없이 그렸고, 판단할 때만 이웃의 이름표를 참고했습니다.', 'hint': '학습 때와 판단 때를 나눠 생각해 보세요.'}],
    'q44': [{'q': '문턱이 0.228이고 새 물고기의 가장 가까운 이웃 거리가 2.28이면?', 'o': ['문턱의 10배, 배운 범위 밖', '문턱 안, 믿어도 됨'], 'a': 0,
             'why': '2.28 ÷ 0.228 = 10. 학습 물고기 어디와도 멀리 떨어져 있습니다.', 'hint': '나눠서 몇 배인지 보세요.'},
            {'q': '다수결 확신이 100%인데도 답을 보류해야 하는 경우는?', 'o': ['이웃까지 거리가 문턱을 크게 넘을 때', '이웃이 모두 같은 종일 때'], 'a': 0,
             'why': '확신은 이웃끼리 의견이 같다는 뜻일 뿐, 이웃이 가깝다는 뜻이 아닙니다.', 'hint': '"의견이 같다"와 "가깝다"는 다릅니다.'}],
}

JS = r'''
var D=FL.load(),X=D.X,N=D.n,SP=FL.SP,SPC=FL.SPC,SPKO=FL.SPKO;
var TE=D.test,isTe={};TE.forEach(function(i){isTe[i]=1;});var TR=[];for(var i=0;i<N;i++)if(!isTe[i])TR.push(i);
var MS=FL.meanStd(X),Z=FL.standardize(X,MS);
var MW=__MW__,AE=__AE__,OD=__OD__,R4=__R4__,PEX=__PEX__;
var NAMES=['무게','길이1','길이2','길이3','높이','폭'];
/* 학습용으로만 PCA */
var Ztr=TR.map(function(i){return Z[i];}),mtr=[0,0,0,0,0,0];Ztr.forEach(function(z){for(var j=0;j<6;j++)mtr[j]+=z[j]/Ztr.length;});
var Zc=Ztr.map(function(z){return z.map(function(v,j){return v-mtr[j];});}),PCt=FL.pca(Zc);
function toMap(z){return FL.project(z.map(function(v,j){return v-mtr[j];}),PCt.vecs,2);}
function fromMap(s){var z=FL.unproject(s,PCt.vecs);return z.map(function(v,j){return v+mtr[j];});}
var MAP=Z.map(toMap);
function predW(L,Hh,W){return Math.exp(MW.intercept+MW.coef[0]*Math.log(L)+MW.coef[1]*Math.log(Hh)+MW.coef[2]*Math.log(W));}
/* 4-1 */
(function(){var cv=$('#cv41'),cur=-1,reveal=false;var pts=TE.map(function(i){return [X[i][0],predW(X[i][1],X[i][4],X[i][5]),i];});
  var mae=pts.reduce(function(a,p){return a+Math.abs(p[0]-p[1]);},0)/pts.length;
  function vals(){return [+$('#l41').value,+$('#h41').value,+$('#w41').value];}
  function draw(){var f=fit(cv),g=f.c,A=FL.axes(g,f.W,f.H,{xmin:0,xmax:2400,ymin:0,ymax:2400,xlab:'가려 둔 실제 무게 (g)',ylab:'맞힌 무게 (g)'});
    g.strokeStyle='#8a96a3';g.setLineDash([5,4]);g.beginPath();g.moveTo(A.sx(0),A.sy(0));g.lineTo(A.sx(2400),A.sy(2400));g.stroke();g.setLineDash([]);
    pts.forEach(function(p){FL.dot(g,A.sx(p[0]),A.sy(p[1]),2.8,SPC[D.sp[p[2]]],.6);});
    if(cur>=0&&reveal){var p=pts[cur];g.strokeStyle='#c9302c';g.lineWidth=2.5;g.beginPath();g.arc(A.sx(p[0]),A.sy(p[1]),8,0,6.2832);g.stroke();}
    stamp(g,f.W,'시험 물고기 '+pts.length+'마리 · 점선 = 딱 맞힘');}
  function info(){var v=vals();$('#l41v').textContent=v[0].toFixed(1)+'cm';$('#h41v').textContent=v[1].toFixed(1)+'cm';$('#w41v').textContent=v[2].toFixed(1)+'cm';var w=predW(v[0],v[1],v[2]);
    var real=cur>=0?X[TE[cur]][0]:null;
    FL.kpis($('#kp41'),[[FL.fmt(w)+'g','길이·높이·폭으로 맞힌 무게','g'],[cur>=0?(reveal?FL.fmt(real)+'g':'? (가림)'):'—','가려 둔 실제 무게','a'],[cur>=0&&reveal?FL.fmt(Math.abs(w-real))+'g':'—','이 물고기에서 빗나간 양','r'],[FL.fmt(mae,1)+'g','시험 물고기 전체 평균 빗나감','m']]);
    $('#in41').innerHTML=cur>=0?'<p class="'+(reveal?'g':'a')+'">'+(reveal?'시험 물고기('+SPKO[D.sp[TE[cur]]]+')의 실제 무게는 '+FL.fmt(real)+'g, 맞힌 무게는 '+FL.fmt(w)+'g입니다. 빗나간 비율 '+FL.pct(Math.abs(w-real)/real)+'.':'학습에 쓰지 않은 물고기를 뽑아 길이·높이·폭만 넣었습니다. 무게는 아직 가려 두었습니다. "가린 무게 보기"를 눌러 맞춰 보세요.')+'</p>':'<p class="a">막대로 길이·높이·폭을 바꿔 보세요. 원자료의 예(31.2 · 12.5 · 4.3cm)는 약 '+FL.fmt(predW(31.2,12.5,4.3))+'g입니다.</p>';}
  ['l41','h41','w41'].forEach(function(id){$('#'+id).addEventListener('input',function(){cur=-1;reveal=false;info();draw();});});
  var r=rng(41);$('#t41').addEventListener('click',function(){cur=Math.floor(r()*TE.length);reveal=false;var x=X[TE[cur]];$('#l41').value=x[1];$('#h41').value=x[4];$('#w41').value=x[5];info();draw();});
  $('#r41').addEventListener('click',function(){if(cur<0)return;reveal=true;info();draw();});
  info();Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 4-2 */
var AEtest=0,PCtest=0;(function(){var s1=0,s2=0;TE.forEach(function(i){var a=FL.aeForward(Z[i],AE.W,AE.b),p=fromMap(toMap(Z[i]));for(var j=0;j<6;j++){s1+=(a[j]-Z[i][j])*(a[j]-Z[i][j]);s2+=(p[j]-Z[i][j])*(p[j]-Z[i][j]);}});AEtest=s1/(TE.length*6);PCtest=s2/(TE.length*6);})();
(function(){var cv=$('#cv42'),cv2=$('#cv42b'),fi=0;var big=TE.slice().sort(function(a,b){return X[b][0]-X[a][0];});$('#f42').max=big.length-1;
  function net(){var f=fit(cv),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=[6,16,2,16,6],cols=L.length,i=big[fi],act=[Z[i]];var h=Z[i];
    for(var l=0;l<AE.W.length;l++){var o=[];for(var j=0;j<AE.W[l][0].length;j++){var s=AE.b[l][j];for(var k=0;k<h.length;k++)s+=h[k]*AE.W[l][k][j];o.push(l<AE.W.length-1?Math.tanh(s):s);}h=o;act.push(o);}
    function pos(c,n){var x=40+c*(f.W-80)/(cols-1),y=[];for(var q=0;q<n;q++)y.push(f.H/2+(q-(n-1)/2)*Math.min(13,(f.H-40)/n));return {x:x,y:y};}
    for(var c=0;c<cols-1;c++){var a=pos(c,L[c]),b=pos(c+1,L[c+1]);g.strokeStyle='rgba(91,104,116,.12)';for(var p=0;p<L[c];p++)for(var q=0;q<L[c+1];q++){g.beginPath();g.moveTo(a.x,a.y[p]);g.lineTo(b.x,b.y[q]);g.stroke();}}
    for(c=0;c<cols;c++){var P=pos(c,L[c]);for(p=0;p<L[c];p++){var v=act[c][p],t=Math.max(-1,Math.min(1,v/2));g.fillStyle=t>=0?'rgba(31,122,82,'+(.25+.75*t)+')':'rgba(201,48,44,'+(.25-.75*t)+')';g.beginPath();g.arc(P.x,P.y[p],c===2?9:5,0,6.2832);g.fill();g.strokeStyle='#16212b';g.lineWidth=c===2?2:1;g.stroke();}}
    g.fillStyle='#16212b';g.font='700 13px "IBM Plex Sans KR",sans-serif';g.textAlign='center';['여섯 값','16','병목 2','16','다시 여섯 값'].forEach(function(t,c){g.fillText(t,pos(c,1).x,18);});
    g.fillText('인코더 (접기)',(pos(0,1).x+pos(2,1).x)/2,f.H-8);g.fillText('디코더 (펴기)',(pos(2,1).x+pos(4,1).x)/2,f.H-8);g.textAlign='left';
    g.fillStyle='#9b3fb5';g.fillText('메모: '+act[2].map(function(v){return v.toFixed(2);}).join(', '),pos(2,1).x+16,f.H/2+4);stamp(g,f.W,'학습한 가중치 · 색 = 신호 세기');}
  function bars(){var i=big[fi],a=FL.aeForward(Z[i],AE.W,AE.b),p=fromMap(toMap(Z[i])),f=fit(cv2),g=f.c;g.fillStyle='#fff';g.fillRect(0,0,f.W,f.H);var L=70,R=20,T=14,rowH=(f.H-T-14)/6;
    function sx(v){return L+(v+3)/8*(f.W-L-R);}g.font='13px "IBM Plex Sans KR",sans-serif';
    for(var j=0;j<6;j++){var y=T+rowH*j+rowH/2;g.fillStyle='#16212b';g.textAlign='right';g.fillText(NAMES[j],L-8,y+4);g.fillStyle='rgba(31,122,82,.25)';g.fillRect(sx(0),y-8,sx(Z[i][j])-sx(0),16);FL.dot(g,sx(p[j]),y-3,5,'#1e55c8',1);FL.dot(g,sx(a[j]),y+4,5,'#c9302c',1);}
    g.textAlign='left';stamp(g,f.W,'표준화 눈금');
    var xa=a.map(function(v,j){return v*MS.s[j]+MS.m[j];}),xp=p.map(function(v,j){return v*MS.s[j]+MS.m[j];});
    $('#f42v').textContent=SPKO[D.sp[i]]+' '+X[i][0]+'g';
    $('#t42').innerHTML='<tr><th>측정값</th><th class="n">원래</th><th class="n">PCA로 편 값</th><th class="n">오토인코더로 편 값</th></tr>'+NAMES.map(function(n,j){return '<tr><td>'+n+' ('+FL.UNITS[j]+')</td><td class="n">'+X[i][j]+'</td><td class="n">'+xp[j].toFixed(j?2:0)+'</td><td class="n">'+xa[j].toFixed(j?2:0)+'</td></tr>';}).join('');
    FL.kpis($('#kp42'),[[PCtest.toFixed(4),'시험 물고기 복원 오차 · PCA','i'],[AEtest.toFixed(4),'시험 물고기 복원 오차 · 오토인코더','r'],[FL.fmt(Math.abs(xp[0]-X[i][0]))+'g','이 물고기 무게 오차 · PCA','a'],[FL.fmt(Math.abs(xa[0]-X[i][0]))+'g','이 물고기 무게 오차 · 오토인코더','g']]);
    $('#in42').innerHTML='<p class="g">두 방법 모두 숫자 두 개로 접었다 폈습니다. 시험 물고기 전체에서 오토인코더의 복원 오차가 PCA보다 약 '+(PCtest/AEtest).toFixed(1)+'배 작습니다. 차이는 대부분 무게에서 납니다. 막대를 오른쪽 끝(가벼운 물고기)과 왼쪽 끝(무거운 물고기)으로 옮겨 비교해 보세요.</p>';}
  $('#f42').addEventListener('input',function(){fi=+this.value;net();bars();});
  Loop.add(cv,function(dt){if(dt===0)net();});Loop.add(cv2,function(dt){if(dt===0)bars();});
})();
/* 4-3 */
var CARDS=SP.map(function(s){for(var k=0;k<TR.length;k++){var i=TR[k];if(D.sp[i]===s&&D.orig[i])return i;}});
function knn(i,pool,k){var arr=pool.map(function(j){return [FL.d2(MAP[i],MAP[j]),j];});arr.sort(function(a,b){return a[0]-b[0];});return arr.slice(0,k);}
function vote(nb){var c={};nb.forEach(function(x){var s=D.sp[x[1]];c[s]=(c[s]||0)+1;});var best=null;SP.forEach(function(s){if(c[s]&&(!best||c[s]>c[best]))best=s;});return {sp:best,n:c[best]};}
var ACC={};function acc(mode){if(ACC[mode]!==undefined)return ACC[mode];var ok=0;TE.forEach(function(i){var nb=mode==='all'?knn(i,TR,5):knn(i,CARDS,1);if(vote(nb).sp===D.sp[i])ok++;});return ACC[mode]=ok/TE.length;}
(function(){var cv=$('#cv43'),mode='all',fi=0;$('#f43').max=TE.length-1;
  function draw(){var i=TE[fi],nb=mode==='all'?knn(i,TR,5):knn(i,CARDS,1),v=vote(nb);var f=fit(cv),g=f.c,A=FL.axes(g,f.W,f.H,{xmin:-5,xmax:8,ymin:-3,ymax:3,xlab:'지도 가로 (PC1 · 크기)',ylab:'지도 세로 (PC2 · 체형)'});
    TR.forEach(function(j){FL.dot(g,A.sx(MAP[j][0]),A.sy(MAP[j][1]),2.2,'#8a96a3',.3);});
    if(mode==='seven')CARDS.forEach(function(j){FL.dot(g,A.sx(MAP[j][0]),A.sy(MAP[j][1]),7,SPC[D.sp[j]],1);g.fillStyle='#16212b';g.font='12px "IBM Plex Sans KR",sans-serif';g.fillText(SPKO[D.sp[j]],A.sx(MAP[j][0])+9,A.sy(MAP[j][1])-6);});
    nb.forEach(function(x){var j=x[1];g.strokeStyle='#5b6874';g.lineWidth=1.5;g.beginPath();g.moveTo(A.sx(MAP[i][0]),A.sy(MAP[i][1]));g.lineTo(A.sx(MAP[j][0]),A.sy(MAP[j][1]));g.stroke();FL.dot(g,A.sx(MAP[j][0]),A.sy(MAP[j][1]),5,SPC[D.sp[j]],1);});
    g.fillStyle='#16212b';g.strokeStyle='#16212b';g.lineWidth=2.5;g.beginPath();g.arc(A.sx(MAP[i][0]),A.sy(MAP[i][1]),8,0,6.2832);g.fillStyle='#fff';g.fill();g.stroke();
    stamp(g,f.W,'회색 = 학습 물고기(이름표 없이 그림)');
    $('#f43v').textContent='#'+(fi+1);var ok=v.sp===D.sp[i];
    FL.kpis($('#kp43'),[[SPKO[v.sp],'이웃 다수결 답','g'],[mode==='all'?FL.pct(v.n/5,0):'—',mode==='all'?'확신 (같은 답 이웃 ÷ 5)':'이름표 7장이라 가장 가까운 1장으로','i'],[SPKO[D.sp[i]]+(ok?' ✓':' ✗'),'시험 물고기의 실제 종','a'],[FL.pct(acc(mode)),'시험 '+TE.length+'마리 정답률','m']]);
    $('#in43').innerHTML=mode==='all'?'<p class="'+(ok?'g':'r')+'">이웃 5마리에게 물었습니다. '+(ok?'답이 맞았습니다.':'답이 틀렸습니다. 지도 가운데 농어·로치·흰송어가 겹치는 곳에서 자주 일어납니다.')+' 시험 정답률은 '+FL.pct(acc('all'))+'로, 이름표를 학습에 쓴 지도학습 KNN('+'__SUPKNN__'+')보다 조금 낮습니다.</p>':'<p class="m">이름표가 종마다 한 장(큰 점)뿐입니다. 가장 가까운 이름표 한 장을 답으로 하면 시험 정답률이 '+FL.pct(acc('seven'))+'입니다. 찍기(14.3%)의 약 '+(acc('seven')/0.1429).toFixed(1)+'배입니다.</p>';}
  $$('#p43 [data-l]').forEach(function(bt){bt.addEventListener('click',function(){mode=bt.dataset.l;$$('#p43 [data-l]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();});});
  $('#f43').addEventListener('input',function(){fi=+this.value;draw();});Loop.add(cv,function(dt){if(dt===0)draw();});
})();
/* 4-4 */
var THR=OD.thr_q99,THR4=R4.thr_q99;
function nnDist(m){var b=Infinity;TR.forEach(function(j){var d=FL.d2(m,MAP[j]);if(d<b)b=d;});return Math.sqrt(b);}
function recon4(z){var c=z.map(function(v,j){return v-mtr[j];}),s=FL.project(c,PCt.vecs,4),b=FL.unproject(s,PCt.vecs),e=0;for(var j=0;j<6;j++)e+=(c[j]-b[j])*(c[j]-b[j]);return e/6;}
(function(){var cv=$('#cv44'),preset='perch',scale=1;var base=X[PEX].slice();
  var PRE={perch:base,big:OD.big_fish.x.slice(),sea:[base[0],base[3],base[2],base[3],base[4],base[5]]};
  function fishNow(){var x=PRE[preset].slice();x[1]=x[1]*scale;return x;}
  function draw(){var x=fishNow(),z=x.map(function(v,j){return (v-MS.m[j])/MS.s[j];}),m=toMap(z),d=nnDist(m),rc=recon4(z);var nb=TR.map(function(j){return [FL.d2(m,MAP[j]),j];}).sort(function(a,b){return a[0]-b[0];}).slice(0,5);var v=vote(nb);
    var fd=d>THR,fr=rc>THR4,al=fd||fr;
    var f=fit(cv),g=f.c,xmax=Math.max(8,m[0]+1.5),ymin=Math.min(-3,m[1]-1),ymax=Math.max(3,m[1]+1);var A=FL.axes(g,f.W,f.H,{xmin:-5,xmax:xmax,ymin:ymin,ymax:ymax,xlab:'지도 가로 (PC1 · 크기)',ylab:'지도 세로 (PC2 · 체형)'});
    TR.forEach(function(j){FL.dot(g,A.sx(MAP[j][0]),A.sy(MAP[j][1]),2.2,'#1f7a52',.25);});
    var j0=nb[0][1];g.strokeStyle=fd?'#c9302c':'#1f7a52';g.lineWidth=2;g.setLineDash([6,4]);g.beginPath();g.moveTo(A.sx(m[0]),A.sy(m[1]));g.lineTo(A.sx(MAP[j0][0]),A.sy(MAP[j0][1]));g.stroke();g.setLineDash([]);
    g.fillStyle=al?'#c9302c':'#1f7a52';g.beginPath();g.arc(A.sx(m[0]),A.sy(m[1]),9,0,6.2832);g.fill();g.fillStyle='#fff';g.font='700 12px "IBM Plex Sans KR",sans-serif';g.textAlign='center';g.fillText(al?'!':'✓',A.sx(m[0]),A.sy(m[1])+4);g.textAlign='left';
    stamp(g,f.W,'초록 구름 = 학습 물고기');
    $('#s44v').textContent='×'+scale.toFixed(2)+' ('+x[1].toFixed(1)+'cm)';
    FL.kpis($('#kp44'),[[SPKO[v.sp],'이웃 다수결 답 (늘 나옴)','i'],[(d/THR).toFixed(1)+'배','지도 거리 ÷ 거리 문턱',fd?'r':'g'],[(rc/THR4).toFixed(1)+'배','복원 오차 ÷ 복원 문턱',fr?'r':'g'],[al?'경보 · 답 보류':'범위 안','판단',al?'r':'g']]);
    var t;if(fd&&fr)t='지도 거리도 복원 오차도 문턱을 넘었습니다. 학습한 물고기와 전혀 다른 물고기입니다. 답 "'+SPKO[v.sp]+'"는 보류합니다.';
    else if(fd)t='지도 거리가 문턱의 '+(d/THR).toFixed(1)+'배입니다. 지도 구름 밖에 놓였으니 답 "'+SPKO[v.sp]+'"는 보류합니다.';
    else if(fr)t='지도 거리는 문턱 안('+(d/THR).toFixed(1)+'배)이라 거리만 보면 놓칩니다. 그런데 네 축으로 접었다 펴면 원래대로 돌아오지 않습니다(복원 오차가 문턱의 '+(rc/THR4).toFixed(1)+'배). 길이1이 길이2보다 길게 적혀 길이 세 값의 관계가 깨졌기 때문입니다.';
    else t='두 자 모두 문턱 안입니다. 이웃 다수결 답 "'+SPKO[v.sp]+'"를 참고해도 됩니다. 길이1 배율을 바꿔 길이1만 늘이거나 줄여 보세요. 길이 관계가 깨지면 복원 오차가 먼저 반응합니다.';
    $('#in44').innerHTML='<p class="'+(al?'r':'g')+'">'+t+'</p>';}
  $$('#p44 [data-p]').forEach(function(bt){bt.addEventListener('click',function(){preset=bt.dataset.p;scale=1;$('#s44').value=1;$$('#p44 [data-p]').forEach(function(x){x.setAttribute('aria-pressed',x===bt?'true':'false');});draw();});});
  $('#s44').addEventListener('input',function(){scale=+this.value;draw();});Loop.add(cv,function(dt){if(dt===0)draw();});
})();
Duel({el:'#d4',run:function(){return {fly:PCtest,robo:AEtest};},fmt:function(v){return v.toFixed(4);},higherIsBetter:false,bigGap:.02,
  report:function(r){return '시험 물고기 '+TE.length+'마리의 복원 오차는 초파리 쪽(PCA) '+r.fly.toFixed(4)+', 주판봇 쪽(오토인코더) '+r.robo.toFixed(4)+'예요. 작을수록 잘 되살린 거예요. 무게에서 차이가 가장 커요.';},
  verdict:{fly:'곧은 접기로 충분했다. 초파리 승.',robo:'무게처럼 휜 관계는 곡선 접기가 더 잘 되살린다. 주판봇 승.',draw:'두 접기가 비슷하다. 이번 판은 나눠 갖는다.'}});
'''.replace('__MW__', json.dumps(R['mask_weight'])).replace('__AE__', json.dumps(R['ae_weights'])).replace('__OD__', json.dumps(R['ood'])).replace('__R4__', json.dumps({'thr_q99': R['pca4_ood']['thr_q99']})).replace('__PEX__', str(R['perch_example'])).replace('__SUPKNN__', pct(R['supervised']['knn1_group_cv']))


def main():
    USED.update(['fly_arms', 'fly_coffee', 'fly_cry', 'robo_sigh', 'robo_happy', 'robo_meh', 'fly_point', 'robo_coin'])
    hero_html = hero('4장 · 비지도학습 물고기 연구실', '맞히기 — 자기지도학습', '절반을 가리고, 남은 절반으로 맞히게 하면 정답표 없이도 배울 수 있을까?',
                     '정답표를 만들 사람이 없습니다. 그런데 데이터 자체가 정답표가 될 수 있습니다. 가린 부분을 원래 데이터로 채워 보면 맞았는지 스스로 알 수 있으니까요. '
                     '이 장에서는 <b>가린 무게 맞히기</b>, 곡선으로 접는 <b>오토인코더</b>, 지도 위 <b>이웃 찾기</b>를 차례로 보고, 마지막으로 가장 중요한 습관인 <b>"배운 범위 밖에서는 모른다고 말하기"</b>를 연습합니다.',
                     [(num(mw['mae_g'], 1) + 'g', '가린 무게를 맞힌 평균 빗나감 (시험 물고기)', 'g'), (num(av['ae_test_mse'], 4), '오토인코더 복원 오차 (PCA ' + num(av['pca2_test_mse'], 4) + ')', 'r'),
                      (pct(km['pc2_k5_test_acc']), '이름표 없이 그린 지도 위 이웃 5마리 정답률', 'i'), (num(od['big_fish']['times_thr'], 1) + '배', '1m 물고기의 이웃 거리 (문턱 대비)', 'a')],
                     [('doc', 'front', '오늘은 데이터가 스스로 문제를 내고 스스로 채점합니다. 그리고 모르는 걸 모른다고 말하는 법을 배웁니다.'),
                      ('asst', 'smile', '정답표 없이 채점을 한다고요? 그게 가능해요?'),
                      ('fly', 'point', '가린 값이 정답이야. 대신 처음 보는 물고기 앞에서는 조심해야 해.'),
                      ('robo', 'coin', '큰 신경망이면 다 맞혀! 이번엔 확실히 이긴다.')])
    b = body()
    b += footer([('데이터', 'Aung Pyae, Kaggle "Fish market" (CC BY 4.0) → <a href="https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning">Fish_Market_Data_Machine_Learning</a> 증강본'),
                 ('원자료', '안상선, 강의 슬라이드 「라벨링 없이 맞추는 AI — 비지도학습 모델」 PART 3 자기지도학습 (2026)'),
                 ('수치', 'code/analysis.py (scikit-learn 1.9.1, 물고기 묶음 단위 80/20 분할 random_state=0, MLPRegressor 16-2-16 tanh)'),
                 ('오토인코더', 'Hinton, G. E., & Salakhutdinov, R. R. (2006). Reducing the dimensionality of data with neural networks. Science, 313(5786), 504–507'),
                 ('마스크드 모델링', 'Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT. NAACL-HLT 2019, 4171–4186'),
                 ('k-최근접 이웃', 'Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1), 21–27')],
                ['4-4의 "1m 큰 물고기"(무게 9kg)와 "다른 바다 물고기"(길이1 항목에 길이3 값)는 설명용 가상 물고기', '수식 상자의 f(x) = 2x, 이웃 다섯의 종 목록은 예시값', '오토인코더 그림의 신호 색은 학습한 가중치로 계산한 실제 값'],
                prev=('03_folding.html', '3장 · 접기 — 차원 축소'), nxt=('practice/index.html', '마지막 장 · 실전 연습장'))
    return build(P, title='4장 · 맞히기 — 자기지도학습 · 비지도학습 물고기 연구실',
                 desc='가린 무게 맞히기, 오토인코더, 지도 위 이웃 찾기, 배운 범위 밖 경보로 자기지도학습과 비지도학습의 판단 습관을 익힌다.',
                 nav=[('#first', '3줄'), ('#s1', '4-1 가린 무게'), ('#s2', '4-2 오토인코더'), ('#s3', '4-3 이웃'), ('#s4', '4-4 범위 밖'), ('#duel', '대결'), ('#sum', '정리')],
                 cover_html=cover('cover_04', '4장 · 맞히기', '맞히기 — 자기지도학습'), hero=hero_html, body=b, gloss=GLOSS, quizzes=QUIZ, page_js=JS, with_test=True, og='og_04')


if __name__ == '__main__':
    print(main())
