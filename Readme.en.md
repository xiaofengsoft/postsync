<div align="center">
<img src="static/imgs/logo.png" width="200" height="200" /> 
<h3 align="center"> PostSync </h3> 
<p align="center"> Promoting the Development of Technical Articles </p> 
</div>

### Introduction

This is an open-source software for synchronizing articles, which allows you to sync your articles to multiple
platforms.

### Usage

Open your browser, log in to your accounts on various platforms: Juejin, CSDN, Zhihu, WeChat Official Account, Bilibili,
CNBlog, and your personal WordPress site.
Open the config.yaml file, configure your browser information and browser user data directory.
Run the command line:

``` shell
.\PostSync.exe -h
```

CopyInsert
Enter the command to use the software.

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
- Please exit the browser before using the software.

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

- [ ] Record the logs of the process.
- [ ] Specially handle the case of the specific exception.
- [ ] Specially handle the case of the specific column argument.
- [ ] Optimize the code typing structure.
- [ ] Optimize code document read and output.
- [ ] Not input if the arguments are not provided.
- [ ] Direct publishing to WeChat Official Account.
- [ ] Optimize inclusion search to approximate search.
- [ ] Connect to an already open browser instance.

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