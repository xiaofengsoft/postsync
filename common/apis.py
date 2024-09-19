# -*- coding: utf-8 -*-
from typing import TypedDict, Sequence, Optional


class PostPaths(TypedDict, total=True):
    docx: str
    html: str
    md: str


class PostContents(TypedDict, total=False):
    docx: str
    html: str
    md: str


class PostArguments(TypedDict, total=True):
    title: Optional[str]
    cover: Optional[str]
    tags: Optional[Sequence[str]]
    columns: Optional[Sequence[str]]
    sites: Optional[Sequence[str]]
    category: Optional[str]
    topic: Optional[str]
    file: str
    digest: Optional[str]


class Post(TypedDict, total=True):
    title: str
    paths: PostPaths
    cover: Optional[str]
    tags: Optional[Sequence[str]]
    columns: Optional[Sequence[str]]
    sites: Optional[Sequence[str]]
    category: Optional[str]
    topic: Optional[str]
    digest: Optional[str]
    contents: PostContents
