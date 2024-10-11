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
        redirect: "/dashboard",
      },
      {
        path: "dashboard",
        name: "dashboard",
        component: () => import("@/views/Dashboard.vue"),
      },
      {
        path: "write",
        name: "write",
        component: () => import("@/views/Write.vue"),
      },
      {
        path: "upload",
        name: "upload",
        component: () => import("@/views/Upload.vue"),
      },
      {
        path: "settings",
        name: "settings",
        component: () => import("@/views/Settings.vue"),
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
