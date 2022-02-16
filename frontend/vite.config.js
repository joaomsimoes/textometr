import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      // '/api': 'https://textometr.ru'
      '/api': {
        target: 'http://127.0.0.1:8000',
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  plugins: [
    Components({
      extensions: ['vue'],
      include: [/\.vue$/, /\.vue\?vue/]
    }),
    vue()
  ]
})
