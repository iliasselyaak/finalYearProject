<template>
    <div class="tutorial">
        <h1>How it works</h1>
        <div class="body">
            <h2>How to start building?</h2>
            <div class="content">
                <p>1. Click on Start Building on the Home page. This will redirect you to the Dashboard. </p>
                <p class="subsection">a.If you are not logged in, then you will be redirected to login or make a new account.</p>
                <br>
                <p>2.Create a new page using the input field or select an existing page (if already created). </p>
                <img src="../assets/dashboard.jpeg">
                <p>3. You are now inside the editor, where you can load templates, drag blocks and export you code!!</p>
                <img src="../assets/editor.jpeg">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style lang="scss" scoped>
    .tutorial h1{
        text-align: center;
        font-weight: 700;
        font-size: 2em;
    }

    .tutorial h2{
        font-weight: 700;
        font-size: 1.2em;
        margin-bottom: 1em;
    }

    .body{
        margin: 4em;
    }

    img{
        margin-bottom: 2em;
        border: black 1px solid;
        height:40em;
    }

    p{
        margin-bottom: 0.5em;
    }

    .subsection{
        margin-left: 2em;
    }

</style>