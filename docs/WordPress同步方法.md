1. 登录WordPress后台
2. 打开 `config.yaml` 文件，做出如下修改：
    ```yaml
    wordpress:
      enable: True  # 是否启用WordPress同步
      url: https://yunyicloud.cn  # WordPress博客地址
    ```
    > 请将 `url` 改为你的WordPress博客地址
3. 保存并关闭 `config.yaml` 文件
4. 重新运行即可