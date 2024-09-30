<template>
  <div class="tinymce-editor">
    <editor v-model="myValue" :init="init" :disabled="disabled" @onClick="onClick" />
  </div>
</template>
<script>
import 'tinymce'
import Editor from "@tinymce/tinymce-vue"

/* Required TinyMCE components */
import 'tinymce/icons/default/icons.min.js';
import 'tinymce/themes/silver/theme.min.js';
import 'tinymce/models/dom/model.min.js';

/* Import a skin (can be a custom skin instead of the default) */
import 'tinymce/skins/ui/oxide/skin.js';

/* Import plugins */
import 'tinymce/plugins/advlist';
import 'tinymce/plugins/code';
import 'tinymce/plugins/emoticons';
import 'tinymce/plugins/emoticons/js/emojis';
import 'tinymce/plugins/link';
import 'tinymce/plugins/lists';
import 'tinymce/plugins/table';

/* content UI CSS is required */
import 'tinymce/skins/ui/oxide/content.js';

/* The default content CSS can be changed or replaced with appropriate CSS for the editor content. */
import 'tinymce/skins/content/default/content.js';

export default {
  components: {
    Editor
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    plugins: {
      type: [String, Array],
      default:
        'code advlist lists image media wordcount link template fullscreen'
    },
    toolbar: {
      type: [String, Array],
      default:
        'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | image | code'
    }
  },
  data() {
    const This = this
    return {
      init: {
        language_url: `/tinymce/zh_CN.js`,
        language: 'zh_CN',
        skin_url: `/tinymce/skins/ui/oxide`,
        content_css: `/tinymce/skins/content/default/content.css`,
        height: 300,
        plugins: this.plugins,
        toolbar: this.toolbar,
        branding: false,
        menubar: false,
        // 如需ajax上传可参考https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_handler
        images_upload_handler: (blobInfo, success, failure) => {
          const file = blobInfo.blob() || {}
          if (!file || !file.size) return
          const maxSize = 10
          if (file.size > maxSize * 1024 * 1024) {
            this.$Message.warning(`图片最大尺寸是${maxSize}M`)
            return
          }
        },
        file_picker_types: 'file image'
      },
      myValue: this.value
    }
  },
  watch: {
    value(newValue) {
      this.myValue = newValue
    },
    myValue(newValue) {
      this.$emit('input', newValue)
    }
  },
  mounted() {
    tinymce.init({})
  },
  methods: {
    // 添加相关的事件，可用的事件参照文档=> https://github.com/tinymce/tinymce-vue => All available events
    // 需要什么事件可以自己增加
    onClick(e) {
      this.$emit('onClick', e, tinymce)
    },
    // 可以添加一些自己的自定义事件，如清空内容
    clear() {
      this.myValue = ''
    }
  }
}
</script>
