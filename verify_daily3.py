from playwright.sync_api import sync_playwright
import time, os
URL="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"index.html"))

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); time.sleep(0.5)
    print("载入后 JS错误:", errs)
    pg.click("#btn-edit"); time.sleep(0.3)
    print("弹密码框后 pwd 可见:", pg.is_visible("#ov-pwd"))
    pg.fill("#pwd-input","1234"); pg.click("#pwd-ok"); time.sleep(0.5)
    print("进入编辑后 edit-hint:", len(pg.query_selector_all(".edit-hint")))
    print("进入编辑后 addsubj:", len(pg.query_selector_all("[data-act='addsubj']")))
    print("此时 JS错误:", errs)
    print("btn-edit 文本:", pg.text_content("#btn-edit"))
    b.close()
