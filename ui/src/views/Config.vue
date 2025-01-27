<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import SettingApi from '../apis/setting';
import { MessagePlugin } from 'tdesign-vue-next';
import InputSetting from '../components/InputSetting.vue';
import Helper from '../utils/helper';
import { Configuration } from '../types/config';
import { useConfigStore } from '../store/config';
const settings = ref<Configuration>({});
const labelList = ref<string[]>([]);
const configStore = useConfigStore();

const saveSettings = () => {
  SettingApi.saveSettings(settings.value).then((response) => {
    configStore.initConfig();
    MessagePlugin.success('保存成功');
  }).catch((error) => {
    MessagePlugin.error('保存失败');
  });
};
const getLabels = (value: any = settings.value) => {
  if (Helper.isObject(value)) {
    if (value.desc) {
      labelList.value.push(value.desc);
    }
    Object.keys(value).forEach((key) => {
      getLabels(value[key]);
    });
  }
};
const fetchSettings = () => {
  settings.value = configStore.configurations;
  labelList.value = [];
  getLabels(settings.value);
};

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
      <t-col :span="7" style="overflow-y: scroll;height: 70vh;">
        <InputSetting v-model:value="settings" label="设置" :path="''" />
      </t-col>
      <t-col :span="4" style="margin-left: 2vw;">
        <t-anchor>
          <t-anchor-item v-for="label in labelList" :href="`#${label}`" :title="label" />
        </t-anchor>
      </t-col>
    </t-row>


  </t-card>
</template>
<style>
.t-anchor__item a {
  all: unset;
  font-size: 2vh;
  margin: 0.1vh;
}
</style>