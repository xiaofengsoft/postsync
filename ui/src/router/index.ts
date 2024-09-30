import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Layout",
    component: () => import("@/views/Layout.vue"),
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@/views/Dashboard.vue"),
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/Dashboard.vue"),
      },
      {
        path: "write",
        name: "Write",
        component: () => import("@/views/Write.vue"),
      },
      {
        path: "upload",
        name: "Upload",
        component: () => import("@/views/Upload.vue"),
      },
      {
        path: "settings",
        name: "Settings",
        component: () => import("@/views/Settings.vue"),
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
