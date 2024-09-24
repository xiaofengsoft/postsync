# -*- coding: utf-8 -*-
from playwright.async_api import Page


async def get_page_local_storage(page: Page) -> dict:
    local_storage = await page.evaluate("""
            () => {
                const items = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            }
    """)
    return local_storage
