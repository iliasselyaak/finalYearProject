<template>
    <div class="signup">
        <form @submit.prevent = "submitForm">
            <div class="imgcontainer">
                <img src="../assets/login-signup.png" width="862" height="162">
            </div>
            <div class="signup-container">
                <input type="email" placeholder="EMAIL" name="username" v-model="username">
                <input type="password" placeholder="PASSWORD" name="password" v-model="password">
                <button class="btn-signup" type="submit">Sign Up</button>
            </div>
        </form>
        <div v-if="Object.keys(error).length > 0">
            <dl>
            <dt v-for="(values, name) in error" :key="name">
                <dl>
                <span class="error-text" v-for="value in values" :key="value">
                    {{ value }}
                </span>
                </dl>
            </dt>
            </dl>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return{ //Initialize data
            username:'',
            password:'',
            error:{},
        }
    },
    methods : {
        submitForm(){
            const formData = { //Form data
                username: this.username,
                password: this.password,
            }

            axios
                .post('/api/v1/users/', formData) //Post request to login
                .then(response => {
                    this.$router.push('/login') //Redirect to login page
                    console.log(response)
                })
                .catch(error => { //Catch error
                    this.error = error.response.data;
                    console.log(this.error)
                })
        }
    }
}
</script>

<style scoped>

    .signup {
        padding-top: 10em;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #3A4F39;
    }

    .signup-container{
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