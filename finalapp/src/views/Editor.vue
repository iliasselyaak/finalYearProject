<template>
    <div class="editor-container">
      <div class="header">
        <h1 class="page-name">{{pageName}}</h1>
        <div class="name-change">
          <input class="enter-name" type="text" v-model="newPageName" placeholder="Enter new name" />
          <button class="btn-change" @click="changePageName">Change Name</button>
        </div>
      </div>
      <div class="blocks-wrapper">
        <div id="blocks" class="column">
          <h1 class="templates">Templates</h1>
          <button id="replace-code-btn">Load</button>
          <h1 class="templates">Blocks</h1>
        </div>
        <div id="editor-canvas" class="middle-column">
          <div class="editor-top">
              <div class="editor-actions" ref="editorActions"></div>
              <div class="panel__devices"></div>
          </div>
          <div id="gjs">
          </div>
        </div>
        <div id="settings" class="column">
          <div class="panel__switcher" ref="panelSwitcher"></div>
          <div class="layers-container"></div>
          <div class="styles-container"></div>
          <div class="traits-container"></div>
        </div>
      </div>

    </div>
</template>

<script>
//Libaries
import axios from "axios";
import grapesjs from "grapesjs";
import "grapesjs/dist/grapes.min.js";
import "grapesjs/dist/css/grapes.min.css";
import blocksBasic from 'grapesjs-blocks-basic';
import exportP from 'grapesjs-plugin-export';
import formsP from 'grapesjs-plugin-forms';
import tabs from 'grapesjs-tabs';
import codeBlock from 'grapesjs-custom-code';
import { html as beautifyHtml, css as beautifyCss } from 'js-beautify';




