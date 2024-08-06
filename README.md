# GLSL Nodes for ComfyUI

This nodes add support for GLSL shaders on workflows, by adding the following nodes: glslEditor, glslViewer, int, float, vec2, vec3, vec4.

Here some examples:

`examples/types.json`
![examples/types.json](https://github.com/user-attachments/assets/656038bf-1126-4b29-9148-06e33822394b)

`examples/depth_of_field.json`
![examples/depth_of_field.json](https://github.com/user-attachments/assets/5ef20d7b-ac2a-4682-a052-ae8a52c9be84)

`examples/edge_detection.json`
![examples/edge_detection.json](https://github.com/user-attachments/assets/32e31f24-d988-474f-a0bb-b8599c0babc0)

`examples/look_up_table.json`
![examples/look_up_table.json](https://github.com/user-attachments/assets/41f607fd-1602-4bde-8700-1e039f78f9ee)

`examples/video_flow.json`

https://github.com/user-attachments/assets/995f541e-cb11-42ff-95ea-b4e08d010778

`examples/video_mask.json`

https://github.com/user-attachments/assets/1f2a230d-b703-4889-b3b5-659855444366

`examples/video_dither.json`

https://github.com/user-attachments/assets/21537547-2ff4-45b1-8828-287d91a47774

`examples/shadertoy.json`

https://github.com/user-attachments/assets/3e0f9dc7-1e30-4c55-95ce-45757596a977

Features:

* It the code is compatible with [GlslViewer](https://github.com/patriciogonzalezvivo/glslViewer), [Glsl-Pipeline](https://github.com/patriciogonzalezvivo/glsl-pipeline/) and [GlslCanvas](https://marketplace.visualstudio.com/items?itemName=circledev.glsl-canvas) by following the following specs for:
  * [Uniforms](https://github.com/patriciogonzalezvivo/glslViewer/wiki/GlslViewer-UNIFORMS)
  * [Defines](https://github.com/patriciogonzalezvivo/glslViewer/wiki/GlslViewer-DEFINES)
* It contain [LYGIA Shader Library](https://lygia.xyz/) by resolving all `#include` directives from [LYGIA's Server](https://lygia.xyz/)

# Roadmap

- [x] 100, 120, 130, 140, 150, 300, 330, 330 core, 400, 410, 420, 430 and 440 GLSL shaders
- [x] Resolves dependencies to [LYGIA Shader Library](https://lygia.xyz/)
- [x] Code editor (ACE) on GlslEditorPro nodes
- [x] produce multiple frames
- [x] reads multiple textures and texturesArrays
- [x] multiple float, vec2, vec3, vec4 uniforms
- [x] Dynamic inputs for uniforms
- [x] Uniforms node for efficiency by caching textures and texturesArrays together with the GL context
- [x] basic GLSL type nodes: `int`, `float`, `vec2`, `vec3` and `vec4`
- [x] 2D position node widget
- [x] 3D position node widget
- [x] Color Picker node widget
- [x] multiple buffers (`#ifdef BUFFER_X`)
- [x] multiple double uniforms (`#ifdef DOUBLEBUFFER_X`)
- [ ] multiple pyramids (`#ifdef PYRAMID_X`)
- [x] OPTICAL_FLOW textures
- [x] MASK textures (create SDF on other channels)
- [ ] loading 3D geometry
- [ ] Vertex Shaders
- [ ] CubeMaps (Auto detect equirectangular, cross, etc)
- [ ] BACKGROUND pass (`#ifdef BACKGROUND`)
- [ ] POSTPROCESSING pass (`#ifdef POSTPROCESSING`)
- [ ] SCENE pass (`#ifdef SCENE`) that exposes `u_scene` and `u_sceneDepth`
