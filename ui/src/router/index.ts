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
        path: "plugins",
        name: "plugins",
        component: () => import("@/views/Plugins.vue"),
      },
      {
        path: "config",
        name: "config",
        component: () => import("@/views/Config.vue"),
      },
      {
        path: "test",
        name: "test",
        component: () => import("@/views/Test.vue"),
      }
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
