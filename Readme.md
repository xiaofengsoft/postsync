<div align="center">
<img height="200" src="static/imgs/logo.png" width="200"/>
<h3 align="center">
    PostSync
    </h3>
<p align="center">
        促进技术文章发展
    </p>
</div>

### 介绍

这是一个开源的同步文章的软件，你可以使用它来同步你的文章到多个平台。  
目前支持的平台有掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台。  
支持GUI界面或者命令行界面来使用该软件。

### 使用

#### GUI版本

1. 打开PostSyncGUI.exe文件

#### 命令行版本

1. 打开config.yaml文件，配置你的浏览器信息、浏览器用户数据目录、可执行浏览器路径
   ```yaml
   executable:
     path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe # 浏览器可执行文件路径
   default:
     browser: msedge # 选择使用的浏览器 (msedge,chrome,firefox)
   ```
   &gt; 可以联网查找浏览器数据目录所在位置
2. 运行PostSync.exe文件命令行
   根据需要上传的平台类型手动登录
   系统会自动检测是否登录成功
   成功后会自动保存登录信息并关闭页面
3. 再次运行命令行

### 开发

#### 配置debug

打开`config.yaml`文件,将`app/debug`设置为`True`

#### 打包

``` bash
python make.py
```

### 注意事项

- 使用标签分类等功能请确保您在相关平台上已经创建相应的标签分类
- 文件路径带有空格请使用英文双引号包裹

### 功能

- 自动同步文章到掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台并返回生成文章链接
- 支持多协程，异步上传文章
- 支持包含查找，大小写模糊匹配
- 支持md,html,docx文件
- 支持自定义默认配置
- 支持命令行界面，GUI界面
- 自定义标题、标签、分类、专栏、封面、摘要

### 优化任务

- [ ] 搭配前端网页界面接口
- [ ] 搭配图床接口
- [ ] 算法处理内容提取摘要和标签
- [ ] 记录失败日志
- [ ] 未填写参数不输入网站处理
- [ ] 公众号直接发布
- [ ] 包含查找优化为近似查找

### 开发规范

- entity包下的新增社区嘞应继承Community类
- 新增社区类的命令应为首字母大写其余字母全部小写
- 代码风格遵循PEP8规范

### 关于作者

作者本人目前就读于中原工学院，是一名超级热爱编程的本科生
喜欢各种运动和各种音乐
- 邮箱：<xiaofengs@yeah.net>
- 网站: <https: yunyicloud.cn="">

公众号: 

![云奕科软公众号二维码](static/imgs/official-account.jpg)

### 打赏

&gt; 如果觉得本软件对您有帮助，不如请我喝杯☕！

![微信支付](static/imgs/reward-wechat.jpg)

### 鸣谢
- 感谢JetBrains公司提供的免费学生许可证
- 感谢FittenCode AI智能代码辅助助手的大力相助</https:></xiaofengs@yeah.net>