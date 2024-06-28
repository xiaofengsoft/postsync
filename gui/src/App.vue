<template>
  <div style="height: 100vh;background-color: white;">
    <TitleBar class="title-bar" />
    <el-container style="margin-top: 7%;">
      <el-aside width="200px">
        <SideBar @changeView="changeView" />
      </el-aside>
      <el-container>
        <el-main>
          <component :is="currentView"></component>
        </el-main>
      </el-container>
    </el-container>

  </div>

</template>

<script>
import SideBar from './components/SideBar.vue'
import TitleBar from './components/TitleBar.vue'
import UploadPost from './views/UploadPost.vue'
import NewPost from './views/NewPost.vue'
import LocalConfig from './views/LocalConfig.vue';

export default {
  name: 'App',
  components: {
    UploadPost,
    NewPost,
    SideBar,
    TitleBar,
    LocalConfig,
  },
  data() {
    return {
      currentView: UploadPost
    }
  },
  methods: {
    changeView(view) {
      this.currentView = view
    }
  }
}
</script>

<style>
body {
  margin: 0;
  /* 允许内容在垂直方向上滚动 */
  overflow-y: auto;

  /* 隐藏滚动条，但保持滚动功能（WebKit 浏览器） */
  &::-webkit-scrollbar {
    width: 0;
    /* 去除垂直滚动条的宽度 */
    background: transparent;
    /* 可选：使滚动条透明 */
  }

  /* 可选：隐藏水平滚动条 */
  &::-webkit-scrollbar-track {
    background: transparent;
    /* 滚动条轨道颜色 */
  }

  &::-webkit-scrollbar-thumb {
    background: transparent;
    /* 滚动条颜色 */
  }
}

.title-bar {
  box-shadow: 0px -3px 5px rgba(0, 0, 0, 0.3),
    0px -10px 20px rgba(0, 0, 0, 0.1);
  background-color: white;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
</style>
