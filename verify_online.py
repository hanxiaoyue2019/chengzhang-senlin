from playwright.sync_api import sync_playwright
import time
URL="https://hanxiaoyue2019.github.io/chengzhang-senlin/"
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(ignore_https_errors=True)
    pg=ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); time.sleep(1.5)
    pg.click("#btn-edit"); time.sleep(0.3)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.4)
    print("线上-进入编辑: edit-hint=%d mini-del=%d"%(len(pg.query_selector_all(".edit-hint")),len(pg.query_selector_all(".mini-del"))))
    pg.click("#btn-edit"); time.sleep(0.5)  # 退出
    print("线上-退出编辑: edit-hint=%d mini-del=%d add-btn=%d"%(len(pg.query_selector_all(".edit-hint")),len(pg.query_selector_all(".mini-del")),len(pg.query_selector_all(".add-btn"))))
    print("JS错误:",errs)
    b.close()
