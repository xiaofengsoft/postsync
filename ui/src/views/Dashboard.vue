<template>
  <div>
    <t-alert v-for="loginStatus in loginStatuses" :key="loginStatus.name" style="margin-top: 10px;" theme="warning"
      title="登录状态" :message="`${loginStatus.name}未登录`" close>
      <template #operation>
        <span @click="handleLoginOnce(loginStatus)">点击登录</span>
      </template>
    </t-alert>
    <t-space align="center" direction="vertical" style="width: 100%; height: 100%;">
      <t-space direction="horizontal">
        <t-card title="文章列表" style="flex: 1; height: 100%; overflow-y: auto;">
          <t-list split stripe size="large" :scroll="{ type: 'virtual' }">
            <t-list-item style="margin-top: 10px; background: var(--td-gray-color-2);border-radius: 10px;"
              v-for="(post, index) in postList" :key="index">
              <template #action>
                <t-link theme="success" hover="color" @click="handleUpload(post)" style="margin-left: 16px"> 上传
                </t-link>
                <t-link theme="danger" hover="color" @click="handleDelete(post)" style="margin-left: 16px"> 删除 </t-link>
              </template>
              <t-list-item-meta :title="post.name" :description="post.path" />
            </t-list-item>
          </t-list>
        </t-card>

        <t-card cover="/imgs/logo-landscape.png" theme="poster2" :style="{ width: '400px' }">
          <template #footer>
            <t-comment avatar="https://yunyicloud.cn/wp-content/uploads/2024/08/cropped-%E4%BA%91%E5%A5%95.png"
              author="张一风" content="正在进行中" />
          </template>
          <template #actions>
            <t-dropdown :options="options" :min-column-width="112" @click="() => console.log('click')">
              <t-button variant="text" shape="square">
                <more-icon />
              </t-button>
            </t-dropdown>
          </template>
        </t-card>
      </t-space>
      <t-card title="操作方法">
        <t-timeline style="" layout="horizontal" label-align="alternate" mode="alternate">
          <t-timeline-item v-for="(item, index) in options" :key="index" :label="item.label" dot-color="primary">
            {{ item.content }}
          </t-timeline-item>
        </t-timeline>
      </t-card>
    </t-space>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import dashboardApi from '../apis/dashboard';
import { MessagePlugin, DialogPlugin } from 'tdesign-vue-next';

interface LoginStatus {
  name: string;
  status: string | boolean;
  alias: string;
}

interface Post {
  name: string;
  path: string;
}

const loginStatuses = ref<LoginStatus[]>([]);
const postList = ref<Post[]>([]);
const options = ref<any[]>([
  {
    content: '操作一',
    value: 1,
    label: '操作一',
  },
  {
    content: '操作二',
    value: 2,
    label: '操作二',
  },
  {
    content: '操作三',
    value: 3,
    label: '操作三',
  },
  {
    content: '操作四',
    value: 4,
    label: '操作四',
  },
  {
    content: '操作五',
    value: 5,
    label: '操作五',
  },
  {
    content: '操作六',
    value: 6,
    label: '操作六',
  },
  {
    content: '操作七',
    value: 7,
    label: '操作七',
  },

]);

const fetchLoginStatuses = async () => {
  try {
    if (localStorage.getItem('loginStatuses')) {
      loginStatuses.value = JSON.parse(localStorage.getItem('loginStatuses') || '[]').filter((item: LoginStatus) => item.status === 'False' || item.status === false);
    } else {
      const response = await dashboardApi.checkLogin();
      if (response && response.data && Array.isArray(response.data.data)) {
        loginStatuses.value = response.data.data
        localStorage.setItem('loginStatuses', JSON.stringify(loginStatuses.value));
        loginStatuses.value = loginStatuses.value.filter((item: LoginStatus) =>
          item.status === 'False' || item.status === false
        );
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
      MessagePlugin.success('登录成功');
    } else {
      MessagePlugin.error('登录失败');
    }
  }).catch((error) => {
    MessagePlugin.error('登录失败');
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

const handleUpload = (post: Post) => {
  console.log(`上传文章: ${post.name}`);
};

const handleDelete = (post: Post) => {
  const confirmDialog = DialogPlugin.confirm({
    header: '删除文章',
    body: `确定删除文章: ${post.name}`,
    onConfirm: () => {
      dashboardApi.deletePostFile(post.path).then((response) => {
        console.log(response.data.data);
        if (response.data.code === 0) {
          MessagePlugin.success('删除成功');
          fetchPostList();
          confirmDialog.hide();
        } else {
          MessagePlugin.error('删除失败');
          confirmDialog.hide();
        }
      }).catch((error) => {
        MessagePlugin.error('删除失败');
        confirmDialog.hide();
      });
    },
    onCancel: () => {
      confirmDialog.hide();
    }
  });
};

onMounted(() => {
  fetchLoginStatuses();
  fetchPostList();
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
