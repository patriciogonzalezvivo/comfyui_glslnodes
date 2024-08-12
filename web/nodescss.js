const glslnode_css = `extensions/comfyui_glslnodes/node.css`

const load_css = (doc, url) => {
    const link = doc.createElement("link")
    link.rel = 'stylesheet'
    link.type = 'text/css'
    link.href = url
    doc.head.appendChild(link)
}

export const load_glslnode_css = (doc) => {
    load_css(doc, glslnode_css)
}

export const glslnode_css_link = `<link rel="stylesheet" type="text/css" href="${glslnode_css}" />`