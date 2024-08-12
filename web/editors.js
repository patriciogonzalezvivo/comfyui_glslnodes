import { app } from "../../scripts/app.js"
import { load_glslnode_css } from "./nodescss.js"
import { getJSON } from "./utils.js"

const glslnodes_root = "extensions/comfyui_glslnodes/"

export const init_editor = async () => {
    // comfyui will try to load these if we leave them as .js files.
    // but ace wants to load them its own way,
    // so we rename them to .js_ and map the features here
    const features = [
        "mode/glsl", "mode-glsl.js_",
        "theme/tomorrow_night_bright", "theme-tomorrow_night_bright.js_",
        "keyboard/vscode", "keybinding-vscode.js_",
        "ext/language_tools", "ext-language_tools.js_",
    ];
    
    for (let i = 0; i < features.length; i += 2) {
        const feature = features[i];
        const js_ = features[i + 1];
        const response = await fetch(`${glslnodes_root}ace/${js_}`);
        const text = await response.text();
        const blob = new Blob([text], { type: `application/javascript` });
        const url = URL.createObjectURL(blob);
        ace.config.setModuleUrl(`ace/${feature}`, url);
    }
}

const getLygiaCompleter = () => {
    getJSON('https://lygia.xyz/glsl.json', (err, data) => {
        if (err)
            return

        let lygiaFiles = [];
        
        for (let i = 0; i < data.length; i++) {
            const file = data[i];
            lygiaFiles.push({
                name: file,
                value: file,
                score: 300,
                meta: "lygia"
            });
        }
        
        return {
            getCompletions: (editor, session, pos, prefix, callback) => {
                if (prefix.length === 0) {
                    callback(null, []);
                    return;
                }
                // console.log(pos, session.getTokenAt(pos.row, pos.column));
                callback(null, lygiaFiles.map(function(ea) {
                    return ea;
                }))
            }
        };
    });

    return null;
}


export class GlslEditorACE {
    static i_editor = 0
    constructor(...args) {
        const [inputName, opts] = args;
        this.name = inputName;
        this.type = opts[0];
        this.options = opts[1];

        this.selectedPointIndex = null;
        this.value = this.value || this.options.default;
        this.size = [400, 300];

        // ACE editor
        this.editor = null;
        this.div_widget = null;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        if (node.editor === undefined) {
            const editor_id = `glslnode_editor_${GlslEditorACE.i_editor++}`;
            const glslnode_div = document.createElement('div');
            glslnode_div.classList.add('glslnodeEditorContainer');
        
            const div_widget = node.addDOMWidget(glslnode_div.id, "div", glslnode_div);
        
            const editor_pre = document.createElement('pre');
            editor_pre.id = editor_id;
            editor_pre.classList.add('glslnodeEditorPre');
            editor_pre.style.height = '100%';
            editor_pre.style.overflow = 'hidden';
            editor_pre.style.margin = '0';
            
            glslnode_div.appendChild(editor_pre);
            
            div_widget.glslnode_div = glslnode_div;
            div_widget.editor_pre = editor_pre;

            let langTools = ace.require("ace/ext/language_tools");
            let editor = ace.edit(editor_id);
            editor.session.setMode("ace/mode/glsl");
            editor.setTheme("ace/theme/tomorrow_night_bright");
            editor.setOptions({
                keyboardHandler: 'ace/keyboard/vscode',
                selectionStyle: "text",
                showPrintMargin: false,
                hasCssTransforms: true,
                highlightActiveLine: false,
                // enableLiveAutocompletion: true,
                // enableBasicAutocompletion: true,
            });

            // let lygiaCompleter = getLygiaCompleter();
            // if (lygiaCompleter) {
            //     console.log("lygia completer")
            //     langTools.addCompleter(lygiaCompleter);
            // }

            editor.on('change', () => {
                this.value = editor.getValue();
            })

            editor.setValue(this.value);
            editor.clearSelection();
            node.div_widget = div_widget;
            node.editor = editor;
        }
        node.editor.resize();
        node.editor.renderer.updateFull();
    }
}

app.registerExtension({
    name: "glslnodes.editor",
    init: async (app) => {
        load_glslnode_css(document);
        await init_editor();
    },
    getCustomWidgets: () => {
        return {
            GLSL_STRING:  (node, inputName, inputData, app) => {
                return {
                    widget: node.addCustomWidget(new GlslEditorACE(inputName, inputData), ),
                    minWidth: 600,
                    minHeight: 400,
                }
            }
        }
    },
})