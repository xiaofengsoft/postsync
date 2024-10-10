<script lang="ts">
import { defineComponent } from 'vue';
import SettingApi from '../apis/setting';
import { MessagePlugin } from 'tdesign-vue-next';

interface InputItem {
  label: string;
  path: string;
  type: string;
}

interface NestedObject {
  [key: string]: NestedObject | any;
}

interface Settings {
  [key: string]: any;
}

export default defineComponent({
  name: "Settings",
  data() {
    return {
      settings: {} as Settings,
      inputs: [] as InputItem[]
    };
  },
  methods: {
    createInputs(data: any, path = '') {
      const keys = Object.keys(data);
      keys.forEach((key) => {
        const fullPath = path ? `${path}.${key}` : key;
        if (Array.isArray(data[key])) {
          this.inputs.push({
            label: fullPath,
            path: fullPath,
            type: 'array'
          });
        } else if (typeof data[key] === 'object' && data[key] !== null && typeof data[key] !== "string") {
          this.createInputs(data[key], fullPath);
        } else {
          this.inputs.push({
            label: fullPath,
            path: fullPath,
            type: 'input'
          });
        }
      });
    },
    getNestedValue(obj: any, path: string) {
      return path.split('.').reduce((acc, part) => acc && acc[part], obj);
    },
    setNestedValue(obj: any, path: string, value: any) {
      const parts = path.split('.');
      const last = parts.pop();
      const target = parts.reduce((acc, part) => acc[part] = acc[part] || {}, obj);
      if (last) target[last] = value;
    },
    updateSetting(path: string, value: any) {
      const pathArray = path.split('.');
      let current = this.settings;
      for (let i = 0; i < pathArray.length - 1; i++) {
        if (!current[pathArray[i]]) {
          current[pathArray[i]] = {};
        }
        current = current[pathArray[i]];
      }
      current[pathArray[pathArray.length - 1]] = value;
    },
    handleInputChange(path: string, value: string | string[]) {
      this.setNestedValue(this.settings, path, value);
    },
    saveSettings() {
      console.log(this.settings);
      SettingApi.saveSettings(this.settings).then((response) => {
        console.log(response);
        MessagePlugin.success('保存成功');
      }).catch((error) => {
        MessagePlugin.error('保存失败');
      });
    },
    async fetchSettings() {
      try {
        const response = await SettingApi.getSettings();
        this.settings = response.data.data;
        this.createInputs(this.settings);
      } catch (error) {
        console.error('获取设置失败:', error);
      }
    }
  },
  mounted() {
    this.fetchSettings();
  }
});
</script>

<template>
  <t-card title="设置" header-bordered>
    <template #actions>
      <t-button @click="saveSettings">保存</t-button>
    </template>
    <t-form-item v-for="(input, index) in inputs" :key="index" :label="input.label">
      <t-input :value="getNestedValue(settings, input.path)"
        @change="(val: string) => handleInputChange(input.path, val)" v-if="input.type === 'input'" />
      <t-tag-input :value="getNestedValue(settings, input.path)"
        @change="(val: string[]) => handleInputChange(input.path, val)" v-else-if="input.type === 'array'" />
    </t-form-item>
  </t-card>
</template>