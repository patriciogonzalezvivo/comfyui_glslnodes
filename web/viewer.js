import { app } from "../../../scripts/app.js";
import { removeAllUniforms, addInput } from "./utils.js";

const ViewerId = "glslViewer";

app.registerExtension({
    name: "glslnodes." + ViewerId,
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== ViewerId) {
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
                 if (ioSlot.name === "..."){

                    // Change the type and name based on the connection Type
                    const fromNode = app.graph.getNodeById(link_info.origin_id)
                    const fromNodeOutput = fromNode.outputs[link_info.origin_slot];
                    const fromNodeOutputType = fromNodeOutput.type;
                    
                    if (fromNodeOutputType === "IMAGE") {
                        addInput(this, "u_tex", fromNodeOutputType);
                    }
                    else if (   fromNodeOutputType === "INT" || 
                                fromNodeOutputType === "FLOAT" || 
                                fromNodeOutputType === "VEC2" ||
                                fromNodeOutputType === "VEC3" ||
                                fromNodeOutputType === "VEC4" ) {
                        addInput(this, "u_val", fromNodeOutputType);
                    }
                }
            }
            // If it's disconnecting
            else {
                let totalInputs = this.inputs.length - 1;
                console.log('totalInputs', totalInputs);
                // If the last before "..."
                if (index == totalInputs - 1) {
                    this.removeInput(index);
                }
            }
        }
    }
})
