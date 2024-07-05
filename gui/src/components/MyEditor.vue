<template>
  <div style="border: 1px solid #ccc">
    <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode" />
    <Editor style="height: 500px; overflow-y: hidden;" v-model="valueHtml" :defaultConfig="editorConfig" :mode="mode"
      @onCreated="handleCreated" />
  </div>
</template>
<script>
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

export default {
  components: { Editor, Toolbar },
  emits: ['transferHtmlValue'],
  data() {
    return {
      editorRef: null,
      valueHtml: '',
      mode: 'default', // 或 'simple'
      toolbarConfig: {},
      editorConfig: { placeholder: '请输入内容...' }
    }
  },
  mounted() {
    // 模拟 ajax 异步获取内容
    setTimeout(() => {
      this.valueHtml = '<p>Hello PostSync !!!</p>'
    }, 1500)
  },
  watch: {
    valueHtml(val) {
      this.$emit('transferHtmlValue', val)
    }
  },
  beforeUnmount() {
    const editor = this.editorRef
    if (editor == null) return
    editor.destroy()
  },
  methods: {
    handleCreated(editor) {
      this.editorRef = editor // 记录 editor 实例，重要！
    },
  },
  computed: {
  }
}
</script>