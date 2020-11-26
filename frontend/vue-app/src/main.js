import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Vuelidate from 'vuelidate'
import router from './router'
import App from './App.vue'


// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


Vue.use(Vuelidate)

Vue.config.productionTip = false


new Vue({
  el: '#app',
  render: h => h(App),
  router
})