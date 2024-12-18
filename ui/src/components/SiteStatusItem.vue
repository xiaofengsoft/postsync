<template>
  <div class="site-status-item">
    <t-tag :theme="item.status ? 'success' : 'danger'">{{ item.name }}</t-tag>
    <t-button v-if="!item.status" theme="primary" @click="handleLogin" class="login-button">登录</t-button>
  </div>
</template>

<script lang="ts" setup>
import { defineProps } from 'vue';
import { SiteStatus } from '../types/site';
import dashboardApi from '../apis/dashboard';
import { useSiteStore } from '../store/site';
import { MessagePlugin } from 'tdesign-vue-next';
const props = defineProps<{ item: SiteStatus }>();
const siteStore = useSiteStore();
const handleLogin = async () => {
  MessagePlugin.loading(`正在登录 ${props.item.name}...`, 0);
  try {
    const response = await dashboardApi.loginOnce(props.item.id);
    console.log(response.data);
    if (response.data.code === 0) {
      siteStore.updateSiteStatus(props.item.id, 1);
      MessagePlugin.success('登录成功');
    } else {
      MessagePlugin.error('登录失败');
    }
  } catch {
    MessagePlugin.error('登录失败');
  }
  MessagePlugin.closeAll();
};
</script>

<style scoped>
.site-status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.login-button {
  margin-left: 10px;
}
</style>
