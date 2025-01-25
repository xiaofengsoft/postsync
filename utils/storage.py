# -*- coding: utf-8 -*-
from common import constant as c
from playwright.async_api import Page
import yaml
from utils.load import get_root_path


def storage_config():
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(c.config, file, default_flow_style=False, encoding='utf-8',
                  Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True)


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
