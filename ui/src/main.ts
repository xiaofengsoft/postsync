import { createApp } from "vue";
import TDesign from "tdesign-vue-next";
import "./assets/style/theme.css";
import "./assets/style/base.css";
import "./assets/style/global.css";
import Router from "./router/index";
import App from "./App.vue";
import { createPinia } from "pinia";
import clickOnceDirective from "./directives/click-once.directive";

const pinia = createPinia();
const app = createApp(App).use(TDesign).use(Router);
app.use(pinia);
app.directive("click-once", clickOnceDirective);
app.mount("#app");
