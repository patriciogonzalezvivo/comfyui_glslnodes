# GLSL Nodes for ComfyUI

https://github.com/user-attachments/assets/8d4504f4-6631-4aa1-8844-8367b98f76fb

This nodes add support for GLSL shaders on workflows.

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
- [ ] Add support for multiple buffers (`#ifdef BUFFER_X`)
- [ ] Add support for multiple double uniforms (`#ifdef DOUBLEBUFFER_X`)
- [ ] Add support for multiple pyramids (`#ifdef PYRAMID_X`)
- [ ] Add support for Vertex Shaders and 3D Models
- [ ] Add support for CubeMaps (Auto detect equirectangular, cross, etc)
- [ ] Add support for BACKGROUND pass (`#ifdef BACKGROUND`)
- [ ] Add support for POSTPROCESSING pass (`#ifdef POSTPROCESSING`)
- [ ] Add support for SCENE pass (`#ifdef SCENE`) that exposes `u_scene` and `u_sceneDepth`
