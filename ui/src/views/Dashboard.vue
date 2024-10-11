<template>
  <div style="width: 100%;overflow-x: hidden;">
    <t-alert v-for="loginStatus in loginStatuses" :key="loginStatus.name"
      style="margin: 1vh 0;box-shadow: var(--td-shadow-1);" theme="warning" title="登录状态"
      :message="`${loginStatus.name}未登录`" close>
      <template #operation>
        <span @click="handleLoginOnce(loginStatus)">点击登录</span>
      </template>
    </t-alert>
    <t-space align="center" direction="vertical" style="width: 100%;">
      <t-row :gutter="16">
        <t-col :span="6">
          <t-card style="height: 50vh;overflow-y: scroll;">
            <template #content>
              <t-list split size="large" :scroll="{ type: 'virtual' }" style="height: 100%;">
                <t-list-item style="margin: 1.3vh; box-shadow: var(--td-shadow-1);border-radius: 10px;"
                  v-for="(post, index) in postList" :key="index">
                  <template #action>
                    <t-link theme="success" hover="color" @click="handleUpload(post)" style="margin-left: 1vw"> 上传
                    </t-link>
                    <t-link theme="danger" hover="color" @click="handleDelete(post)" style="margin-left: 1vw"> 删除
                    </t-link>
                  </template>
                  <t-list-item-meta :title="post.name" :description="post.path" style="overflow-x: hidden;" />
                </t-list-item>
              </t-list>
            </template>
          </t-card>
        </t-col>
        <t-col :span="6">
          <t-card title="PostSync介绍" description="作者：张一风" hover-shadow style=" height: 50vh;overflow-y: scroll;">
            <t-typography-paragraph>
              这是一个开源的同步文章的软件，你可以使用它来同步你的文章到多个平台。<br>
              目前支持的平台有掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台。<br>
              支持GUI界面或者命令行界面来使用该软件。<br>
              <br>
              自动同步文章到掘金、CSDN、知乎、公众号、哔哩哔哩、博客园、个人WordPress平台并返回生成文章链接<br>
              支持多协程，异步上传文章<br>
              支持包含查找，大小写模糊匹配<br>
              支持md,html,docx文件<br>
              支持自定义默认配置<br>
              支持命令行界面，GUI界面<br>
              自定义标题、标签、分类、专栏、封面、摘要
            </t-typography-paragraph>

            <template #actions>
            </template>
          </t-card>
        </t-col>
      </t-row>
      <t-row style="height: 50vh;">
        <t-card title="操作方法" style="margin-bottom: 10vh; flex: 1;">
          <t-timeline style="" layout="horizontal" label-align="alternate" mode="alternate">
            <t-timeline-item v-for="(item, index) in options" :key="index" :label="item.label" dot-color="primary">
              {{ item.content }}
            </t-timeline-item>
          </t-timeline>
        </t-card>
        <div style="flex: 1;"></div>
      </t-row>

    </t-space>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import dashboardApi from '../apis/dashboard';
import { MessagePlugin, DialogPlugin } from 'tdesign-vue-next';
import windowApi from '../apis/window';
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
      return;
    }
    const storageResp = await windowApi.getStorage();
    if (storageResp.data.code === 0) {
      localStorage.setItem('loginStatuses', storageResp.data.data);
      return;
    }
    const response = await dashboardApi.checkLogin();
    if (response && response.data && Array.isArray(response.data.data)) {
      loginStatuses.value = response.data.data
      const data = JSON.stringify(loginStatuses.value)
      loginStatuses.value = loginStatuses.value.filter((item: LoginStatus) =>
        item.status === 'False' || item.status === false
      );
      windowApi.saveStorage(data).then((response) => {
        if (response.data.code === 0) {
          localStorage.setItem('loginStatuses', data);
        } else {
          MessagePlugin.error('保存数据失败');
        }
      });
    } else {
      console.error('Unexpected response format:', response);
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
      const data = JSON.stringify(loginStatuses.value);
      windowApi.saveStorage(data).then((response) => {
        if (response.data.code === 0) {
          localStorage.setItem('loginStatuses', data);
          MessagePlugin.success('登录成功');
          fetchLoginStatuses();
        } else {
          MessagePlugin.error('保存数据失败');
        }
      });
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