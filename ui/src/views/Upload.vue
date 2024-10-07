<script lang="ts">
import postApi from "../apis/post";
import { MessagePlugin } from 'tdesign-vue-next';

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
      post: {
        file: '',
        title: '',
        digest: '',
        content: '',
        sites: [],
        category: [],
        topic: '',
        cover: '',
        tags: [],
        columns: [],
      },
    }
  },
  methods: {
    chooseFilePost() {
      postApi.choosePost().then(res => {
        console.log(res);
        this.post.file = res.data.data[0];
      })
    },
    chooseFileCover() {
      postApi.chooseCover().then(res => {
        console.log(res);
        this.post.cover = res.data.data[0];
      })
    },
    uploadPost() {
      console.log(this.post);
      postApi.uploadPost(this.post).then(res => {
        console.log(res);
        if (res.data.code == 0) {
          MessagePlugin.success({ content: '上传成功' })
        } else {
          MessagePlugin.error({ content: res.data.message })
        }
      })
    }
  }
}
</script>
<template>
  <t-card style="max-height: 81vh;overflow-y: scroll;" title="上传文章">
    <t-form labelAlign="left">
      <t-form-item label="文件路径" name="file">
        <t-input placeholder="请选择文件" v-model="post.file" style="margin-right: 10px;" />
        <t-button type="primary" @click="chooseFilePost" v-click-once>选择文件</t-button>
      </t-form-item>
      <t-form-item label="文章标题" name="title">
        <t-input placeholder="请输入标题" v-model="post.title" />
      </t-form-item>
      <t-form-item label="文章摘要" name="digest">
        <t-textarea placeholder="请输入摘要" v-model="post.digest" :autosize="{ minRows: 4, maxRows: 7 }">
        </t-textarea>
      </t-form-item>
      <t-form-item label="文章分类" name="category">
        <t-input placeholder="请输入分类" v-model="post.category" />
      </t-form-item>
      <t-form-item label="封面图" name="file">
        <t-input placeholder="请选择文件" v-model="post.cover" style="margin-right: 10px;" />
        <t-button type="primary" @click="chooseFileCover" v-click-once>选择文件</t-button>
      </t-form-item>
      <t-form-item label="文章话题" name="topic">
        <t-input placeholder="请输入话题" v-model="post.topic" />
      </t-form-item>
      <t-form-item label="文章标签" name="tags">
        <t-tagInput clearable v-model="post.tags" />
      </t-form-item>
      <t-form-item label="文章栏目" name="columns">
        <t-tagInput clearable v-model="post.columns" />
      </t-form-item>

      <t-form-item label=" 上传网站" name="site"
        initialData="['juejin', 'csdn', 'zhihu', 'cnblog', 'bilibili', 'wechat', 'wordpress']">
        <t-select v-model="post.sites" :options="siteAlias" placeholder="请选择要上传的网站" multiple />
      </t-form-item>
      <t-button @click="uploadPost" style="margin-top: 20px;" block variant="outline">点击上传</t-button>
    </t-form>
  </t-card>
</template>