from playwright.sync_api import sync_playwright
import time, os
URL="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"index.html"))

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(0.5)

    # 进入编辑，加科目
    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.3)
    print("编辑中 addsubj 数:", len(pg.query_selector_all("[data-act='addsubj']")))
    pg.click("[data-act='addsubj']"); time.sleep(0.3)
    print("加1科后 .subj-group:", len(pg.query_selector_all(".subj-group")))
    # 完成1项
    pg.click("#btn-edit"); time.sleep(0.3)
    pg.click(".task-check"); time.sleep(0.3)
    print("阳光:", pg.text_content("#s-sun"))
    # 检查 days 结构
    st=pg.evaluate("JSON.parse(localStorage.getItem('chengzhang_forest_v1'))")
    print("days键:", list(st['days'].keys()), "今天done:", st['days'][list(st['days'].keys())[0]]['done'])
    print("JS错误:", errs)
    b.close()
