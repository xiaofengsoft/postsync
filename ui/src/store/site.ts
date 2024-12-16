import { defineStore } from 'pinia';
import { SiteStatus } from '../types/site';

export const useSiteStore = defineStore('site', {
  state: () => ({
    siteStatuses: [] as SiteStatus[],
  }),
  actions: {
    addSiteStatus(siteStatus: SiteStatus) {
      this.siteStatuses.push(siteStatus);
    },
    updateSiteStatus(siteStatus: SiteStatus) {
      this.siteStatuses = this.siteStatuses.map((item) =>
        item.id === siteStatus.id ? siteStatus : item
      );
    },
  },
});
