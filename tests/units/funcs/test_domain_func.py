# -*- coding: utf-8 -*-
import pytest
from utils.domain import get_domain


@pytest.mark.parametrize("url , expected", [
    ("https://www.google.com", "www.google.com"),
    ("https://google.com", "google.com"),
    ("https://yunyicloud.cn","yunyicloud.cn"),
])
def test_get_domain(url: str, expected: str):
    assert get_domain(url) == expected