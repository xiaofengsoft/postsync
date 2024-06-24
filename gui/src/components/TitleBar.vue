<template>
  <el-page-header class="title-bar" :icon="null">
    <template #title>
      <div class="flex items-center">
        <el-avatar :size="36" style="margin-top: 5px;" src="./../assets/imgs/logo.ico" />
      </div>
    </template>
    <template #content>
      <span style="color: black;">PostSync</span>
    </template>


    <template #extra>
      <div class="flex buttons items-center">
        <el-button @click="minimize" color="black" :icon="Minus" circle plain>
        </el-button>
        <el-button @click="maximize" color="black" :icon="FullScreen" plain circle>
        </el-button>
        <el-button @click="close" color="black" :icon="Close" plain circle>
        </el-button>
      </div>
    </template>
  </el-page-header>
</template>


<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { Minus, FullScreen, Close } from '@element-plus/icons-vue';

const minimize = () => {
  window.electronAPI.windowMinimize();
};

const maximize = () => {
  window.electronAPI.windowMaximize();
};

const close = () => {
  window.electronAPI.windowClose();
};


onMounted(() => {
  // 组件挂载时的逻辑
});

onUnmounted(() => {
  // 组件卸载时的逻辑
});
</script>

<style scoped>
.title-bar {
  padding: 2px 10px;
  -webkit-app-region: drag;
}

.buttons {
  font-size: 14px;
  -webkit-app-region: no-drag;
}
</style>
