<div align="center">
  <img src="static/imgs/logo.png" width="200" height="200">
    <h3 align="center">
    PostSync
    </h3>
    <p align="center">
        促进技术文章发展
    </p>
</div>

### 介绍

这是一个开源的同步文章的软件，你可以使用它来同步你的文章到多个平台。

### 使用

1. 打开浏览器，登录各个平台的账号，掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress
2. 打开config.yaml文件，配置你的浏览器信息以及浏览器用户数据目录
3. 运行命令行：
    ``` bash
    .\PostSync.exe -h
    ```
4. 输入命令即可使用



### 开发

#### 配置debug

打开`config.yaml`文件,将`app/debug`设置为`True`

#### 打包

``` bash
pyinstaller PostSync.spec
```
接着拷贝config.yaml到dist/PostSync目录下，命令行运行PostSync.exe即可

### 注意事项

- 在使用前请确保已经登录各个平台的账号
- 使用标签分类等功能请确保您在相关平台上已经创建相应的标签分类
- 使用前请退出浏览器


### 功能

- 自动同步文章到掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台并返回生成文章链接
- 支持多协程，异步上传文章
- 支持包含查找，大小写模糊匹配
- 支持md,html文件
- 支持自定义默认配置
- 支持命令行界面
- 自定义标签、分类、专栏、封面、摘要

### 优化任务

- [ ] 记录失败日志
- [ ] 具体异常具体处理
- [ ] 具体栏目参数具体处理
- [ ] 优化代码类型结构
- [ ] 优化代码文档读取生成
- [ ] 未填写参数不输入网站处理
- [ ] 公众号直接发布
- [ ] 连接已经打开的浏览器实例
- [ ] 包含查找优化为近似查找

### 开发规范

- entity包下的新增社区嘞应继承Community类
- 新增社区类的命令应为首字母大写其余字母全部小写
- 代码风格遵循PEP8规范

### 技术架构

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