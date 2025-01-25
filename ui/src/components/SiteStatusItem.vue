<template>
  <div class="site-status-item">
    <t-tag :theme="item.status ? 'success' : 'danger'">{{ item.name }}</t-tag>
    <t-button v-if="!item.status" theme="primary" @click="handleLogin" class="login-button">登录</t-button>
    <t-button v-else theme="warning" @click="resetLogin">重置</t-button>

    <t-dialog v-model:visible="isLoginModalVisible" header="登录确认" :confirm-btn="{ content: '确认登录成功', theme: 'primary' }"
      :cancel-btn="{ content: '未成功登录' }" @confirm="confirmLogin" @cancel="cancelLogin">
      <template #body>
        <div class="login-modal-content">
          请在浏览器中完成登录操作后，点击确认按钮
        </div>
      </template>
    </t-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { defineProps } from 'vue';
import { SiteStatus } from '../types/site';
import dashboardApi from '../apis/dashboard';
import { useSiteStore } from '../store/site';
import { MessagePlugin } from 'tdesign-vue-next';

const props = defineProps<{ item: SiteStatus }>();
const siteStore = useSiteStore();
const isLoginModalVisible = ref(false);

const handleLogin = async () => {
  isLoginModalVisible.value = true;
  try {
    await dashboardApi.loginOnce(props.item.id);
  } catch {
    isLoginModalVisible.value = false;
  }
};

const confirmLogin = async () => {
  try {
    await dashboardApi.confirmLogin(props.item.id);
    siteStore.updateSiteStatus(props.item.id, 1);
    MessagePlugin.success('登录成功');
    isLoginModalVisible.value = false;
  } catch {
    MessagePlugin.error('确认失败');
  }
};

const cancelLogin = async () => {
  MessagePlugin.info('取消登录');
  isLoginModalVisible.value = false;
};

const resetLogin = async () => {
  try {
    const response = await dashboardApi.resetLogin(props.item.id);
    if (response.data.code === 0) {
      siteStore.updateSiteStatus(props.item.id, 0);
      MessagePlugin.success('恢复成功');
    } else {
      MessagePlugin.error('恢复失败');
    }
  } catch {
    MessagePlugin.error('恢复失败');
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

.login-modal-content {
  padding: 20px;
  text-align: center;
}
</style>
