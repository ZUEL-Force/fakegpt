import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '@/css/global.css'
import '@/assets/font/index.css'
import 'vant/lib/index.css'
// touch-diffcult!!!
// import vueTouch from 'kim-vue-touch'
// import vueTouch from 'vue-touch'
// app.use(vueTouch,{name:'v-touch'})
// import VueAwesomeSwiper from "vue-awesome-swiper";
import './permission'
import Vant from 'vant'
const app=createApp(App)
// app.use(VueAwesomeSwiper)
app.use(Vant)
app.use(store).use(router).mount('#app')

