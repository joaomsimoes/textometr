import { ViteSSG } from 'vite-ssg/single-page'
import App from './App.vue'
import './assets/styles.scss'

if (typeof navigator !== 'undefined') {
  navigator.serviceWorker.getRegistrations().then(function (registrations) {
    for (const registration of registrations) {
      registration.unregister()
    }
  })
}

export const createApp = ViteSSG(App)
