import { app } from "../../scripts/app.js";
import { removeAllUniforms, addInput, getMaxIndex } from "./utils.js";

const ViewerId = "glslViewer";
const UniformsId = "glslUniforms";

app.registerExtension({
    name: "glslnodes.DynamicUniforms",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== ViewerId && nodeData.name !== UniformsId) {
            return;
        }

        // Override onNodeCreated to add the input
        const onNodeCreated = nodeType.prototype.onNodeCreated
        nodeType.prototype.onNodeCreated = function () {
            this.options = {}
            const r = onNodeCreated
            ? onNodeCreated.apply(this, arguments)
            : undefined
            
            // Remove all inputs to make it dynamic
            removeAllUniforms(this);

            // Add the first input
            this.addInput("...", "*");
            return r
        }

        const onConnectionsChange = nodeType.prototype.onConnectionsChange
        nodeType.prototype.onConnectionsChange = function (...args) {
            const [_type, index, connected, link_info, ioSlot] = args
            const r = onConnectionsChange
                ? onConnectionsChange.apply(this, args)
                : undefined

            if (link_info === undefined) {
                return r
            }
            
            // If it's connecting
            if (connected) {
                // to the last input "..."
                 if (ioSlot.name === "...") {

                    // Change the type and name based on the connection Type
                    const fromNode = app.graph.getNodeById(link_info.origin_id)
                    const fromNodeOutput = fromNode.outputs[link_info.origin_slot];
                    const fromNodeOutputType = fromNodeOutput.type;

                    console.log("CONNECTING", fromNodeOutputType)

                    if (fromNodeOutputType === "GLSL_CONTEXT") {
                        let isUniformsAlreadyConnected = false;
                        for (let i = 0; i < this.inputs.length; i++)
                            if (this.inputs[i].name === "uniforms")
                                isUniformsAlreadyConnected = true;

                        if (!isUniformsAlreadyConnected) 
                            addInput(this, index, "uniforms", fromNodeOutputType, false);
                    }
                    else if (   fromNodeOutputType === "IMAGE" ||
                                fromNodeOutputType === "MASK" ||
                                fromNodeOutputType === "OPTICAL_FLOW")
                        addInput(this, index, "u_tex", fromNodeOutputType);
        
                    else if (   fromNodeOutputType === "INT" || 
                                fromNodeOutputType === "FLOAT" || 
                                fromNodeOutputType === "VEC2" ||
                                fromNodeOutputType === "VEC3" ||
                                fromNodeOutputType === "VEC4" )
                        addInput(this, index, "u_val", fromNodeOutputType);
    
                }
            }
            // If it's disconnecting
            else {
                if (ioSlot.name.startsWith("uniforms")) {
                    this.removeInput(index);
                }
                else if (ioSlot.name.startsWith("u_tex")) {
                    let maxTexIndex = getMaxIndex(this, "u_tex");
                    let maxTexName = "u_tex" + maxTexIndex;
                    if (ioSlot.name === maxTexName) {
                        this.removeInput(index);
                    }
                }
                else if (ioSlot.name.startsWith("u_val")) {
                    let maxValIndex = getMaxIndex(this, "u_val");
                    let maxValName = "u_val" + maxValIndex;
                    if (ioSlot.name === maxValName) {
                        this.removeInput(index);
                    }
                }
            }
        }
    }
})
