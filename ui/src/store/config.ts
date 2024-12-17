import { defineStore } from 'pinia';
import { Configuration } from '../types/config';
import SettingApi from '../apis/setting';

export const useConfigStore = defineStore('config', {
  state: () => ({
    configurations: {} as Configuration,
  }),
  actions: {
    initConfig() {
      SettingApi.getSettings().then((res: any) => {
        this.configurations = res.data.data;
      });
    }
  },
});
