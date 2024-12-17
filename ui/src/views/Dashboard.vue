<template>
  <div class="dashboard-container">
    <t-space align="center" direction="vertical" class="space">
      <t-row :gutter="16">
        <t-col :span="6">
          <t-card title="文章列表">
            <template #content>
              <t-list v-if="postList.length > 0" split size="large" :scroll="{ type: 'virtual' }" class="list">
                <PostListItem v-for="(post, index) in postList" :key="index" :path="post.path" :name="post.name"
                  @refresh="fetchPostList" />
              </t-list>
              <t-empty v-else title="暂无文章" class="empty" />
            </template>
          </t-card>
        </t-col>
        <t-col :span="6">
          <t-card title="登录状态">
            <template #content>
              <t-list v-if="siteStore.siteStatuses.length > 0" split size="large" :scroll="{ type: 'virtual' }"
                class="list">
                <SiteStatusItem v-for="(loginStatus, index) in siteStore.siteStatuses" :key="index" :item="loginStatus"
                  @login="handleLoginOnce" />
              </t-list>
              <t-empty v-else title="暂无登录状态" class="empty" />
            </template>
          </t-card>
        </t-col>
      </t-row>
    </t-space>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import dashboardApi from '../apis/dashboard';
import { MessagePlugin, DialogPlugin } from 'tdesign-vue-next';
import { Post } from '../types/post';
import { SiteStatus } from '../types/site';
import { useSiteStore } from '../store/site';
import PostListItem from '../components/PostListItem.vue';
import SiteStatusItem from '../components/SiteStatusItem.vue';
import path from 'path';

const siteStore = useSiteStore();
const postList = ref<Post[]>([]);



const handleLoginOnce = async (siteStatus: SiteStatus) => {
  MessagePlugin.loading(`正在登录 ${siteStatus.name}...`, 0);
  try {
    const response = await dashboardApi.loginOnce(siteStatus.id);
    if (response.data.code === 0) {
      MessagePlugin.success('登录成功');
    } else {
      MessagePlugin.error('登录失败');
    }
  } catch {
    MessagePlugin.error('登录失败');
  }
};

const fetchPostList = async () => {
  try {
    const response = await dashboardApi.getPostList();
    if (response?.data?.data) {
      postList.value = response.data.data;
    }
  } catch (error) {
    console.error('Error fetching post list:', error);
  }
};
onMounted(() => {
  fetchPostList();
});
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  overflow-x: hidden;
  padding: 20px;
}

.alert {
  margin: 1vh 0.3vw;
  box-shadow: var(--td-shadow-1);
}

.space {
  width: 100%;
}


.list {
  height: 100%;
}


.empty {
  margin: 15vh 10vw;
}
</style>
