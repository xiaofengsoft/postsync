<template>
  <el-row>
    <el-form class="post-from">
      <el-input size="large" v-model="input" placeholder="请输入文章标题"></el-input>
    </el-form>
    <MyEditor />
    <el-button type="primary" style="width:100%;margin-top: 10px;" @click="centerDialogVisible = true">点击上传</el-button>
    <el-dialog v-model="centerDialogVisible" title="文章表单" width="500" align-center>
      <el-form>
        <el-input size="large" v-model="input" placeholder="请输入文章标题"></el-input>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="centerDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="centerDialogVisible = false">
            Confirm
          </el-button>
        </div>
      </template>
    </el-dialog>
  </el-row>
</template>
<script>
import MyEditor from '../components/MyEditor.vue';
export default {
  data() {
    return {
      centerDialogVisible: false
    }
  }
}
</script>
<style scoped>
.post-from {
  width: 100%;
  margin-bottom: 10px;
}
</style>