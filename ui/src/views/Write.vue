<script lang="ts">
import Editor from '@/components/Editor.vue';
import postApi from '../apis/post';
export default {
  name: 'Write',
  components: {
    Editor,
  },
  data() {
    return {
      content: '',
      title: '',
      type: 'md'
    };
  },
  methods: {
    handleSave(content: string) {
      this.content = content;
      postApi.savePostFile({
        title: this.title,
        content: this.content,
        type: this.type
      }).then(res => {
        console.log(res);
      });
    },
  },
};
</script>

<template>
  <t-card title="文档编辑" style="height: 80vh;overflow: scroll;">
    <t-form-item label="文档标题">
      <t-input v-model="title" />
    </t-form-item>
    <Editor v-model:content="content" @save="handleSave" />
  </t-card>
</template>