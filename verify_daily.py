from playwright.sync_api import sync_playwright
import time, os
URL="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"index.html"))
NOW=int(time.time()*1000)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))

    # 第一天（当前时间）
    pg.clock.install(time=NOW)
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(0.4)

    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.3)
    pg.click("[data-act='addsubj']"); time.sleep(0.2)
    n1=len(pg.query_selector_all(".subj-group"))
    pg.click("#btn-edit"); time.sleep(0.3)
    pg.click(".task-check"); time.sleep(0.3)
    sun=pg.text_content("#s-sun")
    print("第一天: 科目数=%d 完成1项阳光=%s"%(n1,sun))
    day1=pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('chengzhang_forest_v1')).days)")
    print("第一天 days 键:", day1)

    # 第二天：把时钟拨到 +26 小时，重载
    pg.clock.install(time=NOW+26*3600*1000)
    pg.goto(URL); time.sleep(0.6)
    n2=len(pg.query_selector_all(".subj-group"))
    sun2=pg.text_content("#s-sun")
    print("第二天: 科目数=%d 阳光=%s"%(n2,sun2))

    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.3)
    pg.click("[data-act='addsubj']"); time.sleep(0.2)
    n2b=len(pg.query_selector_all(".subj-group"))
    day2=pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('chengzhang_forest_v1')).days)")
    print("第二天再加1科后: 科目数=%d  days键=%s"%(n2b,day2))

    # 切回第一天时钟，确认第一天副本仍含当时加的科目(5个)
    pg.clock.install(time=NOW)
    pg.goto(URL); time.sleep(0.6)
    n1b=len(pg.query_selector_all(".subj-group"))
    print("切回第一天: 科目数=%d (应为5，含当天加的)"%n1b)
    print("JS错误:", errs)
    b.close()
