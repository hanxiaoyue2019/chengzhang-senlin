from playwright.sync_api import sync_playwright
import time
URL="http://localhost:8033/index.html"
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={"width":390,"height":844}); pg=ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(1)
    pg.screenshot(path="/workspace/cz_top.png")
    pg.evaluate("window.scrollTo(0,600)"); time.sleep(0.5)
    pg.screenshot(path="/workspace/cz_scrolled.png")
    # 检查 header 是否吸顶：滚动后 header 的 getBoundingClientRect().top 应≈0
    top=pg.evaluate("document.querySelector('header').getBoundingClientRect().top")
    print("滚动后 header top:", top)
    print("JS错误:", errs)
    b.close()
