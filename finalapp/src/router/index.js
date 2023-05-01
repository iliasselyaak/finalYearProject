import { createRouter, createWebHistory } from 'vue-router'
import Showcase from '../views/Showcase.vue'
import Tutorial from '../views/Tutorial.vue'
import Signup from '../views/Signup.vue'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Editor from '../views/Editor.vue'
import PublicPage from '../views/PublicPage.vue'

const routes = [ // Define the routes
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/publicpage/:id',
    name: 'PublicPage',
    component: PublicPage
  },
  {
    path: '/showcase',
    name: 'Showcase',
    component: Showcase
  },
  {
    path: '/tutorial',
    name: 'Tutorial',
    component: Tutorial
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      requiresAuth: true, //requires authentication
    },
  },
  {
    path: '/editor/:id',
    name: "Editor",
    component: Editor,
    meta: {
      requiresAuth: true, //requires authentication
    },
  },
  

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Check if the user is authenticated
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (localStorage.getItem("token")) {
      next();
      return;
    }
    next("/login");
  } else {
    next();
  }
});




export default router
