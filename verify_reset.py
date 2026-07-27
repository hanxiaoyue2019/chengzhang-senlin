from playwright.sync_api import sync_playwright
import time, os
URL="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"index.html"))
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(0.5)

    def nsubj(): return len(pg.query_selector_all(".subj-group"))
    print("默认科目数:", nsubj())

    # 进入编辑
    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.3)

    # 添加两个科目
    pg.click("[data-act='addsubj']"); time.sleep(0.2)
    pg.click("[data-act='addsubj']"); time.sleep(0.2)
    print("添加2科目后:", nsubj())

    # 点恢复默认（确认）
    pg.on("dialog", lambda d: d.accept())
    pg.click("[data-act='reset']"); time.sleep(0.3)
    print("恢复默认后科目数:", nsubj())

    # 退出编辑
    pg.click("#btn-edit"); time.sleep(0.4)
    print("退出后 edit-hint=%d mini-del=%d"%(len(pg.query_selector_all(".edit-hint")),len(pg.query_selector_all(".mini-del"))))
    print("JS错误:", errs)
    b.close()
