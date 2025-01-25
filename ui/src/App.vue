<template>
  <router-view></router-view>
</template>
<script lang="ts" setup>
import { onBeforeMount } from 'vue';
import { useConfigStore } from './store/config';
import dashboardApi from './apis/dashboard';
import { useSiteStore } from './store/site';
import { MessagePlugin } from 'tdesign-vue-next';
const configStore = useConfigStore();
const siteStore = useSiteStore();
const checkLoginState = async () => {
  if (siteStore.siteStatuses && siteStore.siteStatuses.length > 0) {
    return;
  }

  MessagePlugin.loading('检查登录状态', 0);
  const response = await dashboardApi.checkLogin();
  if (response?.data?.data) {
    const temp = response.data.data.map((site: any) => ({
      name: site.name,
      id: site.alias,
      status: site.status?.toString().toLowerCase() === 'true' ? 1 : 0
    }));
    siteStore.$patch({ siteStatuses: temp });
    MessagePlugin.success('登录状态检查完成');
  }
  MessagePlugin.closeAll();
};
onBeforeMount(async () => {
  // 初始化配置
  await configStore.initConfig();
  // 获取登录状态
  await checkLoginState();
})
</script>
