# GLSL Nodes for ComfyUI

This nodes add support for GLSL shaders on workflows, by adding the following nodes: glslEditor, glslViewer, int, float, vec2, vec3, vec4.

Here some examples:

![examples/depth_of_field.json](https://github.com/user-attachments/assets/5ef20d7b-ac2a-4682-a052-ae8a52c9be84)
![examples/edge_detection.json](https://github.com/user-attachments/assets/32e31f24-d988-474f-a0bb-b8599c0babc0)
![examples/look_up_table.json](https://github.com/user-attachments/assets/41f607fd-1602-4bde-8700-1e039f78f9ee)

https://github.com/user-attachments/assets/21537547-2ff4-45b1-8828-287d91a47774

https://github.com/user-attachments/assets/3e0f9dc7-1e30-4c55-95ce-45757596a977

Features:

* It the code is compatible with [GlslViewer](https://github.com/patriciogonzalezvivo/glslViewer), [Glsl-Pipeline](https://github.com/patriciogonzalezvivo/glsl-pipeline/) and [GlslCanvas](https://marketplace.visualstudio.com/items?itemName=circledev.glsl-canvas) by following the following specs for:
  * [Uniforms](https://github.com/patriciogonzalezvivo/glslViewer/wiki/GlslViewer-UNIFORMS)
  * [Defines](https://github.com/patriciogonzalezvivo/glslViewer/wiki/GlslViewer-DEFINES)
* It contain support for [LYGIA Shader Library](https://lygia.xyz/) by resolving all `#include` directives from [LYGIA's Server](https://lygia.xyz/)

# Roadmap

- [x] Add support for GLSL shaders
- [x] Add support for [LYGIA Shader Library](https://lygia.xyz/)
- [ ] Add JS editor on the node client UI
- [x] Add support for multiple frames
- [x] Add support for multiple textures
- [x] Add support for multiple float uniforms
- [x] Add dynamic inputs for uniforms
- [x] Add Uniforms node for efficiency by caching textures and texturesArrays together with the GL context
- [x] Add basic GLSL type nodes: `int`, `float`, `vec2`, `vec3` and `vec4`
- [x] Add 2D position node
- [ ] Add 3D position node
- [ ] Add Color Picker
- [x] Add support for multiple buffers (`#ifdef BUFFER_X`)
- [x] Add support for multiple double uniforms (`#ifdef DOUBLEBUFFER_X`)
- [ ] Add support for multiple pyramids (`#ifdef PYRAMID_X`)
- [ ] Add support for loading 3D geometry
- [ ] Add support for Vertex Shaders
- [ ] Add support for CubeMaps (Auto detect equirectangular, cross, etc)
- [ ] Add support for BACKGROUND pass (`#ifdef BACKGROUND`)
- [ ] Add support for POSTPROCESSING pass (`#ifdef POSTPROCESSING`)
- [ ] Add support for SCENE pass (`#ifdef SCENE`) that exposes `u_scene` and `u_sceneDepth`
