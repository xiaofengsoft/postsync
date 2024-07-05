<template>
  <el-row>
    <MyEditor @transferHtmlValue="getPostHtmlValue" />
    <el-form class="post-from">
      <el-input size="large" style="margin-top: 10px;" v-model="input" placeholder="请输入文章标题"></el-input>
      <el-input v-model="post.digest" style="margin-top: 10px;" rows="6" type="textarea" placeholder="请输入摘要" />
      <el-upload style="margin-top: 10px;" :on-change="handleCoverChanged" :auto-upload="false" accept=".jpg,.png,.jpeg"
        :limit="1" drag>
        <img width="30%" v-if="post" :src="post.cover" class="avatar" />
        <el-icon v-else class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          点击选择封面
        </div>
      </el-upload>
    </el-form>
    <el-button type="primary" style="width:100%;margin-top: 10px;" @click="submitNewPost">点击上传</el-button>
  </el-row>
</template>
<script>
import MyEditor from '../components/MyEditor.vue';
export default {
  data() {
    return {
      centerDialogVisible: false,
      post: '',
      htmlValue: '',
    }
  },
  methods: {
    submitNewPost() {
      console.log(this.htmlValue)
    },
    getPostHtmlValue(html) {
      this.htmlValue = html
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