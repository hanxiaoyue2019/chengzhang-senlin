import subprocess, sys, time, os
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    from playwright.sync_api import sync_playwright

URL = "file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL)
    pg.evaluate("localStorage.clear()")
    pg.reload()
    time.sleep(0.5)

    # 完成第一项作业 -> 阳光应 +10
    sun0 = pg.text_content("#s-sun")
    pg.click(".task-check")
    time.sleep(0.3)
    sun1 = pg.text_content("#s-sun")
    print("阳光: %s -> %s" % (sun0, sun1))

    # 切到森林看是否种了一棵树
    pg.click("nav button:has-text('森林')")
    time.sleep(0.3)
    plots = pg.query_selector_all("#tab-garden .plot")
    grown = sum(1 for pl in plots if "locked" not in (pl.get_attribute("class") or ""))
    print("森林格子数=%d 已种=%d" % (len(plots), grown))

    # 切回首页，进入编辑，改名第一个科目
    pg.click("nav button:has-text('首页')")
    time.sleep(0.2)
    pg.click("#btn-edit"); time.sleep(0.2)
    pg.fill("#pwd-input", "1234"); pg.click("#pwd-ok"); time.sleep(0.3)
    pg.on("dialog", lambda d: d.accept("【改名测试】"))
    pg.click(".subj-name[data-renames='0']")
    time.sleep(0.5)
    newname = pg.text_content(".subj-name[data-renames='0']")
    print("改名后科目0:", newname)

    print("JS错误:", errors)
    b.close()
