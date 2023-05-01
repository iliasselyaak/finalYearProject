<template>
  <div class="app-container">
    <nav>
        <Navbar :logout="logout"/>
    </nav>
      <router-view />
    <footer id="footer">
      <img src="./assets/footer.png" alt="Logo">
      <p>Copyright © Iliass Elyaakoubi Benssaleh</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from './components/Navbar.vue';
import { mapGetters } from "vuex";


export default {
    name: "App",
    methods: {
          logout() { //Logout function
            axios.post("/api/v1/token/logout").then((response) => { //Post request to logout
              localStorage.removeItem("token");
              this.$store.commit("removeToken"); //Remove token from store
              this.$router.push("/");

              //Clear token
              axios.defaults.headers.common["Authorization"] = ""; //Clear authorization header
            });
          },
        },
    computed: {
          ...mapGetters({
            isAuthenticated: "isAuthenticated", //Get isAuthenticated from store
          }),
    },
    beforeCreate() {
        this.$store.commit("initializeStore");
        const token = this.$store.state.token;
        if (token) {
            axios.defaults.headers.common["Authorization"] = `Token ${token}`; //Set token
        }
        else {
            axios.defaults.headers.common["Authorization"] = ""; //Clear authorization header
        }
    },
    components: { Navbar }
}
</script>

<style lang="scss">

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
}

.app-container {
  display: grid;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
  width: 100%;
}

nav {
  
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

footer {
  background-color: #3A4F39;
  color: white;
  text-align: center;

  img{
    text-align: center;
    width: 165px;
    height: 31px;
  }
  
}

#footer{
  padding: 30px;
  
}


</style>
