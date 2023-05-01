<template>
    <nav class="navbar">
      <div class="container">
        <div class="left">
            <router-link to="/" class="logo"><img src="../assets/logo.png" alt="Logo"></router-link>
            <router-link to="/showcase" class="nav-link">Showcase</router-link>
            <router-link to="/tutorial" class="nav-link">How it works</router-link>
        </div>
        <div class="right" v-if="!isAuthenticated">
            <router-link to="/login" class="nav-link">Login</router-link>
            <router-link to="/signup" class="nav-link signup-link">Get Started</router-link>
        </div>
        <div class="right"  v-if="isAuthenticated">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            <button  @click.native=logout class="nav-link logout" to="/">Logout</button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import axios from "axios";

    export default {
        name: "Navbar",
        data() {
          return {
            user_data: '',
          };
        },
        props:{
          logout: Function, //Logout function from App.vue
        },
        computed: {
          ...mapGetters({
            isAuthenticated: "isAuthenticated", //Get the isAuthenticated getter from the store
        }),
      },
    };
  </script>
  
  <style lang="scss">

    .navbar {
    width: 100%;
    background-color: #FFFFFF;
    padding: 30px 0;
    }

    .container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0 3em;
    }

    .left,
    .right {
        display: flex;
        align-items: center;
    }


    .left{
      .nav-link {
          color: #000;
          text-decoration: none;
          font-family: 'Inter';
          font-style: normal;
          font-weight: 400;
          font-size: 22px;
          margin-inline: 3em;

          &:hover {
          color: #ccc;
          }
      }
    }

    .right{
      .nav-link {
          color: #000;
          text-decoration: none;
          font-family: 'Inter';
          font-style: normal;
          font-weight: 400;
          font-size: 22px;
          margin-inline: 1em;

          &:hover {
          color: #ccc;
          }
      }
    }

    .signup-link{
      background-color: #3A4F39;
      border-radius: 4px;
      border: none;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding: 17px 30px;
      gap: 10px;
      color: #FFFFFF!important; 
      cursor: pointer;
      box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    }

    .logout{
      text-decoration: none;
      font-family: 'Inter';
      font-style: normal;
      font-weight: 400;
      font-size: 22px;
      background-color: #3A4F39;
      border-radius: 4px;
      border: none;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding: 10px 20px;
      gap: 10px;
      color: #FFFFFF!important;
      cursor: pointer;
      box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    }

    .logo {
      width: 187.55px;
      height: 35.09px;
      margin-right: 3em;
    }

    .logo img {
      max-width: 100%; 
      max-height: 100%;
    }
    
</style>