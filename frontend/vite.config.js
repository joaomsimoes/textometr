import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Components from "unplugin-vue-components/vite";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/analyze": "https://textometr.ru", // 'http://backend:8888'
    },
  },
  plugins: [
    Components({
      extensions: ["vue"],
      include: [/\.vue$/, /\.vue\?vue/],
    }),
    vue(),
  ],
});
