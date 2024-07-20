// import { app } from '../../scripts/app.js'

// import { makeUUID } from './utils.js'

// class GlslVec2Pos extends LiteGraph.LGraphNode {

//   // same values as the comfy note
//   color = LGraphCanvas.node_colors.yellow.color
//   bgcolor = LGraphCanvas.node_colors.yellow.bgcolor
//   groupcolor = LGraphCanvas.node_colors.yellow.groupcolor

//   constructor() {
//     super()
//     this.uuid = makeUUID()
//     this.collapsable = true
//     this.isVirtualNode = true
//     this.shape = LiteGraph.BOX_SHAPE
//     this.serialize_widgets = true

//     // - state
//     this.live = true
//     this.calculated_height = 0
//   }

//   onDrawForeground(ctx, _graphcanvas) {
//     if (this.flags.collapsed) return
//   }
// }

// app.registerExtension({
//     name: "glslnodes.types",
//     registerCustomNodes() {
//         LiteGraph.registerNodeType('vec2 (pos)', GlslVec2Pos)
//         GlslEditorIDE.category = 'GLSL'
//         GlslEditorIDE.title = 'vec2 (position)'
//     },
//   })