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
  for (let i = 0; i < totalInputs; i++){
      removeLastUniform(node);
  }
}

export const getMaxIndex = (node, str) => {
  let maxIndex = -1;
  for (let i = 0; i < node.inputs.length; i++) {
      if (node.inputs[i].name.startsWith(str)) {
          if (node.inputs[i].link) {
              maxIndex = Math.max(maxIndex, parseInt(node.inputs[i].name.replace(str, "")));
          }
      }
  }
  return maxIndex;
}

export const getNextName = (node, str) => { return str + (getMaxIndex(node, str) + 1); }

export const addInput = (node, str, type) => {
  let name = getNextName(node, str);

  node.graph.beforeChange();
  
  node.inputs[node.inputs.length - 1].name = name;
  node.inputs[node.inputs.length - 1].type = type;
  
  node.addInput("...", "*");
  node.graph.afterChange();
}