<script setup lang="ts">
import { ref, onMounted } from 'vue';
import pluginsApi from "../apis/plugin";
import { Card, Space, Row, Col, MessagePlugin } from 'tdesign-vue-next';
import { useSiteStore } from '../store/site';
import { useConfigStore } from '../store/config';

// 修改插件类型定义，使其更明确
type PluginInfo = {
  name: string;
  desc: string;
};

type Plugin = [string, PluginInfo];

const plugins = ref<Plugin[]>([]);
const siteStore = useSiteStore();
const configStore = useConfigStore();
const uploading = ref(false);

const handleUninstall = async (name: string) => {
  try {
    await pluginsApi.uninstallPlugins(name);
    siteStore.deleteSiteStatus(name);
    MessagePlugin.success('卸载成功');
    // 重新加载插件列表
    const response = await pluginsApi.getPlugins();
    await configStore.initConfig();
    plugins.value = response.data.data;
  } catch (error) {
    MessagePlugin.error('卸载失败');
  }
};

const handleInstallPlugin = async () => {
  uploading.value = true;
  try {
    const response = await pluginsApi.installPlugin();
    if (response.data.code === 0) {
      MessagePlugin.success('安装成功');
      // 重新加载插件列表
      const pluginsResponse = await pluginsApi.getPlugins();
      await configStore.initConfig();
      plugins.value = pluginsResponse.data.data;
    } else {
      MessagePlugin.error(response.data.message || '安装失败');
    }
  } catch (error) {
    MessagePlugin.error('安装失败');
  } finally {
    uploading.value = false;
  }
};

onMounted(async () => {
  try {
    const response = await pluginsApi.getPlugins();
    plugins.value = response.data.data;
  } catch (error) {
    MessagePlugin.error('获取插件列表失败');
  }
});
</script>

<template>
  <div class="plugin-container">
    <h2 class="title">插件管理</h2>
    <Row :gutter="[16, 16]">
      <!-- 安装插件卡片 -->
      <Col :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
      <Card hoverable class="plugin-card install-card">
        <template #title>安装新插件</template>
        <Space direction="vertical" align="center" class="upload-space">
          <t-button :loading="uploading" @click="handleInstallPlugin" variant="outline">
            {{ uploading ? '安装中...' : '选择插件文件' }}
          </t-button>
          <p class="upload-hint">支持 .py 格式的插件文件</p>
        </Space>
      </Card>
      </Col>
      <!-- 现有插件列表 -->
      <Col v-for="plugin in plugins" :key="plugin[0]" :xs="24" :sm="12" :md="8" :lg="6" :xl="4">
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

.install-card {
  display: flex;
  flex-direction: column;
}

.upload-space {
  width: 100%;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-hint {
  color: var(--td-text-color-secondary);
  font-size: 12px;
  margin-top: 8px;
}
</style>