<template>
  <div class="editor-container">
    <MdEditor v-model="localContent" previewTheme="github" :style="{ cursor: 'text', height }" :toolbars="toolbars"
      noUploadImg @onSave="handleSave">
      <template #defToolbars>
        <NormalToolbar title="选择图片" @onClick="handleSelectImg">
          <template #trigger>
            <ImageAddIcon style="width: 23px; height: 23px;margin: 5px 8px;" />
          </template>
        </NormalToolbar>
      </template>
    </MdEditor>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import { MdEditor, NormalToolbar } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import writeApi from '../apis/write';
import type { ToolbarNames, Footers } from 'md-editor-v3';
import { ImageAddIcon } from 'tdesign-icons-vue-next';

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '60vh'
  }
});

const toolbars = ref<ToolbarNames[]>([
  'bold',
  'underline',
  'italic',
  '-',
  'title',
  'strikeThrough',
  'sub',
  'sup',
  'quote',
  'unorderedList',
  'orderedList',
  'task',
  '-',
  'codeRow',
  'code',
  'link',
  'image',
  0,
  'table',
  'mermaid',
  'katex',
  '-',
  'revoke',
  'next',
  'save',
  '=',
  'preview',
  'previewOnly',
  'htmlPreview',
  'catalog',
]);

const emit = defineEmits(['update:content', 'save']);

const localContent = ref(props.content);

watch(() => props.content, (newValue) => {
  localContent.value = newValue;
});

watch(localContent, (newValue) => {
  emit('update:content', newValue);
});

const handleSelectImg = () => {
  writeApi.selectImage().then((res: any) => {
    let newContent = localContent.value;
    res.data.data.forEach((item: string) => {
      newContent += `![${item}](${item})\n`;
    });
    localContent.value = newContent;
  });
};

const handleSave = () => {
  emit('save', localContent.value);
};

</script>

<style scoped>
:root {
  all: initial;
}

.editor-container {
  all: initial;
}

.editor-container :deep(.md-editor-content) {
  height: 100%;
  min-height: 40vh;
}

.editor-container :deep(.md-editor-content div) {
  font-size: 2vh;
}

.editor-container :deep(.md-editor-footer div) {
  font-size: 1.8vh;
}

.editor-container :deep(.md-editor-content p) {
  font-size: 2vh;
}


.editor-container :deep(svg) {
  width: 35px;
  height: 35px;
}
</style>
<style>
.md-editor-modal-func {
  top: -75px !important;
}
</style>
