<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import windowApi from '../apis/window';
import { MessagePlugin } from 'tdesign-vue-next';

const currentTab = ref('dashboard');
const isMaximized = ref(false);
const router = useRouter();
const route = useRoute();
const watchRoute = watch(route, (newVal) => {
  currentTab.value = newVal.name as string || 'dashboard';
});

const handleMenuChange = (value: string) => {
  currentTab.value = value;
  router.push(value);
};

const minimizeWindow = () => {
  windowApi.minimizeWindow().then((data) => {
    console.log(data);
  }).catch(() => {
    console.log('最小化窗口失败');
  });
};

const toggleWindow = () => {
  if (isMaximized.value) {
    windowApi.restoreWindow().then((data) => {
      isMaximized.value = false;
      console.log(data);
    }).catch(() => {
      console.log('还原窗口失败');
    });
  } else {
    isMaximized.value = true;
    windowApi.maximizeWindow().then((data) => {
      console.log(data);
    }).catch(() => {
      console.log('最大化窗口失败');
    });
  }
};

const closeWindow = () => {
  windowApi.closeWindow().then((data) => {
    console.log(data);
  }).catch(() => {
    console.log('关闭窗口失败');
  });
};

onMounted(() => {
  currentTab.value = route.name as string || 'dashboard';
  console.log(currentTab.value);
});
</script>

<template>
  <t-layout style="height: 100vh;">
    <t-header :class="['layout-header', 'pywebview-drag-region']">
      <t-head-menu value="item1">
        <template #logo>
          <img width="136" class="logo" src="@/assets/imgs/logo-landscape.png" alt="logo" />
        </template>
        <template #operations>
          <a @click="minimizeWindow"><t-icon class="t-menu__operations-icon" name="remove" /></a>
          <a @click="toggleWindow"><t-icon class="t-menu__operations-icon" name="center-focus-strong" /></a>
          <a @click="closeWindow"><t-icon class="t-menu__operations-icon" name="close" /></a>
        </template>
      </t-head-menu>
    </t-header>
    <t-layout>
      <t-aside class="layout-aside">
        <t-menu theme="light" :value="currentTab" @change="handleMenuChange" style="width: 14vw;box-shadow: inherit;">
          <t-menu-item value="dashboard">
            <template #icon>
              <t-icon name="dashboard" />
            </template>
            仪表盘
          </t-menu-item>
          <t-menu-item value="write">
            <template #icon>
              <t-icon name="pen-ball" />
            </template>
            新文章
          </t-menu-item>
          <t-menu-item value="upload">
            <template #icon>
              <t-icon name="cloud-upload" />
            </template>
            上传文章
          </t-menu-item>
          <t-menu-item value="settings">
            <template #icon>
              <t-icon name="setting" />
            </template>
            设置
          </t-menu-item>
        </t-menu>
      </t-aside>
      <t-layout>
        <t-content class="layout-content">
          <router-view />
        </t-content>
        <t-footer class="layout-footer">
          Copyright @ 2024-{{ new Date().getFullYear() }} XFS. All Rights
          Reserved</t-footer>
      </t-layout>
    </t-layout>
  </t-layout>
</template>

<style scoped>
.layout-header {
  box-shadow: var(--td-shadow-1);
  margin-bottom: var(--td-comp-margin-xs);
  padding: 1vh 0;
  background: var(--td-brand-color);
}

.layout-header .t-menu {
  background: inherit;
  color: white;
}

.t-menu__item {
  padding: 4vh 1.5vw;
  font-size: 1.1vw;
}

.t-menu__item svg {
  font-size: 1.2vw;
}

.layout-header a svg {
  color: white;
}

.layout-header a svg :hover {
  background-color: #000;
}

.layout-aside {
  border-top: 0.5vh solid var(--component-border);
  box-shadow: var(--td-shadow-1);
}

.layout-content {
  padding: 1vw 1vw 0 1vw;
  background-color: var(--td-brand-color-1);
  overflow-y: scroll;
  height: 83vh;
  width: 84vw;
}

.layout-footer {
  background-color: var(--td-brand-color-1);
  height: 1vh;
}
</style>