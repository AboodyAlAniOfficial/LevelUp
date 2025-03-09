import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000/'//Default Django localhost (Change it if we use a new domain later)

createApp(App).use(store).use(router, axios).mount('#app')
