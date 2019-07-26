import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import "prismjs";
import "./modules/prismjs/prism-python.min";
import "prismjs/themes/prism.css";
import VueSweetalert2 from 'vue-sweetalert2';

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(BootstrapVue)
Vue.use(VueSweetalert2);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

