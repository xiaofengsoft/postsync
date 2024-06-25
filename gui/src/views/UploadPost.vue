<template>
  <el-form :model="form">
    <el-upload :on-change="onChanged" :file-list="fileList" :auto-upload="false" accept=".html,.md,.txt" :limit="limit"
      drag>
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
      <el-select size="large" v-model="tagsList[postFile.uid]" :reserve-keyword="true" multiple filterable allow-create
        default-first-option placeholder="请选择标签">
        <el-option v-for="tag in tagOptions" :key="tag.value" :label="tag.label" :value="tag.value" />
      </el-select>
    </el-card>
    <el-form-item>
      <el-button style="display: block;width: 100%;" type="primary" @click="onSubmit">一键上传</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { Close } from '@element-plus/icons-vue'
export default {
  name: 'UploadPost',
  components: {
    Close,
  },
  data: () => ({
    tagOptions: [], // 标签选项
    tagsList: [], // 已选择的标签列表
    fileList: [],
    limit: 5,
  }),
  methods: {
    onSubmit() {
      console.log(this.tagsList)
    },
    onChanged(file, fileList) {
      console.log(file, fileList)
      this.fileList = fileList
      console.log(this.tagOptions)
    },
  },
  watch: {
  }
}
</script>
