<template>
    <div class="dashboard">
        <h1 class="dash_title">Dashboard</h1>
        <span class="dash_user" :src="user_data">User: {{ user_data }}</span>
        <div class="create-page">
          <input type="text" v-model="newPageName" placeholder="Enter page name">
          <button class="btn-create" @click="createPage">Create Page</button>
        </div>
        <h2 class="my_pages">My Pages</h2>
        <div class="dash_container">
          <div class="dash_block" v-for="page in pages" :key="page.id">
            <img @click="deletePage(page)" alt="" class="btn-delete" src="../assets/close.png">
            <img alt="" class="page-image" src="../assets/page.jpg">
            <router-link class="dash_link" :to="{ name: 'Editor', params: { id: page.id } }">{{ page.name }}</router-link>
            <label class="public-label">Public</label>
            <input type="checkbox" v-model="page.public" @change="updatePagePublicStatus(page)" />
          </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
    export default {
        data() {
          return {
            user_data: '',
            pages: [],
            newPageName: "",
          };
        },
        mounted(){
          this.getUser(); // this will call the method on page load to get username
        },

        // this will call the method on page load to get all pages
        async created(){
          const response = await axios.get('/pages/');
          this.pages = response.data;
        },
        methods: {
          // this will get the username
          getUser(e){
            axios.get("/api/v1/users/me").then((response) => {
              console.log(response.data)
              this.user_data = response.data.username;
            })
            .catch(error => {
              console.log(error);
            });
          },

          // this will update the page's public status
          async updatePagePublicStatus(page) {
            try {
              await axios.put(`/pages/${page.id}/`, { public: page.public });
            } catch (error) {
              console.error("Error updating the page's public status:", error);
            }
          },

          // this will create a new page
          async createPage() {
            try {
              let name = this.newPageName.trim() || `Untitled ${this.pages.length + 1}`;
                // Check if a page with the same name already exists
                const existingPage = this.pages.find(page => page.name === name);
                if (existingPage) {
                  let count = 1;
                  while (this.pages.find(page => page.name === `${name} (${count})`)) {
                    count++;
                  }
                  name = `${name} (${count})`;
                }
              const response = await axios.post("/pages/", {
                name: name,
                content: {}
              });

              this.pages.push(response.data);
              this.newPageName = "";
              this.$router.push({ name: "Editor", params: { id: response.data.id } });
            } catch (error) {
              console.error("Error creating a new page:", error);
            }
          },

          // this will delete a page
          async deletePage(page) {
            try {
              await axios.delete(`/pages/${page.id}/`);
              const index = this.pages.indexOf(page);
              this.pages.splice(index, 1);
            } catch (error) {
              console.error('Error deleting the page:', error);
            }
          },
        },
        
    }
</script>

<style lang="scss" scoped>
.dashboard{
    text-align: center;
    margin-bottom: 1em;
    }

    
.public-label {
  font-family: "Inter";
  font-style: normal;
  font-weight: normal;
  font-size: 1em;
  color: #000000;
  margin: 1em;
  position: absolute;
  bottom: 1.5em;
  right: 0;

}

input[type="checkbox"] {
  position: absolute;
  bottom: 1em;
  right: 2.2em;
}

.dash_title{
    font-family: "Inter";
    font-style: normal;
    font-weight: bold;
    font-size: 30px;
    line-height: 28px;
    text-align: center;
    color: #000000;
    margin-inline: 6em;
    margin-bottom: 0.5em;
    
}

.dash_user{
    font-family: "Inter";
    font-style: normal;
    font-weight: normal;
    font-size: 20px;
    line-height: 28px;
    color: #000000;
}

.my_pages{
    font-family: "Inter";
    font-style: normal;
    font-weight: bold;
    font-size: 1.5em;
    line-height: 28px;
    color: #000000;
    text-align: initial;
    margin-top: 3em;
    margin-inline: 4em;
}


.dash_container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 2em;
  margin-inline: 12em;
}

.dash_block {
  position: relative;
  border: #000000 solid 1px;
  width: 400px;
  height: 250px;
  margin: 1em;
  margin-bottom: 2em;
  margin-right: 2em;
  display: flex;
  flex-direction: column;
}

.page-image{
  width: 400px;
  height: 170px;
  top: 0;
}

.dash_link{
  font-family: "Inter";
  font-style: normal;
  font-weight: bold;
  font-size: 1.5em;
  line-height: 28px;
  color: #000000;
  text-align: initial;
  margin: 1em;
  text-decoration: none;
  width: fit-content;
  text-decoration: underline;
}

.btn-delete{
  position: absolute;
  width: 20px;
  height: 20px;
  right:0;
  top: 0;
  margin: 1em;
  cursor: pointer;
}

input[type="text"]{
    box-sizing: border-box;
    width: 28em;
    height: 4em;
    margin: 0.5em;
    border-radius: 4px;
    border: 1px solid #000000;
    background-color: #ffffff;
    margin: 1em;
    padding: 2em;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
}

.btn-create{
    width: 10em;
    height: 3em;
    border-radius: 4px;
    background-color: #1FC93A;
    color: white;
    margin: 1em;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    font-size: 18px;
}
</style>