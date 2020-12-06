import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSession from 'vue-session'
import router from './router'
import App from './App.vue'


// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

var options = {
  persist: true
}
Vue.use(VueSession, options)

Vue.config.productionTip = false


Vue.prototype.$api_hosts= {
  miband_api: '192.168.11.119',
  miband_db_api: '192.168.11.119',
  user_db_api: '192.168.11.119'
}
Vue.prototype.$api_ports = {
  miband_api: '5001',
  miband_db_api: '5002',
  user_db_api: '5000'
}

new Vue({
  el: '#app',
  render: h => h(App),
  router,
})