export default{
    name: "Editor",
    data() {
      return {   
        pageName: "", 
        newPageName: "",
      }
    },
    

    methods: {
      // this will get the page name
      async getPageName() {
        const id = this.$route.params.id;
        try {
          const response = await axios.get(`/pages/${id}/`); 
          this.pageName = response.data.name;
        } catch (error) {
          console.error("Error fetching page name:", error);
        }
      },

      // this will change the page name
      async changePageName() {
        if (!this.newPageName || this.newPageName.trim() === "") {
          alert("Please enter a new page name.");
          return;
        }

        // Send a PUT request to the API to update the page name
        const id = this.$route.params.id;
        try {
          await axios.put(`/pages/${id}/`, { name: this.newPageName }); 
          this.pageName = this.newPageName;
          this.newPageName = "";
        } catch (error) {
          console.error("Error changing page name:", error);
        }
      },

      // this will open the template
      openTemplateModal(editor) {
        const modalContent = `
          <div>
            <h2>Select a Template</h2>
            <select id="template-select">
              <option value="about">About Us</option>
              <option value="contact">Contact Me</option>
            </select>
            <button id="load-template-btn">Load Template</button>
          </div>
        `;

        // Create and open the GrapesJS modal
        const modal = editor.Modal;
        modal.setTitle('Load a Template');
        modal.setContent(modalContent);
        modal.open();

        // Add a click event listener to the 'Load Template' button
        document.getElementById('load-template-btn').addEventListener('click', function() {
          const selectedTemplate = document.getElementById('template-select').value;
          let newHtmlCode = '';

          if (selectedTemplate === 'about') {
            newHtmlCode = `
              <h1>About Us</h1>
              <p>Welcome to our website! We are a company that specializes in XYZ. Our mission is to provide the best services to our clients.</p>
            `;
          } else if (selectedTemplate === 'contact') {
            newHtmlCode = `
              <h1>Contact Me</h1>
              <form>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name">
                <br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email">
                <br>
                <label for="message">Message:</label>
                <textarea id="message" name="message"></textarea>
                <br>
                <button type="submit">Submit</button>
              </form>
            `;
          }

          editor.setComponents(newHtmlCode);
          modal.close(); // Close the modal after loading the template
        });
      }

    },

    mounted() {
        this.getPageName(); // this will get the page name
        const id = this.$route.params.id; // this will get the page id
        const editor = grapesjs.init({ // this will initialize the editor
          container: "#gjs",
          height: "100%",
          width: "100%",
          fromElement: true,
          allowScripts: 1,
          plugins: [blocksBasic, exportP, formsP, tabs, codeBlock],  // plugins
          pluginsOpts:{
            [tabs]: {tabsBlock: {category: 'Extra'}},
            [blocksBasic]:  {
              category:"Columns",
              flexGrid: true,
              blocks: ['column1', 'column2', 'column3', 'column3-7']
            },
          } ,
          storageManager: { //store manager configurations
            type: "remote",
            options: {
              remote: {
                // Load and save templates from a django server
                onStore: (data, editor) => {
                  const pagesHtml = editor.Pages.getAll().map(page => {
                    const component = page.getMainComponent();
                    return {
                      html: editor.getHtml({ component }),
                      css: editor.getCss({ component })
                    }
                  });
                  return { data, pagesHtml };
                },
                
                onLoad: result => result.data,
              }
            },
            autosave: true,
            autoload: true,
            contentTypeJson: false,
            setStepsBeforeSave: 1,
            contentTypeJson: true,
            storeComponents: true,
            storeStyles: true,
            storeHtml: true,
            storeCss: true,
          },
          deviceManager: { //device manager configurations
            devices: [{
                name: 'Desktop',
                width: '', // default size
              }, {
                name: 'Mobile',
                width: '320px', // this value will be used on canvas width
                widthMedia: '480px', // this value will be used in CSS @media
            }]
          },
          blockManager: { //block manager configurations
            appendTo: '#blocks',
            blocks: [
              {
                id: 'section', // Section block
                label:'Section', 
                attributes: { class:'gjs-fonts gjs-f-h1p' },
                content: `<section> //Section's code
                  <h1>This is a simple title</h1>
                  <div>This is just a Lorem text: Lorem ipsum dolor sit amet</div>
                </section>`,
                category: 'Text',
              }, {
                id: 'text', // Text block
                attributes:{class:'gjs-fonts gjs-f-text'},
                label: 'Text',
                content: '<div data-gjs-type="text">Insert your text here</div>', // Text's code
                category: 'Text',
              },{
                id: 'heading', // Heading block
                attributes:{class:'gjs-fonts gjs-f-text'},
                label: 'Heading',
                content: '<h1>Insert your Heading here</h1>', // Heading's code
                category: 'Text',
              }, {
                id: 'image', // Image block
                attributes:{class:'gjs-fonts gjs-f-image'},
                label: 'Image',
                select: true,
                content: { type: 'image' },
                // this triggers `active` event on dropped components and the `image`
                activate: true,
                category: 'Extra',
              }
            ],
          },
          layerManager: { //layer manager configurations
          appendTo: '.layers-container'
          },
          //default panel as a sidebar to contain layers
          panels: {
            defaults: [
              
              {
                id: 'panel-switcher',
                el: '.panel__switcher',
                buttons: [{
                    id: 'show-layers', //layer button
                    active: true,
                    label: 'Layers',
                    command: 'show-layers',
                    className:'icon-layers',
                    togglable: false,
                  }, {
                    id: 'show-style', //style button
                    active: true,
                    label: 'Styles',
                    command: 'show-styles',
                    className:'icon-styles',
                    togglable: false,
                  },
                  {
                    id: 'show-traits', //trait button
                    active: true,
                    label: 'Traits',
                    command: 'show-traits',
                    className:'icon-settings',
                    togglable: false,
                  }],
              },
              {
                id: 'panel-devices',
                el: '.panel__devices', //Changes the canvas size to desktop or mobile
                buttons: [{
                    id: 'device-desktop',
                    label: 'D',
                    command: 'set-device-desktop',
                    active: true,
                    togglable: false,
                    className:'icon-desktop',
                  }, {
                    id: 'device-mobile',
                    label: 'M',
                    command: 'set-device-mobile',
                    togglable: false,
                    className:'icon-mobile',
                }],
              }
            ]
          },
          traitManager: { //trait manager configurations
            appendTo: '.traits-container',
          },
          selectorManager: { //selector manager configurations
            appendTo:'.styles-container'
          },
          styleManager: { //style manager configurations
          appendTo: '.styles-container',
          sectors: [{
              name: 'General', //General settings
              properties:[
                {
                  extend: 'float',
                  type: 'radio',
                  default: 'none',
                  options: [
                    { value: 'none', className: 'fa fa-times'},
                    { value: 'left', className: 'fa fa-align-left'},
                    { value: 'right', className: 'fa fa-align-right'}
                  ],
                },
                'display',
                { extend: 'position', type: 'select' },
                'top',
                'right',
                'left',
                'bottom',
              ],
            }, {
                name: 'Dimension', //Dimension settings
                open: false,
                properties: [
                  'width',
                  'height',
                  'max-width',
                  'min-height',
                  'margin',
                  'padding'
                ],
              },{
                name: 'Typography', //Typography settings
                open: false,
                properties: [
                    'font-family',
                    'font-size',
                    'font-weight',
                    'letter-spacing',
                    'color',
                    'line-height',
                    {
                      extend: 'text-align',
                      options: [
                        { id : 'left',  label : 'Left',    className: 'fa fa-align-left'},
                        { id : 'center',  label : 'Center',  className: 'fa fa-align-center' },
                        { id : 'right',   label : 'Right',   className: 'fa fa-align-right'},
                        { id : 'justify', label : 'Justify',   className: 'fa fa-align-justify'}
                      ],
                    },
                    {
                      property: 'text-decoration',
                      type: 'radio',
                      default: 'none',
                      options: [
                        { id: 'none', label: 'None', className: 'fa fa-times'},
                        { id: 'underline', label: 'underline', className: 'fa fa-underline' },
                        { id: 'line-through', label: 'Line-through', className: 'fa fa-strikethrough'}
                      ],
                    },
                    'text-shadow'
                ],
              },{
                name: 'Decorations', //Decorations settings
                open: false,
                properties: [
                  'opacity',
                  'border-radius',
                  'border',
                  'box-shadow',
                  'background',
                  'background-color' // { id: 'background-bg', property: 'background', type: 'bg' }
                ],
              },{
                name: 'Extra', //Extra settings
                open: false,
                buildProps: [
                  'transition',
                  'perspective',
                  'transform'
                ],
              },{
                name: 'Flex', //Flex settings
                open: false,
                properties: [{
                  name: 'Flex Container',
                  property: 'display',
                  type: 'select',
                  defaults: 'block',
                  list: [
                    { value: 'block', name: 'Disable'},
                    { value: 'flex', name: 'Enable'}
                  ],
                },{
                  name: 'Flex Parent', 
                  property: 'label-parent-flex',
                  type: 'integer',
                },{
                  name: 'Direction', 
                  property: 'flex-direction',
                  type: 'radio',
                  defaults: 'row',
                  list: [{
                    value: 'row',
                    name: 'Row',
                    className: 'icons-flex icon-dir-row',
                    title: 'Row',
                  },{
                    value: 'row-reverse',
                    name: 'Row reverse',
                    className: 'icons-flex icon-dir-row-rev',
                    title: 'Row reverse',
                  },{
                    value: 'column',
                    name: 'Column',
                    title: 'Column',
                    className: 'icons-flex icon-dir-col',
                  },{
                    value: 'column-reverse',
                    name: 'Column reverse',
                    title: 'Column reverse',
                    className: 'icons-flex icon-dir-col-rev',
                  }],
                },{
                  name: 'Justify',
                  property: 'justify-content',
                  type: 'radio',
                  defaults: 'flex-start',
                  list: [{
                    value: 'flex-start',
                    className: 'icons-flex icon-just-start',
                    title: 'Start',
                  },{
                    value: 'flex-end',
                    title: 'End',
                    className: 'icons-flex icon-just-end',
                  },{
                    value: 'space-between',
                    title: 'Space between',
                    className: 'icons-flex icon-just-sp-bet',
                  },{
                    value: 'space-around',
                    title: 'Space around',
                    className: 'icons-flex icon-just-sp-ar',
                  },{
                    value: 'center',
                    title: 'Center',
                    className: 'icons-flex icon-just-sp-cent',
                  }],
                },{
                  name: 'Align',
                  property: 'align-items',
                  type: 'radio',
                  defaults: 'center',
                  list: [{
                    value: 'flex-start',
                    title: 'Start',
                    className: 'icons-flex icon-al-start',
                  },{
                    value: 'flex-end',
                    title: 'End',
                    className: 'icons-flex icon-al-end',
                  },{
                    value: 'stretch',
                    title: 'Stretch',
                    className: 'icons-flex icon-al-str',
                  },{
                    value: 'center',
                    title: 'Center',
                    className: 'icons-flex icon-al-center',
                  }],
                },{
                  name: 'Flex Children',
                  property: 'label-parent-flex',
                  type: 'integer',
                },{
                  name: 'Order',
                  property: 'order',
                  type: 'integer',
                  defaults: 0,
                  min: 0
                },{
                  name: 'Flex',
                  property: 'flex',
                  type: 'composite',
                  properties  : [{
                    name: 'Grow',
                    property: 'flex-grow',
                    type: 'integer',
                    defaults: 0,
                    min: 0
                  },{
                    name: 'Shrink',
                    property: 'flex-shrink',
                    type: 'integer',
                    defaults: 0,
                    min: 0
                  },{
                    name: 'Basis',
                    property: 'flex-basis',
                    type: 'integer',
                    units: ['px','%',''],
                    unit: '',
                    defaults: 'auto',
                  }],
                },{
                  name: 'Align',
                  property: 'align-self',
                  type: 'radio',
                  defaults: 'auto',
                  list: [{
                    value: 'auto',
                    name: 'Auto',
                  },{
                    value: 'flex-start',
                    title: 'Start',
                    className: 'icons-flex icon-al-start',
                  },{
                    value   : 'flex-end',
                    title: 'End',
                    className: 'icons-flex icon-al-end',
                  },{
                    value   : 'stretch',
                    title: 'Stretch',
                    className: 'icons-flex icon-al-str',
                  },{
                    value   : 'center',
                    title: 'Center',
                    className: 'icons-flex icon-al-center',
                  }],
                }]
              }
            ],
        },
        });


        // Commands for changin canvas size
        editor.Commands.add('set-device-desktop', {
          run: editor => editor.setDevice('Desktop')
        });
        editor.Commands.add('set-device-mobile', {
          run: editor => editor.setDevice('Mobile')
        });

        //close all blocks
        let categories = editor.BlockManager.getCategories();
        categories.each(categories => categories.set('open', false));

        //add layers to the sidebar
        editor.Commands.add('show-layers', {
          getRowEl(editor) { return editor.getContainer().closest('.editor-container'); },
          getLayersEl(row) { return row.querySelector('.layers-container') },

          run(editor, sender) {
            const lmEl = this.getLayersEl(this.getRowEl(editor));
            lmEl.style.display = '';
          },
          stop(editor, sender) {
            const lmEl = this.getLayersEl(this.getRowEl(editor));
            lmEl.style.display = 'none';
          },
        });
        //add styles to the sidebar
        editor.Commands.add('show-styles', {
          getRowEl(editor) { return editor.getContainer().closest('.editor-container'); },
          getStyleEl(row) { return row.querySelector('.styles-container') },

          run(editor, sender) {
            const smEl = this.getStyleEl(this.getRowEl(editor));
            smEl.style.display = '';
          },
          stop(editor, sender) {
            const smEl = this.getStyleEl(this.getRowEl(editor));
            smEl.style.display = 'none';
          },
        });
        //add traits to the sidebar
        editor.Commands.add('show-traits', {
          getTraitsEl(editor) {
            const row = editor.getContainer().closest('.editor-container');
            return row.querySelector('.traits-container');
          },
          run(editor, sender) {
            this.getTraitsEl(editor).style.display = '';
          },
          stop(editor, sender) {
            this.getTraitsEl(editor).style.display = 'none';
          },
        });
        //Add action buttons to the top panel
        editor.Panels.addPanel({
          id: 'panel-top',
          el: '.editor-top',
        });

        editor.Panels.addPanel({
          id: 'basic-actions',
          el: '.editor-actions',
          buttons: [
            {
              id: 'visibility', //visibility configurations
              active: true, // active by default
              className: 'icon-editor',
              label: '<u>B</u>',
              command: 'sw-visibility', // Built-in command
            }, {
              id: 'export', //export configurations and show code
              className: 'icon-code',
              label: 'Code',
              command: 'export-template',
              context: 'export-template', // For grouping context of buttons from the same panel
            }, {
              id: 'show-json', //show json
              className: 'icon-json',
              label: 'JSON',
              context: 'show-json',
              command(editor) {
                editor.Modal.setTitle('Components JSON')
                  .setContent(`<textarea style="width:100%; height: 250px;">
                    ${JSON.stringify(editor.getComponents())}
                  </textarea>`)
                  .open();
              },
            }, {
              id: 'show-js', //show js
              className: 'icon-js',
              label: 'JS',
              context: 'show-js',
              command(editor) {
                editor.Modal.setTitle('JS')
                  .setContent(`<textarea style="width:100%; height: 250px;">
                    ${editor.getJs()}
                  </textarea>`)
                  .open();
              },
            },
            {
              id: 'undo', //undo configurations
              className: 'icon-undo',
              label: 'Undo',
              command: 'core:undo',
            },
            {
              id: 'redo', //redo configurations
              className: 'icon-redo',
              label: 'Redo',
              command: 'core:redo',
            },
            {
              id: 'import', //import configurations
              className: 'icon-import',
              label: 'Import',
              command: 'gjs-open-import-webpage',
            },
            {
              id: 'preview', //preview configurations
              className: 'icon-preview',
              label: 'Preview',
              command: (editor) => { //preview command
              const html = editor.getHtml();
              const css = editor.getCss();
              const previewWindow = window.open('', '_blank');
              //open a new window and write the html and css to it
                previewWindow.document.write(`
                  <!DOCTYPE html>
                  <html>
                    <head>
                      <style>${css}</style>
                    </head>
                    <body>${html}</body>
                  </html>
                `);
                previewWindow.document.close();
              },
            },
            {
              id: 'clear-canvas', //clear canvas configurations
              className: 'icon-clear',
              label: 'Clear Canvas',
              command: 'canvas-clear',
            },
          ],
        });

       // Update canvas-clear command
      editor.Commands.add('canvas-clear', function() {
        if(confirm('Are you sure to clean the canvas?')) {
          editor.runCommand('core:canvas-clear')
        }
      });


      // import code command
        editor.Commands.add('gjs-open-import-webpage', {
          run(editor) {
            const modal = editor.Modal;
            const codeViewer = editor.CodeManager.getViewer('CodeMirror').clone(); //change the code viewer
            let viewerEditor = codeViewer.editor;
            //Format html and css
            function formatHtml(html) {
              return beautifyHtml(html, { indent_size: 2, inline: [] });
            }

            function formatCss(css) {
              return beautifyCss(css, { indent_size: 2 });
            }

            // Create the import button
            const btnImp = document.createElement('button');
            btnImp.type = 'button';
            btnImp.innerHTML = 'Import';
            btnImp.className = 'gjs-btn-prim';
            btnImp.style.marginTop = '1em';
            btnImp.onclick = () => {
              const importedHtml = viewerEditor.getValue().trim();
              editor.setComponents(importedHtml);
              modal.close();
            };

            // Initialize the code viewer
            codeViewer.set({
              codeName: 'htmlmixed',
              theme: 'hopscotch',
              readOnly: 0,
            });

            // Create the modal content
            const container = document.createElement('div');
            container.innerHTML = 'Any progress will be lost after importing.<br /><br />';
            const textarea = document.createElement('textarea');
            container.appendChild(textarea);
            container.appendChild(btnImp);

            // Configure the modal
            modal.setTitle('Import HTML');
            modal.setContent(container);

            // Initialize the code viewer and open the modal
            codeViewer.init(textarea);
            viewerEditor = codeViewer.editor;
            const currentHtml = editor.getHtml();
            const currentCss = editor.getCss();
            const preFilledHtml = `${formatHtml(currentHtml)}\n<style>\n${formatCss(currentCss)}\n</style>`;
            viewerEditor.setValue(preFilledHtml);
            modal.open().onceClose(() => editor.stopCommand('gjs-open-import-webpage'));
            viewerEditor.refresh();
          },
        });

        //load code into the editor from the database
        editor.Storage.add('remote', {
          async load() {
            console.log(id)
            const response = await axios.get(`/pages/${id}/`);
            return response.data.content;
          },
          //store code into the database
          async store(data) {
            const html = data.pagesHtml['0'].html
            const css = data.pagesHtml['0'].css
            return await axios.put(`/pages/${id}/`, { content: data, html: html, css: css});
          },
        });
        //open model when the user clicks on the load button
        document.getElementById('replace-code-btn').addEventListener('click', () => {
          this.openTemplateModal(editor);
        });

        
        
    }



}

