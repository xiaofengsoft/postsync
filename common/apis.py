# -*- coding: utf-8 -*-
from typing import TypedDict, Sequence, Optional, Literal, List, Dict, Union


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


class NameValueDict(TypedDict, total=True):
    name: str
    value: str


class LocalStorageData(TypedDict, total=True):
    origin: str
    localStorage: List[NameValueDict]


class CookieData(TypedDict, total=True):
    name: str
    value: str
    domain: str
    path: str
    expires: Union[str, int, float,None]
    httpOnly: Union[str,bool,None]
    secure: Union[str,bool,None]
    sameSite: Union[str,None]


class StorageType(TypedDict, total=True):
    type: Literal["local", "cookie"]
    domain: str
    name: str
    value: Optional[str]


class StorageData(TypedDict, total=True):
    cookies: List[CookieData]
    origins: List[LocalStorageData]





