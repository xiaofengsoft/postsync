<template>
  <div style="height: 100vh;background-color: white;">
    <TitleBar class="title-bar" />
    <el-container style="margin-top: 60px;">
      <el-aside width="30vh">
        <SideBar @changeView="changeView" />
      </el-aside>
      <el-container>
        <el-scrollbar style="width: 100%;" max-height="90vh">
          <el-main>
            <component :is="currentView"></component>
          </el-main>
        </el-scrollbar>
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
  overflow: hidden;
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
