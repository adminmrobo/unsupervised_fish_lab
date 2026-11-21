# -*- coding: utf-8 -*-
"""페이지마다 kg.json · refs.json · meta.json을 만들고 retrofit.py로 #kg·#export를 붙인 뒤 check.py로 점검한다."""
import json, os, subprocess, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib import R, SERIES, SITE

DATE = '2026-11-21'
REFS = {
    'pyae2019fish': {'type': 'dataset', 'title': 'Fish market [Dataset]', 'author': [{'family': 'Pyae', 'given': 'Aung'}], 'publisher': 'Kaggle',
                     'URL': 'https://www.kaggle.com/datasets/aungpyaeap/fish-market', 'genre': '데이터셋 (물고기 7종 159마리)', 'role': 'data',
                     'verified': {'title': True, 'author': True, 'year': False, 'container': True, 'pages': False, 'doi': False}, 'checkedBy': 'Hugging Face scikit-learn/Fish 데이터 카드의 출처 표기 (2026-11-21 확인)', 'checkedSource': 'web', 'year': None},
    'ahn2026supervised': {'type': 'webpage', 'title': 'Fish Market Data로 쉽게 따라하는 머신러닝', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo',
                          'URL': 'https://github.com/adminmrobo/Fish_Market_Data_Machine_Learning', 'genre': '지도학습 해설 시리즈 (증강 데이터 fish_market_x10.csv 출처)', 'role': 'background', 'year': 2026,
                          'verified': {'title': True, 'author': True, 'year': True, 'container': True, 'pages': False, 'doi': False}, 'checkedBy': '저장소 README (2026-11-21 확인)', 'checkedSource': 'repo'},
    'ahn2026slides': {'type': 'speech', 'title': '라벨링 없이 맞추는 AI — 비지도학습 모델 (강의 슬라이드)', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo', 'genre': '강의 자료 (슬라이드 35쪽, Colab 실습 노트북)', 'role': 'primary', 'year': 2026,
                      'verified': {'title': True, 'author': True, 'year': True, 'container': False, 'pages': True, 'doi': False}, 'checkedBy': '저자가 준 PDF', 'checkedSource': 'page'},
    'hastie2009elements': {'type': 'book', 'title': 'The Elements of Statistical Learning (2nd ed.)', 'author': [{'family': 'Hastie', 'given': 'Trevor'}, {'family': 'Tibshirani', 'given': 'Robert'}, {'family': 'Friedman', 'given': 'Jerome'}],
                           'publisher': 'Springer', 'year': 2009, 'role': 'background', 'verified': {'title': True, 'author': True, 'year': True, 'container': True, 'pages': False, 'doi': False}, 'checkedBy': '페이지 참고문헌 목록에서 옮김', 'checkedSource': 'page'},
    'lloyd1982least': {'type': 'article-journal', 'title': 'Least squares quantization in PCM', 'author': [{'family': 'Lloyd', 'given': 'Stuart P.'}], 'container-title': 'IEEE Transactions on Information Theory', 'volume': '28', 'issue': '2', 'page': '129–137', 'year': 1982, 'role': 'method'},
    'rousseeuw1987silhouettes': {'type': 'article-journal', 'title': 'Silhouettes: A graphical aid to the interpretation and validation of cluster analysis', 'author': [{'family': 'Rousseeuw', 'given': 'Peter J.'}], 'container-title': 'Journal of Computational and Applied Mathematics', 'volume': '20', 'page': '53–65', 'year': 1987, 'role': 'method'},
    'ward1963hierarchical': {'type': 'article-journal', 'title': 'Hierarchical grouping to optimize an objective function', 'author': [{'family': 'Ward', 'given': 'Joe H.'}], 'container-title': 'Journal of the American Statistical Association', 'volume': '58', 'issue': '301', 'page': '236–244', 'year': 1963, 'role': 'method'},
    'pearson1901lines': {'type': 'article-journal', 'title': 'On lines and planes of closest fit to systems of points in space', 'author': [{'family': 'Pearson', 'given': 'Karl'}], 'container-title': 'Philosophical Magazine', 'volume': '2', 'issue': '11', 'page': '559–572', 'year': 1901, 'role': 'method'},
    'turk1991eigenfaces': {'type': 'article-journal', 'title': 'Eigenfaces for recognition', 'author': [{'family': 'Turk', 'given': 'Matthew'}, {'family': 'Pentland', 'given': 'Alex'}], 'container-title': 'Journal of Cognitive Neuroscience', 'volume': '3', 'issue': '1', 'page': '71–86', 'year': 1991, 'role': 'background'},
    'hinton2006reducing': {'type': 'article-journal', 'title': 'Reducing the dimensionality of data with neural networks', 'author': [{'family': 'Hinton', 'given': 'Geoffrey E.'}, {'family': 'Salakhutdinov', 'given': 'Ruslan R.'}], 'container-title': 'Science', 'volume': '313', 'issue': '5786', 'page': '504–507', 'year': 2006, 'role': 'method'},
    'devlin2019bert': {'type': 'paper-conference', 'title': 'BERT: Pre-training of deep bidirectional transformers for language understanding', 'author': [{'family': 'Devlin', 'given': 'Jacob'}, {'family': 'Chang', 'given': 'Ming-Wei'}, {'family': 'Lee', 'given': 'Kenton'}, {'family': 'Toutanova', 'given': 'Kristina'}], 'container-title': 'NAACL-HLT 2019', 'page': '4171–4186', 'year': 2019, 'role': 'background'},
    'cover1967nearest': {'type': 'article-journal', 'title': 'Nearest neighbor pattern classification', 'author': [{'family': 'Cover', 'given': 'Thomas'}, {'family': 'Hart', 'given': 'Peter'}], 'container-title': 'IEEE Transactions on Information Theory', 'volume': '13', 'issue': '1', 'page': '21–27', 'year': 1967, 'role': 'method'},
}


