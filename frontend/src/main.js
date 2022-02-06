import { ViteSSG } from 'vite-ssg/single-page'
import App from './App.vue'
import './assets/styles.scss'
import { registerSW } from 'virtual:pwa-register'

const updateSW = registerSW({
  onRegisterError(error) {}
})

export const createApp = ViteSSG(App)
