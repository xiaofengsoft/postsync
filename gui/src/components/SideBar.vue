<template>
  <el-menu style="height: 90vh;" :default-active="activeTab" @select="handleSelect">
    <el-menu-item index="UploadPost">上传文章</el-menu-item>
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
