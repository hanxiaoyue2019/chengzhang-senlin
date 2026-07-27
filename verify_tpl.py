from playwright.sync_api import sync_playwright
import time, os
URL="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"index.html"))

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(0.5)

    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.3)
    # 加科目、改模板按钮、恢复按钮是否存在
    print("savetpl 按钮:", len(pg.query_selector_all("[data-act='savetpl']")))
    print("reset 按钮:", len(pg.query_selector_all("[data-act='reset']")))

    # 加一个科目后，点"存为每日模板"
    pg.click("[data-act='addsubj']"); time.sleep(0.2)
    before=len(pg.query_selector_all(".subj-group"))
    pg.on("dialog", lambda d: d.accept())
    pg.click("[data-act='savetpl']"); time.sleep(0.3)
    # 检查 state.subjects 模板是否变成5科
    tpl=pg.evaluate("JSON.parse(localStorage.getItem('chengzhang_forest_v1')).subjects.length")
    print("存模板前科目=%d 模板科目数=%d"%(before,tpl))

    # 点"恢复今天的默认"应回退到模板(5科，因为已存模板)
    pg.click("[data-act='reset']"); time.sleep(0.3)
    print("恢复今天默认后 .subj-group:", len(pg.query_selector_all(".subj-group")))
    print("JS错误:", errs)
    b.close()