</script>

<style scoped>


.panel__devices {
  position: initial;
}

.templates{
  text-align: center;
  color: #ffffff;
  font-weight:bold ;
  margin: 1em;
}

#replace-code-btn{
    padding: 1em 2em;
    border-radius: 4px;
    background-color: #1FC93A;
    color: white;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    font-size: 13px;
    border: 1px solid #000000;
    
}

.page-name{
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

.header {
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.name-change {
  position: absolute;
  align-items: center;
  top: 0;
  right: 0;

}

.name-change input {
  margin-right: 10px;
}

.enter-name{
    box-sizing: border-box;
    width: 15em;
    height: 2em;
    margin: 0.5em;
    border-radius: 4px;
    border: 1px solid #000000;
    background-color: #ffffff;
    margin: 0;
    padding: 1em;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
}

.btn-change{
    width: 8em;
    height: 3em;
    border-radius: 4px;
    background-color: #1FC93A;
    color: white;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3);
    font-size: 13px;
    border: 1px solid #000000;
    
}


#blocks {
  width: auto;
  height: 100%;
  background-color: #3A4F39;
  margin-inline: 2em;
  text-align: center;
}

#settings {
  width: auto;
  height: 100%;
  background-color: #3A4F39;
  margin-inline: 2em;
  text-align: center;
}

.editor-container{
  display: flex;
  flex-direction: column;
  margin:1em;
}

.blocks-wrapper {
  display: flex;
  height: 100%;
}

.column{
  flex: 1;
}

.middle-column{
  flex: 6;
  margin-inline: 1em;
  border: #3A4F39 solid 1px;
}

#editor-canvas{
  display: flex;
  width: auto;
  height: 100%;
  flex-direction: column;

}

.editor-top {
  padding: 0;
  width: 100%;
  display: flex;
  position: initial;
  justify-content: center;
  justify-content: space-between;
}
.editor-actions {
  position: initial;
}

.panel__switcher {
  position: initial;
}




</style>





