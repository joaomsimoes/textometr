import { ViteSSG } from 'vite-ssg'
import App from './App.vue'
import Analyzer from './pages/Analyzer.vue'
import FrequencyCheck from './pages/FrequencyCheck.vue'
import './assets/styles.scss'

const routes = [
  { path: '/', component: Analyzer },
  { path: '/frequency-check', component: FrequencyCheck }
]

export const createApp = ViteSSG(App, { routes })
