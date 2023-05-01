<template>
    <div class="login">
        <form ref="loginForm" @submit.prevent="login">
            <div class="imgcontainer">
                <img src="../assets/login-signup.png" width="862" height="162">
            </div>
            <div class="login-container">
                <input type="email" label="email" placeholder="EMAIL" name="username" v-model="username">
                <input type="password" label="password" placeholder="PASSWORD" name="password" v-model="password">
                <button class="btn-login" type="submit">LOGIN</button>
                <router-link to="/signup" class="nav-link"><button class="btn-signup">SIGNUP</button></router-link>
            </div>
        </form>
        <div v-if="Object.keys(error).length > 0">
            <dl>
                <dt v-for="(values, name) in error" :key="name">
                <dl>
                    <div v-if="Array.isArray(values)">
                    <span class="error-text" v-for="value in values" :key="value">
                        {{ value }}
                    </span>
                    </div>
                    <div v-else>
                    <span class="error-text">
                        {{ values }}
                    </span>
                    </div>
                </dl>
                </dt>
            </dl>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'LogIn',
        data() {
            return{ //Initialize data
                username:"",
                password:"",
                error:{},
            }
        },
        methods : {
            login(){ //Login method
                const formData = { //Form data
                    username: this.username,
                    password: this.password,
                }
                //initialize autorization header
                axios.defaults.headers.common["Authorization"] = "";
                axios
                    .post("api/v1/token/login", formData) //Post request to login
                    .then((response) => {
                        const token = response.data.auth_token
                        this.$store.commit("setToken", token)
                        axios.defaults.headers.common['Authorization'] = "Token " + token; //Set token 
                        localStorage.setItem("token", token);
                        this.$router.push("/dashboard"); //Redirect to dashboard
                        
                    })
                    .catch(error => { //Catch error
                        this.error = error.response.data;
                        console.log(this.error)
                        
                    });
            },
        },
    };
</script>

<style scoped>

.login {
    padding-top: 10em;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #3A4F39;
}

.login-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: transparent;
    margin: 3em;
}

input{
    box-sizing: border-box;
    width: 28em;
    height: 4em;
    margin: 0.5em;
    border-radius: 4px;
    border: 1px solid #ffffff;
    background-color: #3A4F39;
    color: white;
    margin: 1em;
    padding: 2em;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
}


::placeholder{
        font-weight: 100;
        color: white;
    }

.btn-login{
    width: 18.8em;
    height: 3em;
    border-radius: 4px;
    background-color: #1FC93A;
    color: white;
    margin: 1em;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    font-size: 20px;
}

.btn-signup{
    width: 18.8em;
    height: 3em;
    border-radius: 4px;
    background-color: #ffffff;
    color: #3A4F39;
    margin: 1em;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    font-size: 20px;

}

.error-text{
    color: red;
    font-size: 25px;
    font-weight: 200;
    text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
}



</style>