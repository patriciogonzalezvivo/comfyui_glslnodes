# GLSL Nodes for ComfyUI

This nodes add support for GLSL shaders on workflows, by adding the following nodes: glslEditor, glslViewer, int, float, vec2, vec3, vec4.

Here some examples:

`examples/types.json`
![types](https://github.com/user-attachments/assets/3eabbc40-094a-4950-b46d-e2b407e2f352)

`examples/depth_of_field.json`
![depth_of_field](https://github.com/user-attachments/assets/fa52dc6d-8202-4bb3-a03d-2e4222a4b203)

`examples/edge_detection.json`
![edge_detection](https://github.com/user-attachments/assets/33d13617-8190-4ecb-aa5f-55a7ee93dd1e)

`examples/look_up_table.json`
![look_up_table](https://github.com/user-attachments/assets/83d715eb-c843-4fb9-be52-0cd5eeffeeb9)


`examples/video_flow.json`

https://github.com/user-attachments/assets/995f541e-cb11-42ff-95ea-b4e08d010778

`examples/video_mask.json`

https://github.com/user-attachments/assets/1f2a230d-b703-4889-b3b5-659855444366

`examples/video_dither.json`

https://github.com/user-attachments/assets/1d98caf2-347b-40c1-8442-2c72bb86a940

`examples/video_pixelate.json`

https://github.com/user-attachments/assets/89deee89-db13-4cfa-8a96-2e82f5ff6ca2

`examples/shadertoy.json`

https://github.com/user-attachments/assets/c6a66d8f-34cb-4ff6-b879-ee13e9e856d0

`examples/raymarch_buffers.json`

https://github.com/user-attachments/assets/0cfbad85-6a79-4458-bd38-37a0d83996d0


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
