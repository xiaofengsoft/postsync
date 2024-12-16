<template>
  <div class="site-status-item">
    <t-tag :theme="item.status ? 'success' : 'danger'">{{ item.name }}</t-tag>
    <t-button @click="handleLogin" class="login-button">登录</t-button>
  </div>
</template>

<script lang="ts" setup>
import { defineProps } from 'vue';
import { SiteStatus } from '../types/site';

const props = defineProps<{ item: SiteStatus }>();

const handleLogin = () => {
  // ...existing code...
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
