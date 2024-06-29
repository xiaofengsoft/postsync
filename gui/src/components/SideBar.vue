<template>
  <el-menu mode="vertical" class="sidebar-wrapper" :default-active="activeTab" @select="handleSelect">
    <el-menu-item index="UploadPost">上传文章
    </el-menu-item>
    <el-menu-item index="NewPost">新的文章</el-menu-item>
    <el-menu-item index="LocalConfig">本地配置</el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'SideBar',
  components: {
  },
  data: () => ({
    activeTab: 'UploadPost'
  }),
  methods: {
    handleSelect(index) {
      this.activeTab = index
      this.$emit('changeView', index)
    }
  }
}
</script>
<style scoped>
.sidebar-wrapper {
  height: 90vh;
}
</style>