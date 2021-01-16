import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import './assets/styles.scss'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.config.productionTip = false

new Vue({
  render: (h) => h(App),
}).$mount('#app')
