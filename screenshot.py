from playwright.sync_api import sync_playwright
import time
URL="http://localhost:8033/index.html"
OUT="/workspace/chengzhang_preview.png"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":390,"height":844})
    pg.goto(URL); time.sleep(1)
    pg.screenshot(path=OUT, full_page=False)
    print("saved", OUT)
    b.close()
