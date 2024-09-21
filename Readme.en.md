<div align="center">
  <img src="static/imgs/logo.png" width="200" height="200" /> 
  <h3 align="center"> PostSync </h3> 
  <p align="center"> Promoting the Development of Technical Articles </p> 
</div>

### Introduction

This is an open-source software for synchronizing articles, which allows you to sync your articles to multiple
platforms.

### Usage

1. Open your browser, log in to your accounts on various platforms: Juejin, CSDN, Zhihu, WeChat Official Account, Bilibili,
CNBlog, and your personal WordPress site.
2. Open the config.yaml file, configure your browser information, browser user data directory and executable file path.
   ```yaml
   user:
     dir: C:\Users\xiaof\AppData\Local\Microsoft\Edge\User Data  # 浏览器用户数据目录
   executable:
     path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe # 浏览器可执行文件路径
   default:
     browser: msedge # 选择使用的浏览器 (msedge,chrome,firefox)
   ```
   > Please search for the browser user data directory with the internet.
3. Run the command line:
  ``` shell
  .\PostSync.exe -h
  ```
4. Enter the command to use the software.

### Development

Debug Configuration
Open the config.yaml file and set app/debug to True.

#### Packaging

pyinstaller PostSync.spec
CopyInsert
Then copy config.yaml to the dist/PostSync directory, and run PostSync.exe from the command line.

### Notes

- Ensure you have logged in to your accounts on all platforms before using the software.
- Ensure you have created the corresponding tags and categories on the relevant platforms if you plan to use tagging and
  categorization features.

### Features

- Automatically sync articles to Juejin, CSDN, Zhihu, WeChat Official Account, Bilibili, CNBlog, and personal WordPress
  platforms, returning the generated article links.
- Support for multi-coroutine, asynchronous uploading of articles.
- Support for inclusion search, case-insensitive fuzzy matching.
- Support for .md and .html files.
- Support for custom default configurations.
- Support for command-line interface.
- Customizable tags, categories, columns, covers, and abstracts.

### Optimization Tasks

- [ ] Fix the bug of image upload limited to one repeatedly.
- [ ] Optimize the checking login status of platforms.
- [ ] Materialize the timeout
- [ ] Record the logs of the process.
- [ ] Specially handle the case of the specific exception.
- [ ] Specially handle the case of the specific column argument.
- [ ] Not input if the arguments are not provided.
- [ ] Direct publishing to WeChat Official Account.
- [ ] Optimize inclusion search to approximate search.

### Development Guidelines

New community classes under the entity package should inherit from the Community class.
The naming of new community classes should be in camelCase.
Code style follows PEP8 standards.

### Technical Architecture

- pytest
- requests
- playwright
- faker
- pyyaml
- markdown
- beautifulsoup4
- argparse
- nest-asyncio
- pyinstaller
- customtkinter