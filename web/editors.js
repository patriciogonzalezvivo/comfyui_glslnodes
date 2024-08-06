import { app } from "../../../scripts/app.js"
import { load_glslnode_css } from "./nodescss.js"

const glslnodes_root = "/extensions/comfyui_glslnodes/"

export const init_editor = async () => {
    // comfyui will try to load these if we leave them as .js files.
    // but ace wants to load them its own way,
    // so we rename them to .js_ and map the features here
    const features = [
        "mode/glsl", "mode-glsl.js_",
    ]

    const ace_keyboards = [
        "vim", "emacs", "sublime", "vscode"
    ]

    const ace_themes = [
        "tomorrow_night", "tomorrow_night_bright", "twilight"
    ]
  
    ace_keyboards.forEach((keyboard) => {
        if (keyboard !== 'ace') {
            features.push(`keyboard/${keyboard}`)
            features.push(`keybinding-${keyboard}.js_`)
        }
    })
  
    ace_themes.forEach((theme) => {
        features.push(`theme/${theme}`)
        features.push(`theme-${theme}.js_`)
    })
    
    for (let i = 0; i < features.length; i += 2) {
        const feature = features[i]
        const js_ = features[i + 1]
        const response = await fetch(`${glslnodes_root}ace/${js_}`)
        const text = await response.text()
        const blob = new Blob([text], { type: `application/javascript` })
        const url = URL.createObjectURL(blob)
        ace.config.setModuleUrl(`ace/${feature}`, url)
        console.log(`ace.config.setModuleUrl("ace/${feature}", ${url})`)
    }
}

export class GlslEditorIDE {
    static i_editor = 0
    constructor(...args) {
        const [inputName, opts] = args
        console.log('GlslEditorIDE', opts)
        this.name = inputName
        this.type = opts[0]
        this.options = opts[1]

        this.selectedPointIndex = null
        this.value = this.value || this.options.default
        this.size = [400, 300]

        // 
        this.editor = null
        this.div_widget = null
    }

    draw(ctx, node, widgetWidth, widgetY) {
        if (node.editor === undefined) {
            const editor_id = `glslnode_editor_${GlslEditorIDE.i_editor++}`    
            const glslnode_div = document.createElement('div')
            glslnode_div.classList.add('glslnodeEditorContainer')
        
            const div_widget = node.addDOMWidget(glslnode_div.id, "div", glslnode_div)
        
            const editor_pre = document.createElement('pre')
            // editor_pre.classList.add('glslnode-editor')
            editor_pre.id = editor_id
            editor_pre.classList.add('glslnodeEditorPre')

            // force position to initial
            // editor_pre.style.position = 'initial'
            editor_pre.style.height = '100%'
            editor_pre.style.overflow = 'hidden'
            editor_pre.style.margin = '0'
            
            glslnode_div.appendChild(editor_pre)
            
            div_widget.glslnode_div = glslnode_div
            div_widget.editor_pre = editor_pre
            
            const editor = ace.edit(editor_id, {
                keyboardHandler: 'ace/keyboard/vscode',
                theme: "ace/theme/tomorrow_night_bright",
                mode: "ace/mode/glsl",
                selectionStyle: "text",
                showPrintMargin: false,
            })

            editor.on('change', () => {
                this.value = editor.getValue();
            })

            editor.setValue(this.value);
            editor.clearSelection();
            node.div_widget = div_widget
            node.editor = editor   
        }
        node.editor.resize();
        node.editor.renderer.updateFull();
    }
}

app.registerExtension({
    name: "glslnodes.editor",
    init: async (app) => {
        load_glslnode_css(document)
        await init_editor()
    },
    getCustomWidgets: () => {
        return {
            GLSL_STRING:  (node, inputName, inputData, app) => {
                return {
                    widget: node.addCustomWidget(new GlslEditorIDE(inputName, inputData), ),
                    minWidth: 600,
                    minHeight: 400,
                }
            }
        }
    },
})