<script setup lang="ts">
import { ref } from 'vue';
import postApi from "../apis/post";
import { MessagePlugin } from 'tdesign-vue-next';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { DialogPlugin } from 'tdesign-vue-next';
const siteAlias = ref([
  { label: '全选', checkAll: true },
  { label: '稀土掘金', value: 'juejin' },
  { label: 'CSDN', value: 'csdn' },
  { label: '知乎', value: 'zhihu' },
  { label: '博客园', value: 'cnblog' },
  { label: 'Bilibili', value: 'bilibili' },
  { label: '微信公众号', value: 'wechat' }
]);

const post = ref({
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
});
const router = useRouter();
onMounted(() => {
  const tempPost = router.currentRoute.value.query.postFile as string;
  if (tempPost) {
    const postFile = JSON.parse(tempPost)
    post.value.file = postFile.path;
    post.value.title = postFile.name;
  }
});
const chooseFilePost = () => {
  postApi.choosePost().then(res => {
    console.log(res);
    post.value.file = res.data.data[0];
  });
};

const chooseFileCover = () => {
  postApi.chooseCover().then(res => {
    console.log(res);
    post.value.cover = res.data.data[0];
  });
};

const uploadPost = () => {
  console.log(post.value);
  postApi.uploadPost(post.value).then(res => {
    if (res.data.code == 0) {
      const postedList = (res.data.data as Array<any>).map((item) => {
        return `${item[0]}：${item[1]}`;
      }).join('\n');
      DialogPlugin.confirm({
        header: '提示',
        body: postedList,
        onConfirm: () => {
        }
      })
    } else {
      DialogPlugin.confirm({
        header: '提示',
        body: res.data.message,
        onConfirm: () => {
        }
      })
    }
  });
};

const extractPost = () => {
  postApi.extractPost(post.value.file).then((res) => {
    if (res.data.code == -1) {
      MessagePlugin.error({ content: res.data.message })
    } else {
      post.value.tags = res.data.data.tags
      post.value.digest = res.data.data.digest
    }
  })
}
</script>

<template>
  <t-card title="上传文章">
    <template #actions>
      <t-button @click="extractPost">
        提取摘要标签
      </t-button>
    </template>
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

      <t-form-item label=" 上传网站" name="site" initialData="['juejin', 'csdn', 'zhihu', 'cnblog', 'bilibili', 'wechat']">
        <t-select v-model="post.sites" :options="siteAlias" placeholder="请选择要上传的网站" multiple />
      </t-form-item>
      <t-button @click="uploadPost" style="margin-top: 20px;background-color: var(--td-success-color);"
        block>点击上传</t-button>
    </t-form>
  </t-card>
</template>