1. 首先确保您已经登录WordPress后台
2. 打开 `config.yaml` 文件，做出如下修改：
    ```yaml
    wordpress:
      enable: True  # 是否启用WordPress同步
      domain: yunyicloud.cn  # WordPress用户名
      url: https://yunyicloud.cn  # WordPress博客地址
    ```
    > 请将 `url` 改为你的WordPress博客地址  
   > 或者在GUI界面中点击设置修改 `wordpress.enable` `wordpress.domain` `wordpress.url` 选项
3. 保存文件或者点击保存按钮
