<template>
  <div>
    <el-input type="textarea" v-model="markdownContent" placeholder="在此输入Markdown..." :rows="20"></el-input>
  </div>
</template>

<script>

export default {
  name: "MarkdownEditor",
  data() {
    return {
      markdownContent: "",
    }
  }
}
</script>
