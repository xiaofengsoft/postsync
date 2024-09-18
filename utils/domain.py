# -*- coding: utf-8 -*-

def get_domain(url: str):
    """
    Extract domain name from a URL.
    """
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.netloc


def join_url_paths(base_url: str, paths: list) -> str:
    """
    Join base URL and paths to create a new URL.
    """
    from urllib.parse import urljoin
    return urljoin(base_url, '/'.join(paths))