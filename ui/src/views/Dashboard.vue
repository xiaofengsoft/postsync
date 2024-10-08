<template>
  <t-card style="height: 80vh;overflow-y: scroll;">
    <MdPreview :editorId="id" :modelValue="readmeContent" class="readme-content" previewTheme="cyanosis" />
  </t-card>
</template>
<script lang="ts">
import dashboardApi from '../apis/dashboard';
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
export default {
  name: 'Dashboard',
  components: {
    MdPreview,
  },
  data() {
    return {
      readmeContent: '',
      id: 'preview-only',
    };
  },
  mounted() {
    dashboardApi.readme().then((response) => {
      console.log(response.data.data);
      this.readmeContent = response.data.data;
    })
  }
}
</script>
<style>
.readme-content {
  align-items: center;
  display: flex;
  justify-content: center;
  height: 100%;
  width: 100%;
  padding: 10px 1px;
}
</style>
