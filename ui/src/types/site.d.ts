// 0 代表 未登录
// 1 代表 已登录
export interface SiteStatus {
  id: string
  name: string
  status: 0 | 1
}