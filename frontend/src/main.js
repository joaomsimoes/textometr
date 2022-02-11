import { ViteSSG } from 'vite-ssg/single-page'
import App from './App.vue'
import './assets/styles.scss'

export const createApp = ViteSSG(App)
