import { app } from '../../scripts/app.js'

import { makeUUID } from './utils.js'

class Vec2PosWidget {
    constructor(...args) {
        const [inputName, opts] = args

        this.name = inputName || 'Vec2Pos'
        this.type = 'VEC2POS'
        this.selectedPointIndex = null
        this.options = opts
        this.value = this.value || [0, 0]
        this.size = [200, 200]
        this.wY = 0;
    }

    draw(ctx, node, widgetWidth, widgetY) {
        this.wY = widgetY;
        this.wWidth = widgetWidth;
        this.wHeight = node.size[1] - widgetY;
        
        ctx.clearRect(0, this.wY, this.wWidth, this.wHeight);

        // frame
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        // ctx.strokeRect(0, this.wY, this.wWidth, this.wHeight);

        ctx.beginPath();
        ctx.lineWidth = 0.25;
        let sections = 20;
        let step = this.wWidth / sections;
        for (let i = 0; i < sections; i++) {
            ctx.moveTo(i * step, this.wY);
            ctx.lineTo(i * step, node.size[1]);
        }
        step = this.wHeight / sections;
        for (let i = 0; i < sections; i++) {
            ctx.moveTo(0, this.wY + i * step);
            ctx.lineTo(this.wWidth, this.wY + i * step);
        }
        ctx.stroke();

        // horizontal line
        ctx.strokeStyle = '#555';
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.moveTo(0, this.wY + 0.5 + this.wHeight * 0.5);
        ctx.lineTo(this.wWidth, this.wY + 0.5 + this.wHeight * 0.5);
        ctx.closePath();
        ctx.stroke();

        // vertical line
        ctx.beginPath();
        ctx.moveTo(0.5 + this.wWidth * 0.5, this.wY);
        ctx.lineTo(0.5 + this.wWidth * 0.5, node.size[1]);
        ctx.closePath();
        ctx.stroke();

        let x = Math.round(((this.value[0] + 1.0) * 0.5) * this.wWidth);
        let y = Math.round((((this.value[1] + 1.0) * 0.5)) * this.wHeight) + this.wY;

        // point
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        let radius = 4;
        ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
        ctx.fill();

        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        radius = 8;
        ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
        ctx.stroke();
        ctx.closePath();

        ctx.beginPath();
        ctx.moveTo(x, this.wY);
        ctx.lineTo(x, node.size[1]);
        ctx.moveTo(0, y);
        ctx.lineTo(this.wWidth, y);
        ctx.closePath();
        ctx.stroke();
    }

    mouse(e, pos, node) {
        if (e.type === 'pointermove') {
            this.value = [  (pos[0] / this.wWidth - 0.5) * 2.0, 
                            ((pos[1] - this.wY) / this.wHeight - 0.5) * 2.0];
            // console.log("mouse", e, pos, node, this.value);
        }
    }

    computeSize(width) {
        return [width, width - this.wY]
    }

    async serializeValue(nodeId, widgetIndex) {
        // converte this.value to JSON
        return [this.value[0], -this.value[1]].toString();
     }
}

// class GlslVec2Pos extends LiteGraph.LGraphNode {

// //   // same values as the comfy note
// //   color = LGraphCanvas.node_colors.yellow.color
// //   bgcolor = LGraphCanvas.node_colors.yellow.bgcolor
// //   groupcolor = LGraphCanvas.node_colors.yellow.groupcolor

//     constructor() {
//         super()
//         this.addInput('pos', 'VEC2POS');
//         this.addCustomWidget(new Vec2PosWidget("pos"));          // adds it to the node
//         this.addOutput('pos', 'VEC2');
//         this.category = 'GLSL';
//         this.title = 'vec2 (position)';
//         this.collapsable = true;
//         this.isVirtualNode = true;
//     }
// }

app.registerExtension({
    name: "glslnodes.types",
    getCustomWidgets: () => {
        return {
            VEC2POS:  (node, inputName, inputData, app) => {
                return {
                    widget: node.addCustomWidget(new Vec2PosWidget(inputName, inputData), ),
                    minWidth: 200,
                    minHeight: 200,
                }
            },
        }
    },
    // registerCustomNodes() {
    //     LiteGraph.registerNodeType('vec2 (pos)', GlslVec2Pos)
    //     GlslVec2Pos.category = 'GLSL'
    //     GlslVec2Pos.title = 'vec2 (position)'
    // },
  })