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
    time.sleep(0.5)

    def mini_del():
        return pg.query_selector_all(".mini-del")

    def count(sel):
        return len(pg.query_selector_all(sel))

    # 进入家长编辑（密码默认 1234）
    pg.click("#btn-edit")
    time.sleep(0.3)
    pg.fill("#pwd-input", "1234")
    pg.click("#pwd-ok")
    time.sleep(0.4)

    in_edit = count(".edit-hint")
    del_subj = count("[data-act='delsubj']")
    add_task = count("[data-act='addtask']")
    add_subj = count("[data-act='addsubj']")
    print("进入编辑: edit-hint=%d 删除科目=%d 添加事项=%d 添加科目=%d" % (
        in_edit, del_subj, add_task, add_subj))

    # 添加新科目
    before = count(".subj-group")
    pg.click("[data-act='addsubj']")
    time.sleep(0.3)
    after = count(".subj-group")
    print("添加科目: %d -> %d" % (before, after))

    # 添加事项（第一个科目）
    before_t = count(".task-card")
    pg.click("[data-act='addtask'][data-s='0']")
    time.sleep(0.3)
    after_t = count(".task-card")
    print("添加事项: %d -> %d" % (before_t, after_t))

    # 删除第一个科目的第一个事项
    before_d = count(".task-card")
    pg.click("[data-act='deltask'][data-s='0']")
    time.sleep(0.3)
    after_d = count(".task-card")
    print("删除事项: %d -> %d" % (before_d, after_d))

    # 退出编辑
    pg.click("#btn-edit")
    time.sleep(0.4)
    print("退出编辑后: edit-hint=%d .mini-del=%d .add-btn=%d" % (
        count(".edit-hint"), count(".mini-del"), count(".add-btn")))

    print("JS错误:", errors)
    b.close()
