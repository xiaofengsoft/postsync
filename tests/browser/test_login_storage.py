# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import pytest
import os


@pytest.mark.parametrize("username,password",[("17629851627","Zyf15682828516")])
def test_login_storage(username,password):
    os.chdir("../../")
    print(os.getcwd())
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://juejin.cn/")
        page.get_by_role("button", name="登录 注册").click()
        page.get_by_text("密码登录").click()
        page.get_by_placeholder("请输入邮箱/手机号（国际号码加区号）").fill(username)
        page.get_by_placeholder("请输入密码").fill(password)
        page.get_by_role("button", name="登录", exact=True).click()
        page.pause()
        context.storage_state(path="tests/data/juejin.json")
        context.close()


def test_login():
    os.chdir("../../")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()
        page = context.new_page()
        context.storage_state(path="tests/data/juejin.json")
        page.goto("https://juejin.cn/")
        page.pause()

