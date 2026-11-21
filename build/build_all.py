# 전체 다시 만들기: 페이지 6개 → 지식 색인·꾸러미 붙이기 → 점검
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__))
for p in ['p00', 'p01', 'p02', 'p03', 'p04', 'p05']:
    subprocess.check_call([sys.executable, os.path.join(H, p + '.py')])
subprocess.check_call([sys.executable, os.path.join(H, 'kg_build.py')])
