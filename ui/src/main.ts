import { createApp } from "vue";
import TDesign from "tdesign-vue-next";
import "./assets/style/theme.css";
import "./assets/style/base.css";
import "./assets/style/global.css";
import Router from "./router/index";
import App from "./App.vue";

createApp(App).use(TDesign).use(Router).mount("#app");
