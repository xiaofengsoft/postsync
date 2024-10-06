import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: resolve(__dirname, "./src"),
      },
    ],
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    open: true,
    proxy: {
      "/api": {
        target: "http://localhost:54188", //目标地址，一般是指后台服务器地址
        changeOrigin: true, //是否跨域
        rewriteWsOrigin: true, //是否重写websocket请求地址
        rewrite(path) {
          return path.replace(/^\/api/, "/api"); //重写路径，将/api替换成空字符串
        },
      },
    },
  },
});
