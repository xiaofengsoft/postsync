<template>
  <div style="height: 100vh;background-color: white;">
    <TitleBar />
    <el-container>

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
}
</style>
