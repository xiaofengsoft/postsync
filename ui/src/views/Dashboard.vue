<template>
  <div style="width: 100%;">
    <t-alert v-for="loginStatus in loginStatuses" :key="loginStatus.name" style="margin-top: 10px;" theme="warning"
      title="登录状态" :message="`${loginStatus.name}未登录`" close>
      <template #operation>
        <span @click="handleLoginOnce(loginStatus)">点击登录</span>
      </template>
    </t-alert>
    <t-space align="center" direction="vertical" style="width: 100%;">
      <t-space direction="horizontal" style="width: 100%;display: flex;">
        <t-card title="文章列表" style="flex: 1; height: 100%; ">
          <t-list style="height: 350px;" split size="large" :scroll="{ type: 'virtual' }">
            <t-list-item style="margin: 10px; box-shadow: var(--td-shadow-1);border-radius: 10px;"
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
        <t-card title="PostSync介绍" description="作者：张一风" hover-shadow style="height: 100%;">
          <pre>
        这是一个开源的同步文章的软件，你可以使用它来同步你的文章到多个平台。
        目前支持的平台有掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台。
        支持GUI界面或者命令行界面来使用该软件。

        自动同步文章到掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台并返回生成文章链接
        支持多协程，异步上传文章
        支持包含查找，大小写模糊匹配
        支持md,html,docx文件
        支持自定义默认配置
        支持命令行界面，GUI界面
        自定义标题、标签、分类、专栏、封面、摘要
      </pre>

          <template #actions>
          </template>
        </t-card>
      </t-space>
      <t-space direction="horizontal" style="width: 100%;">
        <t-card title="操作方法" style="margin-bottom: 10px; flex: 1;">
          <t-timeline style="" layout="horizontal" label-align="alternate" mode="alternate">
            <t-timeline-item v-for="(item, index) in options" :key="index" :label="item.label" dot-color="primary">
              {{ item.content }}
            </t-timeline-item>
          </t-timeline>
        </t-card>
        <div style="flex: 1;"></div>
      </t-space>

    </t-space>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
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
    content: '配置文件',
    value: 1,
    label: 'config.yaml',
  },
  {
    content: '执行登录',
    value: 2,
    label: '登录各个网站',
  },
  {
    content: '撰写文章',
    value: 3,
    label: '撰写文章',
  },
  {
    content: '上传文章',
    value: 4,
    label: '保存并上传文章',
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

const router = useRouter();

const handleUpload = (post: Post) => {
  router.push({
    path: '/upload',
    query: { postFile: JSON.stringify(post) }
  });
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