import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {library} from '@fortawesome/fontawesome-svg-core'
import {fas} from '@fortawesome/free-solid-svg-icons'


library.add(fas) // Add all icons from the solid set to the library

import './assets/main.css' // Import the main css file

axios.defaults.baseURL = "http://127.0.0.1:8000" // Base URL for API calls

createApp(App).component('fa', FontAwesomeIcon).use(router, axios).use(store).mount('#app') // Mount the app
