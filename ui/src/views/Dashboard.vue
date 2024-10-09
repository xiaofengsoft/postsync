<template>
  <t-card style="height: 80vh; overflow-y: scroll;" :class="{ 'dashboard-card': loginStatuses.length === 0 }">
    <template v-if="loginStatuses.length > 0">
      <t-alert v-for="loginStatus in loginStatuses" :key="loginStatus.name" style="margin-top: 10px;" theme="warning"
        title="登录状态" :message="`${loginStatus.name}未登录`" close>
        <template #operation>
          <span @click="handleLoginOnce(loginStatus)">点击登录</span>
        </template>
      </t-alert>
    </template>
    <t-empty v-else title="暂无消息" />
    <t-card title="文章列表" style="height: 30%;margin-top: 20px;">
      <t-list split stripe size="large" :scroll="{ type: 'virtual' }"><t-list-item
          style="margin-top: 10px; background: var(--td-gray-color-2);" v-for="(post, index) in postList" :key="index">
          <t-list-item-meta imageUrl="/public/favicon.ico" :title="post.name"
            :description="post.path" /></t-list-item></t-list>

    </t-card>
  </t-card>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import dashboardApi from '../apis/dashboard';
import { List, ListItem, ListItemMeta } from 'tdesign-vue-next';
interface LoginStatus {
  name: string;
  status: string | boolean;
  alias: string;
}

interface Post {
  name: string;
  path: string;
}

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const loginStatuses = ref<LoginStatus[]>([]);
    const postList = ref<Post[]>([]);
    const fetchLoginStatuses = async () => {
      try {
        if (localStorage.getItem('loginStatuses')) {
          loginStatuses.value = JSON.parse(localStorage.getItem('loginStatuses') || '[]');
        } else {
          const response = await dashboardApi.checkLogin();
          if (response && response.data && Array.isArray(response.data.data)) {
            loginStatuses.value = response.data.data.filter((item: LoginStatus) =>
              item.status === 'True' || item.status === true
            );
            localStorage.setItem('loginStatuses', JSON.stringify(loginStatuses.value));
          } else {
            console.error('Unexpected response format:', response);
          }
        }
      } catch (error) {
        console.error('Error fetching login statuses:', error);
      }
    };

    const handleLoginOnce = (loginStatus: LoginStatus) => {
      console.log(`登录社区: ${loginStatus.name}`);
      dashboardApi.loginOnce(loginStatus.alias).then((response) => {
        console.log(response.data.data);
        if (response.data.code === 0) {
          loginStatus.status = 'True';
          localStorage.setItem('loginStatuses', JSON.stringify(loginStatuses.value));
        }
      });
    };

    const fetchPostList = async () => {
      try {
        const response = await dashboardApi.getPostList();
        if (response && response.data && Array.isArray(response.data.data)) {
          console.log(response.data.data);
          postList.value = response.data.data;
        }
      } catch (error) {
        console.error('Error fetching post list:', error);
      }
    };

    onMounted(fetchLoginStatuses);
    onMounted(fetchPostList);

    return {
      loginStatuses,
      handleLoginOnce,
      postList
    };
  }
});
</script>

<style>
.dashboard-card {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
