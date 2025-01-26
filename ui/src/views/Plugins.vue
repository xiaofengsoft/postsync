<script setup lang="ts">
import { ref, onMounted } from 'vue';
import pluginsApi from "../apis/plugin";
import { Card, Space, Row, Col } from 'tdesign-vue-next';

const plugins = ref([]);

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
          {{ plugin }}
        </template>
        <Space direction="vertical">
          <p class="plugin-desc">插件描述信息</p>
          <t-button theme="danger" variant="outline" size="small">
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