<template>
  <MdEditor v-model="localContent" style="cursor:text;" :onUploadImg="handleUploadImg" @onSave="handleSave" />
</template>

<script>
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';

export default {
  components: {
    MdEditor
  },
  props: {
    content: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      localContent: this.content
    }
  },
  watch: {
    localContent(newValue) {
      this.$emit('update:content', newValue);
    }
  },
  methods: {
    handleUploadImg(file) {
      console.log(file);
    },
    handleSave() {
      this.$emit('save', this.localContent);
    }
  }
}
</script>