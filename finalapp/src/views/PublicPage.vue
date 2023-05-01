<template>
    <div>
      <iframe ref="iframe" @load="applyStyles"></iframe>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    data() {
      return {
        page_code: {
          html: '',
          css: '',
        },
      };
    },
    methods: {

      applyStyles() { // this method will apply the styles to the iframe
        const iframe = this.$refs.iframe;
        const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;

        // Open a new document within the iframe
        iframeDocument.open();
        iframeDocument.write('<!DOCTYPE html><html><head></head><body></body></html>');
        iframeDocument.close();

        const body = iframeDocument.body;
        const head = iframeDocument.head;

        // Add the HTML to the body
        body.innerHTML = this.page_code.html;

        // Add the CSS to the head
        const styleElement = document.createElement('style');
        styleElement.innerHTML = this.page_code.css;
        head.appendChild(styleElement);

        // Find the script tags in the HTML and create new script tags to append to the body
        const scriptTags = body.querySelectorAll('script');
        scriptTags.forEach((scriptTag) => {
          const newScriptTag = iframeDocument.createElement('script');
          newScriptTag.text = scriptTag.text;
          scriptTag.parentNode.replaceChild(newScriptTag, scriptTag);
        });
      },

      // this will get the page's code
      async getPublicPagesCode(){
        const id = this.$route.params.id;
        const response = await axios.get(`/public-pages/${id}/`); //get request to get the page's code
        this.page_code = response.data[0]; 
      },
      
    },
    async mounted() { // this will call the method on page load to get the page's code
      await this.getPublicPagesCode();
      this.applyStyles();
    },
  };
  </script>

  <style scoped>
    iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
</style>