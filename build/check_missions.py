# 실전 연습장 미션 판정 검사: 정답 조작을 흉내 내고 판정이 바뀌는지 본다 (스킬 6-1 검사)
import os, json, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        await page.route('**/fonts.g*/**', lambda r: r.abort())
        await page.goto('file://' + os.path.join(ROOT, 'practice/index.html'))
        await page.wait_for_timeout(800)
        out = {}
        js = '''async (steps)=>{const SC=window.LAB_PRACTICE;const res=[];
          for(const [scene,opt] of steps){document.querySelector('[data-tab="'+scene+'"]').click();await new Promise(r=>setTimeout(r,60));SC[scene].set(opt);
            res.push({scene,opt,state:SC[scene].M.state.slice(),kpi:[...document.querySelectorAll('#kp_'+scene+' .kpi b')].map(e=>e.textContent)});}
          return res;}'''
        steps = [
            ['shelf', {'k': 4}], ['shelf', {'k': 3}], ['shelf', {'feat': 'raw', 'k': 3}], ['shelf', {'env': 0.08, 'feat': 'ratio', 'k': 3}], ['shelf', {'env': 0.04, 'feat': 'six', 'k': 2}],
            ['map', {'k': 2}], ['map', {'std': True, 'set': 'six', 'k': 1}], ['map', {'std': True, 'k': 2}], ['map', {'set': 'four', 'std': True, 'k': 2}],
            ['check', {'mult': 6.0, 'tol': 80}], ['check', {'mult': 3.0, 'tol': 50}], ['check', {'mult': 0.5}], ['check', {'day': 'mixed', 'mult': 3.0, 'tol': 50}],
            ['check', {'day': 'normal', 'mult': 2.0, 'tol': 40}], ['check', {'day': 'mixed', 'mult': 5.0, 'tol': 70}],
        ]
        r = await page.evaluate(js, steps)
        for x in r:
            print(x['scene'], json.dumps(x['opt']), x['state'], x['kpi'])
        await b.close()

asyncio.run(main())