def ref(rid):
    r = dict(REFS[rid]); y = r.pop('year', None); role = r.pop('role', 'background')
    ver = r.pop('verified', {'title': True, 'author': True, 'year': True, 'container': True, 'pages': True, 'doi': False})
    cb = r.pop('checkedBy', '페이지 참고문헌 목록에서 옮김 (외부 대조 안 함)'); cs = r.pop('checkedSource', 'page')
    o = {'id': rid}; o.update(r)
    if y: o['issued'] = {'date-parts': [[y]]}
    o['lab'] = {'work': 'lab:work/' + rid, 'role': role, 'supports': [], 'locs': [], 'verified': ver, 'checkedBy': cb, 'checkedSource': cs}
    return o


def build_page(slug, number, title, about, refs, nodes, edges, quiz=None, qanchor=None):
    page = slug
    N, E = [], []
    for t in nodes:
        nid, typ, ko, en, anchor, lvl, dfn = t[:7]
        n = {'id': nid, 'type': typ, 'label': {'ko': ko, 'en': en}, 'page': page, 'anchor': anchor, 'level': lvl, 'status': 'known', 'confidence': 'high',
             'coverage': 'explained', 'match': [], 'domain': ['ai']}
        if dfn: n['definition'] = {'ko': dfn}
        if len(t) > 7 and t[7]: n['source'] = [{'ref': t[7], 'loc': ''}]
        N.append(n)
    for rid in refs:
        a = REFS[rid]
        N.append({'id': 'lab:work/' + rid, 'type': 'Work', 'label': {'ko': '%s (%s) %s' % (a['author'][0]['family'] + (' 외' if len(a['author']) > 1 else ''), a.get('year') or 'n.d.', a.get('container-title') or a.get('publisher', '')),
                                                                     'en': a['title']}, 'page': page, 'anchor': '#export', 'level': 2, 'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
    for s, p, o, anchor in edges:
        E.append({'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': anchor, 'confidence': 'high'})
    # 문헌 노드 연결: 출처 있는 주장 → 문헌, 없으면 첫 개념 → 문헌
    cited = set()
    for n in N:
        for sr in n.get('source', []):
            E.append({'s': n['id'], 'p': 'lab:assertedIn', 'o': 'lab:work/' + sr['ref'], 'anchor': n['anchor'], 'confidence': 'high'}); cited.add(sr['ref'])
    for rid in refs:
        if rid not in cited:
            E.append({'s': about[0], 'p': 'lab:explainedIn', 'o': 'lab:work/' + rid, 'anchor': '#export', 'confidence': 'high'})
    if quiz:
        for qid, items in quiz.items():
            sec = qanchor(qid)
            for k, q in enumerate(items):
                nid = 'lab:quiz/unsup-%s-%s-%d' % (number, qid, k + 1)
                N.append({'id': nid, 'type': 'QuizItem', 'label': {'ko': q['q'][:60], 'en': 'Quiz %s %s-%d' % (number, qid, k + 1)}, 'page': page, 'anchor': sec, 'level': 2,
                          'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
                E.append({'s': nid, 'p': 'lab:assesses', 'o': QMAP[qid], 'anchor': sec, 'confidence': 'high'})
    kg = {'version': '1.0', 'page': page, 'nodes': N, 'edges': E}
    meta = {'title': title, 'number': number, 'series': SERIES, 'about': about, 'basedOn': refs, 'educationalLevel': '입문',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': DATE, 'version': '1.0',
            'language': ['ko'], 'license': '', 'url': SITE + (slug if slug.endswith('/index') is False else slug), 'registry': 'KG_00_registry 0.2',
            'learningResourceType': 'interactive explainer', 'seeAlso': '', 'domain': ['ai'],
            'suggestedCitation': '안상선 (2026). %s. %s %s, v1.0.' % (title, SERIES, number)}
    return kg, [ref(r) for r in refs], meta


T = 'lab:topic/'
QMAP = {}


def pages():
    P = {}
    # 목차
    nodes = [('lab:concept/unsupervised-learning', 'Concept', '비지도학습', 'Unsupervised learning', '#compare', 1, '정답 없이 입력만으로 데이터의 구조를 찾는 학습'),
             ('lab:concept/supervised-learning', 'Concept', '지도학습', 'Supervised learning', '#compare', 1, '입력과 정답을 함께 주고 정답을 맞히도록 배우는 학습'),
             ('lab:concept/self-supervised-learning', 'Concept', '자기지도학습', 'Self-supervised learning', '#toc', 1, '데이터 일부를 가리고 맞히게 해 데이터 자신을 정답으로 쓰는 학습'),
             ('lab:dataset/fish-market-x10', 'Dataset', '어시장 물고기 1,554마리 (증강)', 'Fish Market augmented (1,554 fish)', '#data', 1, 'Kaggle Fish Market 159마리를 종별 평균·분산을 지키며 늘린 데이터', 'ahn2026supervised'),
             ('lab:claim/series-record', 'Claim', '대결 전적 2승 2패 — 단순함도 큰 모델도 늘 정답은 아니다', 'Duel record 2-2', '#record', 2, ''),
             ('lab:question/where-is-answer', 'Question', '정답표가 없어도 데이터 안에 숨은 모양을 찾을 수 있을까?', 'Can we find structure without labels?', '#first', 1, '')]
    edges = [('lab:concept/unsupervised-learning', 'broader', T + 'unsupervised-learning', '#compare'), ('lab:concept/supervised-learning', 'broader', T + 'supervised-learning', '#compare'),
             ('lab:concept/self-supervised-learning', 'broader', T + 'self-supervised', '#toc'), ('lab:concept/unsupervised-learning', 'contrastsWith', 'lab:concept/supervised-learning', '#compare'),
             ('lab:concept/self-supervised-learning', 'relatedTo', 'lab:concept/unsupervised-learning', '#toc'), ('lab:concept/unsupervised-learning', 'evaluatedOn', 'lab:dataset/fish-market-x10', '#data'),
             ('lab:claim/series-record', 'supports', 'lab:concept/unsupervised-learning', '#record'), ('lab:question/where-is-answer', 'addressedBy', 'lab:concept/unsupervised-learning', '#first')]
    P['index'] = ('index', '0', '비지도학습 물고기 연구실 — 목차', ['lab:concept/unsupervised-learning'], ['pyae2019fish', 'ahn2026supervised', 'ahn2026slides', 'hastie2009elements'], nodes, edges, None)
    # 1장
    import p01
    for q in p01.QUIZ: QMAP[q] = {'q11': 'lab:concept/unsupervised-learning', 'q12': 'lab:concept/euclidean-distance', 'q13': 'lab:concept/standardization'}[q]
    nodes = [('lab:concept/unsupervised-learning', 'Concept', '비지도학습', 'Unsupervised learning', '#s1', 1, '정답 없이 입력만으로 데이터의 구조를 찾는 학습'),
             ('lab:concept/supervised-learning', 'Concept', '지도학습', 'Supervised learning', '#s1', 1, '입력과 정답(이름표)을 함께 주고 정답을 맞히도록 배우는 학습'),
             ('lab:concept/self-supervised-learning', 'Concept', '자기지도학습', 'Self-supervised learning', '#s1', 1, '일부를 가리고 맞히게 해 가린 값을 정답으로 쓰는 학습'),
             ('lab:concept/feature', 'Concept', '특성(측정값)', 'Feature', '#map', 1, '한 마리를 설명하는 숫자 열, 여기서는 여섯 개'),
             ('lab:concept/euclidean-distance', 'Concept', '유클리드 거리', 'Euclidean distance', '#s2', 2, '차이의 제곱합에 루트를 씌운 직선 거리'),
             ('lab:concept/manhattan-distance', 'Concept', '맨해튼 거리', 'Manhattan distance', '#s2', 2, '차이의 절댓값을 더한 거리'),
             ('lab:concept/body-ratio', 'Concept', '체형 비율 (높이÷길이1)', 'Body-shape ratio', '#s2', 2, '크기를 빼고 생김새만 남긴 비율'),
             ('lab:method/standardization', 'Method', '표준화 (z 점수)', 'Standardization', '#s3', 2, '평균을 빼고 표준편차로 나눠 눈금을 맞추는 일'),
             ('lab:limitation/unit-dominance', 'Limitation', '단위가 큰 변수가 거리를 독점', 'Unit dominance in distance', '#s3', 2, '원 단위면 무게가 이웃 거리의 81%를 차지'),
             ('lab:claim/std-improves-neighbors', 'Claim', '표준화하면 이웃이 같은 종인 비율이 78.9%→92.3%', 'Standardization raises same-species neighbor rate', '#duel', 2, '', 'pyae2019fish'),
             ('lab:limitation/redundant-features', 'Limitation', '같은 정보를 가진 변수의 중복 투표', 'Redundant features', '#s3', 2, '길이 세 값의 상관이 0.99 이상'),
             ('lab:sim/u1-standardize', 'Simulation', '원 단위 vs 표준화 실험장', 'Raw vs standardized lab', '#s3', 2, '')]
    QMAP['q12'] = 'lab:concept/euclidean-distance'; QMAP['q13'] = 'lab:method/standardization'
    edges = [('lab:concept/unsupervised-learning', 'broader', T + 'unsupervised-learning', '#s1'), ('lab:concept/supervised-learning', 'broader', T + 'supervised-learning', '#s1'),
             ('lab:concept/self-supervised-learning', 'broader', T + 'self-supervised', '#s1'), ('lab:concept/feature', 'broader', T + 'feature-engineering', '#map'),
             ('lab:concept/euclidean-distance', 'broader', T + 'knn', '#s2'), ('lab:concept/manhattan-distance', 'broader', T + 'knn', '#s2'), ('lab:concept/body-ratio', 'broader', T + 'feature-engineering', '#s2'),
             ('lab:method/standardization', 'broader', T + 'feature-engineering', '#s3'), ('lab:limitation/unit-dominance', 'broader', T + 'feature-engineering', '#s3'), ('lab:limitation/redundant-features', 'broader', T + 'feature-engineering', '#s3'),
             ('lab:concept/unsupervised-learning', 'contrastsWith', 'lab:concept/supervised-learning', '#s1'), ('lab:concept/euclidean-distance', 'hasLimitation', 'lab:limitation/unit-dominance', '#s2'),
             ('lab:limitation/unit-dominance', 'addressedBy', 'lab:method/standardization', '#s3'), ('lab:method/standardization', 'hasLimitation', 'lab:limitation/redundant-features', '#s3'),
             ('lab:claim/std-improves-neighbors', 'supports', 'lab:method/standardization', '#duel'), ('lab:concept/manhattan-distance', 'contrastsWith', 'lab:concept/euclidean-distance', '#s2'),
             ('lab:concept/body-ratio', 'relatedTo', 'lab:concept/euclidean-distance', '#s2'), ('lab:sim/u1-standardize', 'demonstratedBy', 'lab:method/standardization', '#s3'),
             ('lab:concept/feature', 'prerequisiteOf', 'lab:concept/euclidean-distance', '#s2')]
    P['01'] = ('01_no_answer_key', '1', '1장 · 정답표 없이 배운다 — 거리와 표준화', ['lab:concept/unsupervised-learning', 'lab:method/standardization'],
               ['pyae2019fish', 'ahn2026supervised', 'ahn2026slides', 'hastie2009elements'], nodes, edges, (p01.QUIZ, lambda q: '#s' + q[2]))
    QMAP['q11'] = 'lab:concept/unsupervised-learning'
    # 2장
    import p02
    QMAP.update({'q21': 'lab:method/kmeans', 'q22': 'lab:method/elbow', 'q23': 'lab:concept/silhouette', 'q24': 'lab:method/hierarchical', 'q25': 'lab:claim/three-body-shapes'})
    nodes = [('lab:concept/clustering', 'Concept', '군집화 (주머니 나누기)', 'Clustering', '#map', 1, '정답 없이 비슷한 것끼리 무리로 나누는 일'),
             ('lab:method/kmeans', 'Method', 'k-평균', 'k-means', '#s1', 2, '중심 k개를 놓고 배정과 평균 이동을 반복', 'lloyd1982least'),
             ('lab:concept/centroid', 'Concept', '중심', 'Centroid', '#s1', 2, '주머니 안 점들의 평균 위치'),
             ('lab:concept/inertia', 'Metric', '안쪽 거리 합', 'Inertia', '#s2', 2, '각 점과 자기 중심 사이 거리 제곱의 합'),
             ('lab:method/elbow', 'Method', '엘보 방법', 'Elbow method', '#s2', 2, '안쪽 거리 합이 줄어드는 폭이 꺾이는 k를 고름'),
             ('lab:concept/silhouette', 'Metric', '실루엣 점수', 'Silhouette score', '#s3', 2, '(b−a)÷max(a,b), −1~+1', 'rousseeuw1987silhouettes'),
             ('lab:method/hierarchical', 'Method', '계층 군집 (워드 연결)', 'Hierarchical clustering (Ward)', '#s4', 2, '흩어짐이 가장 적게 느는 쌍부터 합쳐 족보 나무를 만듦', 'ward1963hierarchical'),
             ('lab:concept/dendrogram', 'Concept', '덴드로그램', 'Dendrogram', '#s4', 2, '합친 기록을 그린 족보 나무'),
             ('lab:metric/ari', 'Metric', '조정 랜드 지수 (대조 점수)', 'Adjusted Rand index', '#s5', 2, '주머니와 이름표가 얼마나 같은지 재는 점수'),
             ('lab:claim/three-body-shapes', 'Claim', '체형 비율로 나누면 납작·중간·길쭉 세 갈래 (k=3, 실루엣 0.68)', 'Three body shapes emerge', '#s5', 2, '', 'pyae2019fish'),
             ('lab:claim/raw-clusters-by-size', 'Claim', '원 단위 측정값으로 나누면 크기로 갈려 대조 점수 0.109', 'Raw features cluster by size', '#s5', 2, ''),
             ('lab:limitation/kmeans-init', 'Limitation', 'k 지정·시작 위치·둥근 모양 가정', 'k-means needs k and is init-sensitive', '#s1', 2, ''),
             ('lab:limitation/cluster-not-species', 'Limitation', '주머니는 닮음이지 정체가 아니다', 'Clusters are not species', '#s5', 2, ''),
             ('lab:sim/u2-kmeans', 'Simulation', 'k-평균 네 걸음 실험장', 'k-means stepper', '#s1', 2, '')]
    edges = [('lab:concept/clustering', 'broader', T + 'clustering', '#map'), ('lab:method/kmeans', 'broader', T + 'clustering', '#s1'), ('lab:concept/centroid', 'broader', T + 'clustering', '#s1'),
             ('lab:method/elbow', 'broader', T + 'clustering', '#s2'), ('lab:method/hierarchical', 'broader', T + 'clustering', '#s4'), ('lab:concept/dendrogram', 'broader', T + 'clustering', '#s4'),
             ('lab:limitation/kmeans-init', 'broader', T + 'clustering', '#s1'), ('lab:limitation/cluster-not-species', 'broader', T + 'clustering', '#s5'),
             ('lab:method/kmeans', 'partOf', 'lab:concept/clustering', '#s1'), ('lab:concept/centroid', 'partOf', 'lab:method/kmeans', '#s1'), ('lab:method/kmeans', 'hasLimitation', 'lab:limitation/kmeans-init', '#s1'),
             ('lab:limitation/kmeans-init', 'addressedBy', 'lab:method/elbow', '#s2'), ('lab:method/elbow', 'measuredBy', 'lab:concept/inertia', '#s2'), ('lab:method/kmeans', 'evaluatedBy', 'lab:concept/silhouette', '#s3'),
             ('lab:limitation/kmeans-init', 'addressedBy', 'lab:method/hierarchical', '#s4'), ('lab:method/hierarchical', 'contrastsWith', 'lab:method/kmeans', '#s4'), ('lab:concept/dendrogram', 'partOf', 'lab:method/hierarchical', '#s4'),
             ('lab:claim/three-body-shapes', 'supports', 'lab:method/kmeans', '#s5'), ('lab:claim/three-body-shapes', 'evaluatedBy', 'lab:metric/ari', '#s5'), ('lab:claim/raw-clusters-by-size', 'supports', 'lab:limitation/cluster-not-species', '#s5'),
             ('lab:concept/clustering', 'hasLimitation', 'lab:limitation/cluster-not-species', '#s5'), ('lab:sim/u2-kmeans', 'demonstratedBy', 'lab:method/kmeans', '#s1')]
    P['02'] = ('02_grouping', '2', '2장 · 묶기 — 군집화', ['lab:concept/clustering', 'lab:method/kmeans'],
               ['pyae2019fish', 'ahn2026slides', 'lloyd1982least', 'rousseeuw1987silhouettes', 'ward1963hierarchical'], nodes, edges, (p02.QUIZ, lambda q: '#s' + q[2]))
    # 3장
    import p03
    QMAP.update({'q31': 'lab:concept/correlation', 'q32': 'lab:concept/projection', 'q33': 'lab:method/pca', 'q34': 'lab:claim/size-shape-axes', 'q35': 'lab:concept/reconstruction'})
    nodes = [('lab:concept/dimensionality-reduction', 'Concept', '차원 축소 (접기)', 'Dimensionality reduction', '#map', 1, '변수 수를 줄여 요약하는 일'),
             ('lab:concept/correlation', 'Concept', '상관계수', 'Correlation', '#s1', 2, '두 값이 직선으로 함께 오르내리는 정도'),
             ('lab:concept/projection', 'Concept', '투영 (그림자)', 'Projection', '#s2', 2, '좌표와 방향을 자리끼리 곱해 더한 값'),
             ('lab:method/pca', 'Method', '주성분 분석 (PCA)', 'Principal component analysis', '#s3', 2, '가장 많이 흔들리는 방향부터 새 축을 만듦', 'pearson1901lines'),
             ('lab:concept/eigenvalue', 'Concept', '고유값·고유벡터', 'Eigenvalue and eigenvector', '#s3', 3, '방향의 흔들림 크기와 방향'),
             ('lab:metric/explained-variance', 'Metric', '설명된 분산', 'Explained variance ratio', '#s3', 2, '전체 흔들림 중 그 방향의 몫'),
             ('lab:claim/two-axes-96', 'Claim', '두 축(PC1+PC2)이 흔들림의 96.1%를 남김 (PC1 87.6%)', 'Two axes keep 96.1% of variance', '#s3', 2, '', 'pyae2019fish'),
             ('lab:claim/size-shape-axes', 'Claim', 'PC1은 크기, PC2는 체형 축', 'PC1 = size, PC2 = body shape', '#s4', 2, ''),
             ('lab:concept/reconstruction', 'Concept', '복원과 복원 오차', 'Reconstruction error', '#s5', 2, '접은 좌표를 다시 펴서 원래 값과 비교'),
             ('lab:limitation/linear-folding', 'Limitation', '곧은 접기는 휜 관계(무게)를 놓침', 'Linear folding misses curved relations', '#s5', 2, ''),
             ('lab:claim/folding-loses-neighbors', 'Claim', '두 축 지도는 이웃 일치율 79.6%, 여섯 축은 92.3%', 'Folding loses neighbor fidelity', '#duel', 2, ''),
             ('lab:concept/eigenface', 'Concept', '고유 얼굴', 'Eigenface', '#s5', 3, '얼굴 사진의 주성분을 그림으로 본 것', 'turk1991eigenfaces'),
             ('lab:sim/u3-shadow', 'Simulation', '그림자 방향 찾기 실험장', 'Projection angle lab', '#s2', 2, '')]
    edges = [('lab:concept/dimensionality-reduction', 'broader', T + 'pca', '#map'), ('lab:method/pca', 'broader', T + 'pca', '#s3'), ('lab:concept/projection', 'broader', T + 'linear-algebra', '#s2'),
             ('lab:concept/eigenvalue', 'broader', T + 'linear-algebra', '#s3'), ('lab:concept/correlation', 'broader', T + 'probability-statistics', '#s1'), ('lab:concept/reconstruction', 'broader', T + 'pca', '#s5'),
             ('lab:limitation/linear-folding', 'broader', T + 'pca', '#s5'), ('lab:concept/eigenface', 'broader', T + 'embedding-space', '#s5'),
             ('lab:method/pca', 'partOf', 'lab:concept/dimensionality-reduction', '#s3'), ('lab:concept/correlation', 'prerequisiteOf', 'lab:method/pca', '#s1'), ('lab:concept/projection', 'prerequisiteOf', 'lab:method/pca', '#s2'),
             ('lab:concept/eigenvalue', 'partOf', 'lab:method/pca', '#s3'), ('lab:method/pca', 'measuredBy', 'lab:metric/explained-variance', '#s3'), ('lab:claim/two-axes-96', 'supports', 'lab:method/pca', '#s3'),
             ('lab:claim/size-shape-axes', 'supports', 'lab:method/pca', '#s4'), ('lab:method/pca', 'evaluatedBy', 'lab:concept/reconstruction', '#s5'), ('lab:method/pca', 'hasLimitation', 'lab:limitation/linear-folding', '#s5'),
             ('lab:claim/folding-loses-neighbors', 'supports', 'lab:limitation/linear-folding', '#duel'), ('lab:concept/eigenface', 'derivedFrom', 'lab:method/pca', '#s5'), ('lab:sim/u3-shadow', 'demonstratedBy', 'lab:concept/projection', '#s2')]
    P['03'] = ('03_folding', '3', '3장 · 접기 — 차원 축소', ['lab:method/pca', 'lab:concept/dimensionality-reduction'],
               ['pyae2019fish', 'ahn2026slides', 'pearson1901lines', 'turk1991eigenfaces'], nodes, edges, (p03.QUIZ, lambda q: '#s' + q[2]))
    # 4장
    import p04
    QMAP.update({'q41': 'lab:method/masked-modeling', 'q42': 'lab:method/autoencoder', 'q43': 'lab:method/map-knn', 'q44': 'lab:method/ood-alarm'})
    nodes = [('lab:concept/self-supervised-learning', 'Concept', '자기지도학습', 'Self-supervised learning', '#s1', 1, '일부를 가리고 맞히게 해 데이터 자신을 정답으로 씀'),
             ('lab:method/masked-modeling', 'Method', '마스크드 모델링 (가린 무게 맞히기)', 'Masked modeling', '#s1', 2, '값 하나를 가리고 나머지로 맞힘', 'devlin2019bert'),
             ('lab:claim/weight-volume-law', 'Claim', '가린 무게 규칙의 지수 합 ≈ 3 (부피처럼 자람), 시험 평균 빗나감 48.7g', 'Weight scales like volume', '#s1', 2, '', 'pyae2019fish'),
             ('lab:method/autoencoder', 'Method', '오토인코더', 'Autoencoder', '#s2', 2, '여섯 값→두 숫자→여섯 값으로 자신을 되살리도록 배우는 신경망', 'hinton2006reducing'),
             ('lab:concept/bottleneck', 'Concept', '병목', 'Bottleneck', '#s2', 2, '가운데 좁은 자리, 중요한 것만 남김'),
             ('lab:claim/ae-beats-pca', 'Claim', '시험 복원 오차: 오토인코더 0.0102, PCA 0.0581', 'Autoencoder reconstructs better than PCA', '#duel', 2, ''),
             ('lab:method/map-knn', 'Method', '지도 위 이웃 찾기 (k-NN)', 'k-NN on the latent map', '#s3', 2, '이웃 다섯의 이름표로 다수결, 이름표는 판단할 때만', 'cover1967nearest'),
             ('lab:claim/map-knn-acc', 'Claim', '이름표 없이 그린 지도 위 이웃 5마리 정답률 83.1%, 이름표 7장만이면 45.9%', 'Latent-map k-NN accuracy', '#s3', 2, ''),
             ('lab:method/ood-alarm', 'Method', '배운 범위 밖 경보 (지도 거리 + 네 축 복원 오차)', 'Out-of-distribution alarm', '#s4', 2, '두 자 중 하나라도 문턱(상위 1%)을 넘으면 답 보류'),
             ('lab:limitation/confident-wrong', 'Limitation', '다수결은 범위 밖에서도 자신 있게 답한다', 'Confident answers out of range', '#s4', 2, ''),
             ('lab:limitation/distribution-shift', 'Limitation', '측정 기준이 바뀌면 지도 밖으로 접힘', 'Measurement shift', '#s4', 2, ''),
             ('lab:sim/u4-checkstation', 'Simulation', '범위 밖 알아차리기 실험장', 'OOD lab', '#s4', 2, '')]
    edges = [('lab:concept/self-supervised-learning', 'broader', T + 'self-supervised', '#s1'), ('lab:method/masked-modeling', 'broader', T + 'self-supervised', '#s1'), ('lab:method/autoencoder', 'broader', T + 'autoencoder', '#s2'),
             ('lab:concept/bottleneck', 'broader', T + 'autoencoder', '#s2'), ('lab:method/map-knn', 'broader', T + 'knn', '#s3'), ('lab:method/ood-alarm', 'broader', T + 'anomaly-detection', '#s4'),
             ('lab:limitation/confident-wrong', 'broader', T + 'anomaly-detection', '#s4'), ('lab:limitation/distribution-shift', 'broader', T + 'distribution-shift', '#s4'),
             ('lab:method/masked-modeling', 'partOf', 'lab:concept/self-supervised-learning', '#s1'), ('lab:claim/weight-volume-law', 'supports', 'lab:method/masked-modeling', '#s1'),
             ('lab:method/autoencoder', 'partOf', 'lab:concept/self-supervised-learning', '#s2'), ('lab:concept/bottleneck', 'partOf', 'lab:method/autoencoder', '#s2'), ('lab:claim/ae-beats-pca', 'supports', 'lab:method/autoencoder', '#duel'),
             ('lab:claim/map-knn-acc', 'supports', 'lab:method/map-knn', '#s3'), ('lab:method/map-knn', 'hasLimitation', 'lab:limitation/confident-wrong', '#s3'), ('lab:limitation/confident-wrong', 'addressedBy', 'lab:method/ood-alarm', '#s4'),
             ('lab:limitation/distribution-shift', 'addressedBy', 'lab:method/ood-alarm', '#s4'), ('lab:sim/u4-checkstation', 'demonstratedBy', 'lab:method/ood-alarm', '#s4')]
    P['04'] = ('04_guessing', '4', '4장 · 맞히기 — 자기지도학습', ['lab:concept/self-supervised-learning', 'lab:method/autoencoder'],
               ['pyae2019fish', 'ahn2026slides', 'hinton2006reducing', 'devlin2019bert', 'cover1967nearest'], nodes, edges, (p04.QUIZ, lambda q: '#s' + q[2]))
    # 실전 연습장
    nodes = [('lab:sim/practice-shelf', 'Simulation', '진열대 정리 (군집 시뮬레이터)', 'Shelf clustering simulator', '#shelf', 2, '자와 진열대 수를 고르고 실루엣·대조 점수 확인'),
             ('lab:sim/practice-map', 'Simulation', '물고기 지도 만들기 (PCA 시뮬레이터)', 'PCA map simulator', '#map', 2, '표준화·축 수·변수 세트를 바꿔 남긴 흔들림 확인'),
             ('lab:sim/practice-check', 'Simulation', '검수대 (범위 밖·가린 무게 시뮬레이터)', 'Inspection station simulator', '#check', 2, '문턱을 바꿔 이상 물고기와 괜한 경보 확인'),
             ('lab:question/robust-conclusion', 'Question', '조건이 바뀌어도 결론이 유지되나?', 'Is the conclusion robust?', '#close', 2, ''),
             ('lab:limitation/threshold-tradeoff', 'Limitation', '문턱을 낮추면 괜한 경보, 높이면 놓침', 'Alarm threshold trade-off', '#check', 2, '')]
    edges = [('lab:sim/practice-shelf', 'demonstratedBy', T + 'clustering', '#shelf'), ('lab:sim/practice-map', 'demonstratedBy', T + 'pca', '#map'), ('lab:sim/practice-check', 'demonstratedBy', T + 'anomaly-detection', '#check'),
             ('lab:limitation/threshold-tradeoff', 'broader', T + 'anomaly-detection', '#check'), ('lab:sim/practice-check', 'raises', 'lab:limitation/threshold-tradeoff', '#check'),
             ('lab:question/robust-conclusion', 'addressedBy', 'lab:sim/practice-shelf', '#close'), ('lab:question/robust-conclusion', 'addressedBy', 'lab:sim/practice-map', '#close'), ('lab:question/robust-conclusion', 'addressedBy', 'lab:sim/practice-check', '#close')]
    P['practice'] = ('practice/index', '5', '마지막 장 · 실전 연습장 — 어시장 운영 시뮬레이터', ['lab:sim/practice-shelf', 'lab:sim/practice-check'], ['pyae2019fish', 'ahn2026slides'], nodes, edges, None)
    return P


def main():
    P = pages()
    report = []
    for key, (slug, number, title, about, refs, nodes, edges, qz) in P.items():
        quiz, qa = (qz if qz else (None, None))
        kg, rf, meta = build_page(slug, number, title, about, refs, nodes, edges, quiz, qa)
        meta['url'] = SITE + slug + '.html'
        if slug == 'practice/index': meta['url'] = SITE + 'practice/'
        d = os.path.join(ROOT, 'kg', slug.replace('/index', '') if slug != 'index' else 'index')
        os.makedirs(d, exist_ok=True)
        for n, o in (('kg.json', kg), ('refs.json', rf), ('meta.json', meta)):
            json.dump(o, open(os.path.join(d, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        html = os.path.join(ROOT, slug + '.html')
        orig = html + '.orig'
        open(orig, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read())
        subprocess.check_call(['python3', os.path.join(HERE, 'retrofit.py'), orig, '--kg', os.path.join(d, 'kg.json'), '--refs', os.path.join(d, 'refs.json'),
                               '--meta', os.path.join(d, 'meta.json'), '--backbone', '/home/claude/adminmrobo/ahnboat_lab_explainer/data/backbone_ai.json', '-o', html])
        rep = os.path.join(d, 'check_report.md')
        subprocess.call(['python3', os.path.join(HERE, 'check.py'), orig, html, '--backbone', '/home/claude/adminmrobo/ahnboat_lab_explainer/data/backbone_ai.json', '--report', rep])
        os.remove(orig)
        report.append((slug, open(rep, encoding='utf-8').read()))
    for s, r in report:
        print('=====', s); print(r[:1500])


if __name__ == '__main__':
    main()
