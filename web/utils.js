import { app } from '../../scripts/app.js'

export function makeUUID() {
    let dt = new Date().getTime()
    const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (dt + Math.random() * 16) % 16 | 0
        dt = Math.floor(dt / 16)
        return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
    })
    return uuid
}
export const removeLastUniform = (node) => {
    let last_index = node.inputs.length - 1;
    let last_input = node.inputs[last_index];
    if (last_input.name.startsWith("u_") || last_input.name === "...") {
        node.removeInput(last_index);
    }
}

export const removeAllUniforms = (node) => {
    let totalInputs = node.inputs.length - 1;
    for (let i = totalInputs; i >= 0; i--) {
        if (node.inputs[i].name.startsWith("u_") || 
            node.inputs[i].name === "uniforms" ||
            node.inputs[i].name === "vertex_code" ||
            node.inputs[i].name === "3D model"
        ) {
            node.removeInput(i);
        }
    }
}

export const getMaxIndex = (node, str) => {
    let maxIndex = -1;
    for (let i = 0; i < node.inputs.length; i++) {
        if (node.inputs[i].name.startsWith(str)) {
            maxIndex = Math.max(maxIndex, parseInt(node.inputs[i].name.replace(str, "")));
        }
    }
    return maxIndex;
}

export const getNextName = (node, str) => { return str + (getMaxIndex(node, str) + 1); }

export const addInput = (node, index, str, type, unique=true) => {
    let name = str;

    if (unique) 
        name = getNextName(node, str);
    
    node.graph.beforeChange();
    
    node.inputs[index].name = name;
    node.inputs[index].type = type;
    
    node.addInput("...", "*");
    node.graph.afterChange();
}