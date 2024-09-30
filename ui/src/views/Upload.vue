<script lang="ts">
import { s } from 'vite/dist/node/types.d-aGj9QkWt';

export default {
  data() {
    return {
      siteAlias: [
        { label: '全选', checkAll: true },
        { label: '稀土掘金', value: 'juejin' },
        { label: 'CSDN', value: 'csdn' },
        { label: '知乎', value: 'zhihu' },
        { label: '博客园', value: 'cnblog' },
        { label: 'Bilibili', value: 'bilibili' },
        { label: '微信公众号', value: 'wechat' },
        { label: 'WordPress', value: 'wordpress' }
      ],
      siteValues: [],
      post: [],
    }
  },
  methods: {
    chooseFilePost() {

    }
  }
}
</script>
<template>
  <t-card style="padding: 5% 2%;">
    <t-form labelAlign="left">
      <t-form-item label="选择文件" name="file">
        <t-upload action="" v-model="post" @success="chooseFilePost" theme="file-input" placeholder="未选择文件"></t-upload>
      </t-form-item>
      <t-form-item label="文章标题" name="name" initialData="TDesign">
        <t-input placeholder="请输入标题" />
      </t-form-item>
      <t-form-item label="上传网站" name="course"
        initialData="['juejin', 'csdn', 'zhihu', 'cnblog', 'bilibili', 'wechat', 'wordpress']">
        <t-select v-model="siteValues" :options="siteAlias" placeholder="请选择要上传的网站" multiple />
      </t-form-item>
    </t-form>
  </t-card>
</template>