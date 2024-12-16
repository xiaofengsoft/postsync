<template>
  <t-list-item>
    <template #content>
      <div class="post-item">
        <div class="post-title">{{ name }}</div>
        <div class="post-actions">
          <t-button theme="primary" variant="text" @click="uploadPostFile">上传</t-button>
          <t-button theme="default" variant="text" @click="editPostFile">编辑</t-button>
          <t-button theme="danger" variant="text" @click="deletePostFile">删除</t-button>
        </div>
      </div>
    </template>
  </t-list-item>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue';
import { Post } from '../types/post';
import { useRouter } from 'vue-router';
const post = defineProps<Post>();
const router = useRouter();
const emit = defineEmits();
import dashboardApi from '../apis/dashboard';
import { MessagePlugin, DialogPlugin } from 'tdesign-vue-next';

const uploadPostFile = () => {
  router.push({ path: '/upload', query: { postFile: JSON.stringify(post) } });
};

const editPostFile = () => {
  router.push({ path: '/write', query: { path: post.path } });
};

const deletePostFile = () => {
  const confirmDialog = DialogPlugin.confirm({
    header: '删除文章',
    body: `确定删除文章: ${post.name}`,
    onConfirm: async () => {
      try {
        const response = await dashboardApi.deletePostFile(post.path);
        if (response.data.code === 0) {
          MessagePlugin.success('删除成功');
          emit('refresh');
        } else {
          MessagePlugin.error('删除失败');
        }
      } catch {
        MessagePlugin.error('删除失败');
      } finally {
        confirmDialog.hide();
      }
    },
    onCancel: () => confirmDialog.hide()
  });
};
</script>

<style scoped>
.post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  font-weight: bold;
}

.post-actions {
  display: flex;
  gap: 10px;
}
</style>
