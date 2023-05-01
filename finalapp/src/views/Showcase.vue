<template>
    <div class="showcase">
        <h1 class="show_title">Pages showcase</h1>
        <div class="show_container">
            <div class="show_block" v-for="page in publicPages" :key="page.id">
                <img alt="" class="page-image" src="../assets/page.jpg">
                <router-link class="show_link" :to="{ name: 'PublicPage', params: { id: page.id } }">{{ page.name }}</router-link>
                <span class="show-user">User: {{ page.user }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

    export default {
        name: "Showcase",
        data() {
            return {
                publicPages: [], //initializing the array
            };
        },
        methods:{
            async getPublicPages(){
                const response = await axios.get('/public-pages/'); //getting the data from the api
                this.publicPages = response.data;  //setting the array to the response data
                },
            },

        mounted(){
            this.getPublicPages();

        },
    }
</script>

<style scoped>
    .show_block {
    border: #000000 solid 1px;
    width: 400px;
    height: 250px;
    margin: 1em;
    margin-bottom: 2em;
    margin-right: 2em;
    display: flex;
    flex-direction: column;
    }
    .show_title{
        font-family: "Inter";
        font-style: normal;
        font-weight: bold;
        font-size: 30px;
        line-height: 28px;
        text-align: center;
        color: #000000;
        margin-inline: 6em;
        margin-bottom: 1.5em;
        
    }

    .show_container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2em;
    margin-inline: 12em;
    }

    .show_link{
    font-family: "Inter";
    font-style: normal;
    font-weight: bold;
    font-size: 1.5em;
    line-height: 28px;
    color: #000000;
    text-align: initial;
    margin: 0.5em;
    text-decoration: none;
    width: fit-content;
    text-decoration: underline;
    }

    .show-user{
        margin-left: 0.8em;
    }

</style>