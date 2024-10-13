<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Editor from '@/components/Editor.vue';
import postApi from '../apis/post';
import { MessagePlugin } from 'tdesign-vue-next';
import { useRouter, useRoute } from 'vue-router';
import writeApi from '../apis/write';
const content = ref('');
const title = ref('');
const type = ref('md');

const handleSave = () => {
  postApi.savePostFile({
    title: title.value,
    content: content.value,
    type: type.value
  }).then(res => {
    if (res.data.code === 0) {
      MessagePlugin.success('保存成功');
    } else {
      MessagePlugin.error(res.data.message);
    }
    console.log(res.data);
  });
};
const router = useRouter();
const handleUpload = () => {
  postApi.savePostFile({
    title: title.value,
    content: content.value,
    type: type.value
  }).then(res => {
    if (res.data.code === 0) {
      MessagePlugin.success('保存成功');
      router.push({
        path: '/upload',
        query: {
          postFile: JSON.stringify({
            name: title.value,
            path: res.data.data.path,
          })
        }
      });
    } else {
      MessagePlugin.error(res.data.message);
    }
    console.log(res.data);
  });

};
const route = useRoute();
onMounted(() => {
  const path = route.query.path as string;
  if (path) {
    writeApi.loadPostFile(path).then((res: any) => {
      title.value = res.data.data.title;
      content.value = res.data.data.content;
    });
  }
});

</script>

<template>
  <t-card title="文档编辑" style="width: 100%;">
    <template #actions>
      <t-button type="primary" @click="handleSave">保存</t-button>
      <t-button type="info" style="margin-left: 10px;" @click="handleUpload">上传</t-button>
    </template>
    <t-form-item label="文档标题">
      <t-input v-model="title" />
    </t-form-item>
    <Editor v-model:content="content" @save="handleSave" />
  </t-card>
</template>
