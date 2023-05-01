<template>
    <div class="home">
        <img class="panel" src="../assets/logo.png" alt="Logo">
        <p class="intro">Elevate your online presence with VisionBuilder—effortlessly design, customize, and transform your website ideas into code!</p>
        <router-link to="/dashboard" class="nav-link"><button class="button">Start Building!!</button></router-link>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style lang="scss" scoped>
    .home{
        text-align: center;
    }
    .panel{
        padding-top: 8em;
        width: 855px;
        height: 160px;
        left: 291px;
        top: 193px;
    }

    .intro{
        padding-top: 2em;
        font-family: "Inter";
        font-style: normal;
        font-weight: normal;
        font-size: 30px;
        line-height: 28px;
        text-align: center;
        color: #000000;
        margin-inline: 6em;
    }

    .button{
        text-decoration: none;
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 22px;
        background-color: #3A4F39;
        border-radius: 4px;
        border: none;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        padding: 20px 40px;
        margin-top: 3em;
        gap: 10px;
        color: #FFFFFF;
        cursor: pointer;
        box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    }
</style>