<script setup lang="ts">
import { ref, onMounted } from 'vue';
import pluginsApi from "../apis/plugin";
import { Card, Space, Row, Col, MessagePlugin } from 'tdesign-vue-next';
import { useSiteStore } from '../store/site';
const plugins = ref([]);
const siteStore = useSiteStore();
const handleUninstall = async (name: string) => {
  try {
    await pluginsApi.uninstallPlugins(name);
    siteStore.deleteSiteStatus(name);
    MessagePlugin.success('卸载成功');
    // 重新加载插件列表
    const response = await pluginsApi.getPlugins();
    plugins.value = response.data.data;
  } catch (error) {
    MessagePlugin.error('卸载失败');
  }
};

onMounted(async () => {
  const response = await pluginsApi.getPlugins();
  plugins.value = response.data.data;
})
</script>

<template>
  <div class="plugin-container">
    <h2 class="title">可用插件</h2>
    <Row :gutter="[16, 16]">
      <Col v-for="plugin in plugins" :key="plugin" :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
      <Card hoverable class="plugin-card">
        <template #title>
          {{ plugin[1].name }}
        </template>
        <Space direction="vertical">
          <p class="plugin-desc">{{ plugin[1].desc }}</p>
          <t-button @click="handleUninstall(plugin[0])" theme="danger" variant="outline" size="small">
            卸载插件
          </t-button>
        </Space>
      </Card>
      </Col>
    </Row>
  </div>
</template>

<style scoped>
.plugin-container {
  padding: 20px;
}

.title {
  margin-bottom: 24px;
  color: var(--td-text-color-primary);
}

.plugin-card {
  height: 100%;
  transition: all 0.3s;
}

.plugin-desc {
  color: var(--td-text-color-secondary);
  font-size: 14px;
}
</style>