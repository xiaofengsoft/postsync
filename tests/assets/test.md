
![SyncTo](imgs/logo.png)
<h1 align="center">PostSync</h1>

<p align="center">
  促进技术文章发展
</p>

### 介绍

这是一个开源的同步文章的软件，你可以使用它来同步你的文章到多个平台。

### 技术架构

- pytest
- requests
- playwright
- faker
- pyyaml
- markdown
- beautifulsoup4
- argparse


### 功能

- 自动同步文章到掘金、CSDN、知乎 等平台并返回生成文章链接
- 支持多协程，异步上传文章
- 支持包含查找，大小写模糊匹配
- 支持md,html,纯文本文件
- 支持自定义配置
- 支持命令行界面


### 优化任务

- [ ] 优化协程为AsyncContextManager管理器 
- [ ] 未匹配到元素异常捕获处理
- [ ] 包含查找优化为近似查找
- [ ] 增加图形化界面