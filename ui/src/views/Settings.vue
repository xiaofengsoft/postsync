<script lang="ts" setup>
import { ref, onMounted } from 'vue';
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
const settings = ref<Settings>({});
const inputs = ref<InputItem[]>([]);
const labelList = ref<string[]>([]);
const createInputs = (data: any, path = '') => {
  const keys = Object.keys(data);
  keys.forEach((key) => {
    if (key === 'desc') {
      return;
    }
    const fullPath = path ? `${path}.${key}` : key;
    if (Array.isArray(data[key])) {
      inputs.value.push({
        label: fullPath,
        path: fullPath,
        type: 'array'
      });
    } else if (typeof data[key] === 'object' && data[key] !== null) {
      // 创建新的 div，并加入 label
      inputs.value.push({
        label: data[key].desc,
        path: fullPath,
        type: 'object'  // 可以添加该类型来标记为对象
      });
      labelList.value.push(data[key].desc);
      createInputs(data[key], fullPath); // 递归调用
    } else {
      inputs.value.push({
        label: fullPath,
        path: fullPath,
        type: 'input'
      });
    }
  });
};

const getNestedValue = (obj: any, path: string) => {
  const ret = path.split('.').reduce((acc, part) => {
    if (!acc) return null; // 如果 acc 为 null 或 undefined，返回 null
    // 检查当前 acc 是否是数组
    if (Array.isArray(acc) && acc.length == 0) {
      return []
    }
    return acc[part]; // 否则返回对象中对应的属性值
  }, obj);
  return ret;
};




const setNestedValue = (obj: any, path: string, value: any) => {
  const parts = path.split('.');
  const last = parts.pop();
  const target = parts.reduce((acc, part) => (acc[part] = acc[part] || {}, acc), obj);
  if (last) target[last] = value;
};


const handleInputChange = (path: string, value: string | string[]) => {
  setNestedValue(settings.value, path, value);
};

const saveSettings = () => {
  console.log(settings.value);
  SettingApi.saveSettings(settings.value).then((response) => {
    console.log(response);
    MessagePlugin.success('保存成功');
  }).catch((error) => {
    MessagePlugin.error('保存失败');
  });
};

const fetchSettings = async () => {
  try {
    const response = await SettingApi.getSettings();
    settings.value = response.data.data;
    createInputs(settings.value);
  } catch (error) {
    console.error('获取设置失败:', error);
  }
};
const handleAnchorClick = (e: MouseEvent) => {
  e.preventDefault();
}

onMounted(() => {
  fetchSettings();
});
</script>

<template>
  <t-card title="设置" header-bordered>
    <template #actions>
      <t-button @click="saveSettings">保存</t-button>
    </template>
    <t-row>
      <t-col :span="6" style="overflow-y: scroll;height: 70vh;">
        <div v-for="(input, index) in inputs" :key="index">
          <div v-if="input.type === 'object'" :id="input.label">
            <b>{{ input.label }}</b>
          </div>
          <t-form-item v-else :label="input.label">
            <t-input :value="getNestedValue(settings, input.path)"
              @change="(val: string) => handleInputChange(input.path, val)" v-if="input.type === 'input'" />
            <t-tag-input :value="getNestedValue(settings, input.path)"
              @change="(val: string[]) => handleInputChange(input.path, val)" v-else-if="input.type === 'array'" />
          </t-form-item>
        </div>
      </t-col>
      <t-col :span="5" style="margin-left: 2vw;">
        <t-anchor :affix-props="{ offsetTop: 150 }" width="200" @click="handleAnchorClick">
          <t-anchor-item v-for="label in labelList" :href="'#' + label" :title="label" />
        </t-anchor>
      </t-col>
    </t-row>


  </t-card>
</template>
