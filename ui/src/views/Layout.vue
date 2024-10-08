<script lang="ts">
import windowApi from '../apis/window';

export default {
  name: 'Layout',
  data: () => ({
    currentTab: 'dashboard',
    isMaximized: false,
  }),
  methods: {
    handleMenuChange(value: string) {
      this.currentTab = value;
      this.$router.push(value);
    },
    minimizeWindow() {
      windowApi.minimizeWindow().then((data) => {
        console.log(data);
      }).catch(() => {
        console.log('minimize window failed');
      });
    },
    toggleWindow() {
      if (this.isMaximized) {
        windowApi.restoreWindow().then((data) => {
          this.isMaximized = false;
          console.log(data);
        }).catch(() => {
          console.log('restore window failed');
        });
      } else {
        this.isMaximized = true;
        windowApi.maximizeWindow().then((data) => {
          console.log(data);
        }).catch(() => {
          console.log('maximize window failed');
        });
      }
    },
    closeWindow() {
      windowApi.closeWindow().then((data) => {
        console.log(data);
      }).catch(() => {
        console.log('close window failed');
      });
    },
  },
  mounted() {
    this.currentTab = this.$route.name as string;
    console.log(this.currentTab);
  }
}
</script>
<template>
  <t-layout style="height: 100vh;">
    <t-header class="layout-header">
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
        <t-menu theme="light" :value="currentTab" @change="handleMenuChange" style="margin-right: 50px" height="550px">
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
  padding: 30px 40px;
  font-size: 16px;
}

.layout-header a svg {
  color: white;
}

.layout-header a svg :hover {
  background-color: #000;
}

.layout-aside {
  border-top: 1px solid var(--component-border);
  box-shadow: var(--td-shadow-1);
}

.layout-content {
  padding: 10px 10px 0 10px;
  background-color: var(--td-brand-color-1);
  overflow-y: hidden;
  height: 100%;
}

.layout-footer {
  background-color: var(--td-brand-color-1);
}
</style>