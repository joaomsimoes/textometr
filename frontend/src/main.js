import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import './assets/styles.scss'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'
import { faFacebook } from '@fortawesome/free-brands-svg-icons'
import { faEnvelope, faQuestionCircle } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faEnvelope, faMoon, faSun, faFacebook, faQuestionCircle)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  render: (h) => h(App),
}).$mount('#app')
