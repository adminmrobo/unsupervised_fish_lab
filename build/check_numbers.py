# 페이지 안 계산값과 data/results.json(scikit-learn) 대조 + 대결 결과 확인
import os, json, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, 'data', 'results.json')))


async def duel(page, did):
    await page.evaluate("document.querySelector('#%s .run').click()" % did)
    await page.wait_for_timeout(300)
    return await page.evaluate("[...document.querySelectorAll('#%s .bar .v')].map(e=>e.textContent).concat([document.querySelector('#%s .vtext').textContent])" % (did, did))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        await page.route('**/fonts.g*/**', lambda r: r.abort())
        for f, did, extra in [('01_no_answer_key.html', 'd1', None), ('02_grouping.html', 'd2', None),
                              ('03_folding.html', 'd3', None), ('04_guessing.html', 'd4', None)]:
            await page.goto('file://' + os.path.join(ROOT, f)); await page.wait_for_timeout(700)
            print(f, 'duel', await duel(page, did))
            if extra:
                print('   page value', await page.evaluate(extra))
        print('python: nn_agree', R['nn_agree'], 'kmr3 sil', R['kmr']['3']['sil'], 'k7', R['kmr']['7']['sil'], 'evr', R['pca']['evr'])
        print('python: nn_agree_pc', R['nn_agree_pc'], 'ae/pca', R['ae_vs_pca']['ae_test_mse'], R['ae_vs_pca']['pca2_test_mse'], 'knn_map', R['knn_map'])
        await b.close()

asyncio.run(main())
