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
      <el-row style="margin-bottom: 10px;">
        <el-input v-model="title" size="large" placeholder="请输入标题" />
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-input v-model="digest" rows="6" type="textarea" placeholder="请输入摘要" />
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-input v-model="category" size="large" placeholder="请输入所属分类或目录" />
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-upload ref="upload" class="upload-demo"
          action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" :limit="1" :on-exceed="handleExceed"
          :auto-upload="false">
          <template #trigger>
            <el-button type="primary" size="large" style="display:block;width:100%">请选择封面</el-button>
          </template>
        </el-upload>
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-input v-model="topic" size="large" placeholder="请输入话题" />
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-select size="large" v-model="sitesList[postFile.uid]" :reserve-keyword="true" multiple filterable
          allow-create default-first-option placeholder="请选择站点">
          <el-option v-for="site in siteOptions" :key="site.value" :label="site.label" :value="site.value" />
        </el-select>
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-select size="large" v-model="tagsList[postFile.uid]" :reserve-keyword="true" multiple filterable
          allow-create default-first-option placeholder="请选择标签">
          <el-option v-for="tag in tagOptions" :key="tag.value" :label="tag.label" :value="tag.value" />
        </el-select>
      </el-row>
      <el-row style="margin-bottom: 10px;">
        <el-select size="large" v-model="columnsList[postFile.uid]" :reserve-keyword="true" multiple filterable
          allow-create default-first-option placeholder="请选择栏目">
          <el-option v-for="column in columnOptions" :key="column.value" :label="column.label" :value="column.value" />
        </el-select>
      </el-row>
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
    siteOptions: [
      { "label": "掘金", "value": "juejin" },
      { "label": "CSDN", "value": "csdn" },
      { "label": "知乎", "value": "zhihu" },
    ],
    sitesList: [],
    columnOptions: [],
    columnsList: [],
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
<style scoped></style>