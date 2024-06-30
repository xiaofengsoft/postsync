<template>
  <el-upload :on-change="handleFileChanged" :file-list="fileList" :auto-upload="false" accept=".html,.md,.txt"
    :limit="limit" drag>
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      点击选择文章
    </div>
    <template #tip>
      <div class="el-upload__tip">
        默认文件名称（去掉后缀）为标题名
      </div>
    </template>
  </el-upload>
  <el-card style="margin-bottom: 10px;" shadow="hover" v-for="postFile in fileList">
    <template #header>
      <div class="card-header">
        <span>{{ postFile.name }}</span>
      </div>
    </template>
    <el-row style="margin-bottom: 10px;">
      <el-input v-model="posts.get(postFile.name).title" size="large" placeholder="请输入标题" />
    </el-row>
    <el-row style="margin-bottom: 10px;">
      <el-input v-model="posts.get(postFile.name).digest" rows="6" type="textarea" placeholder="请输入摘要" />
    </el-row>
    <el-row style="margin-bottom: 10px;">
      <el-input v-model="posts.get(postFile.name).category" size="large" placeholder="请输入所属分类或目录" />
    </el-row>
    <el-upload @click="currentCoverPost = postFile" :on-change="handleCoverChanged" :auto-upload="false"
      accept=".jpg,.png,.jpeg" :limit="1" drag>
      <img width="30%" v-if="posts.get(postFile.name).cover" :src="posts.get(postFile.name).cover" class="avatar" />
      <el-icon v-else class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        点击选择封面
      </div>
    </el-upload>
    <el-row style="margin-bottom: 10px;">
      <el-input v-model="posts.get(postFile.name).topic" size="large" placeholder="请输入话题" />
    </el-row>
    <el-row style="margin-bottom: 10px;">
      <el-select size="large" v-model="posts.get(postFile.name).sites" :reserve-keyword="true" multiple filterable
        allow-create default-first-option placeholder="请选择站点">
        <el-option v-for="site in siteOptions" :key="site.value" :label="site.label" :value="site.value" />
      </el-select>
    </el-row>
    <el-row style="margin-bottom: 10px;">
      <el-select size="large" v-model="posts.get(postFile.name).tags" :reserve-keyword="true" multiple filterable
        allow-create default-first-option placeholder="请选择标签">
        <el-option v-for="tag in tagOptions" :key="tag.value" :label="tag.label" :value="tag.value" />
      </el-select>
    </el-row>
    <el-row style="margin-bottom: 10px;">
      <el-select size="large" v-model="posts.get(postFile.name).columns" :reserve-keyword="true" multiple filterable
        allow-create default-first-option placeholder="请选择栏目">
        <el-option v-for="column in columnOptions" :key="column.value" :label="column.label" :value="column.value" />
      </el-select>
    </el-row>
  </el-card>
  <el-form-item>
    <el-button style="display: block;width: 100%;" type="primary" @click="onSubmit">一键上传</el-button>
  </el-form-item>
</template>

<script>

import { Close } from '@element-plus/icons-vue'
import { joinPostSyncCommands } from '@/utils/command.js'
import { ElMessage, ElMessageBox } from 'element-plus'
export default {
  name: 'UploadPost',
  components: {
    Close,
  },
  data() {
    return {
      currentCoverPost: '',
      tagOptions: [], // 标签选项
      fileList: [],
      siteOptions: [
        { "label": "掘金", "value": "juejin" },
        { "label": "CSDN", "value": "csdn" },
        { "label": "知乎", "value": "zhihu" },
      ],
      columnOptions: [],
      posts: new Map(),
      limit: 5,
    }
  },
  methods: {
    initPost(fileName, filePath) {
      this.posts.set(fileName, {
        title: fileName,
        filePath: filePath,
        digest: '',
        category: '',
        topic: '',
        cover: '',
        coverPath: '',
        sites: [],
        tags: [],
        columns: [],
      })
    },
    async onSubmit() {
      try {
        for (const post of this.posts.values()) {
          ElMessage({
            type: 'info',
            message: `正在上传${post.title}...`,
          })
          let cmd = joinPostSyncCommands(post.filePath, post.title, post.digest, post.category, post.coverPath, post.topic, post.sites, post.tags, post.columns)
          console.log(cmd)
          const result = await window.electronAPI.executeCommand(cmd);
          ElMessageBox.alert(result, '上传结果', {
            confirmButtonText: '确认',
          })
        }
      } catch (error) {
        ElMessageBox.alert(error, '上传出错', {
          confirmButtonText: '确认',
        })
        console.error('执行命令时出错：', error);
      }
    },
    handleFileChanged(file, fileList) {
      this.fileList.push(file)
      this.initPost(file.name, file.raw.path)
    },
    handleCoverChanged(file, fileList) {
      this.posts.get(this.currentCoverPost.name).coverPath = file.raw.path
      window.electronAPI.getImageDataUrl(file.raw.path).then((res) => {
        this.posts.get(this.currentCoverPost.name).cover = res
      })
    },

  },
  watch: {
  }
}
</script>
<style scoped>
.el-upload .el-upload__input {
  padding: 0;
  /* 假设这是影响按钮显示的样式 */
}
</style>