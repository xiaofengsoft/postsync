import { defineStore } from 'pinia';
import { SiteStatus } from '../types/site';

export const useSiteStore = defineStore('site', {
  state: () => ({
    siteStatuses: [] as SiteStatus[],
  }),
  actions: {
    isEmpty() {
      return this.siteStatuses.length === 0;
    },
    addSiteStatus(siteStatus: SiteStatus) {
      this.siteStatuses.push(siteStatus);
    },
    updateSiteStatus(id: string, siteStatus: 0 | 1) {
      this.siteStatuses = this.siteStatuses.map((item: SiteStatus) =>
        item.id === id ? { ...item, status: siteStatus } : item
      );
    },
  },
});
