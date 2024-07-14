import requests
import re

def resolveLygia(src: str):
    source = ""
    lines = src.split("\n")
    for line in lines:
        # resolve #include dependencies
        match = re.search(r'#include\s*["|<](.*.glsl)["|>]', line, re.IGNORECASE)
        if match:
            url = match.group(1)
            print("Adding dependecy", url)
            if url.startswith("lygia"):
                url = url.replace("lygia", "https://lygia.xyz")

                response = requests.get(url, headers={
                    "Origin": "ComfyUI Server",
                })
                if response.status_code == 200:
                    source += response.text + "\n"
                else:
                    print("Failed to fetch", url)

        else:
            source += line + "\n"

    return source


def stackDefines(defines):
    out = ""
    for define in defines:
        out += f"#define {define[0]} {define[1]}\n"
    return out

def getDefaultVertexShader(version):
    out = "#version " + version + "\n"
    if version == "100" or version == "120":
        out += """
#ifdef GL_ES
precision highp float;
#endif

attribute vec2 a_position;
varying vec2 v_texcoord;

void main() {
    v_texcoord = a_position * 0.5 + 0.5;
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
    else:
        out += """
in vec2 a_position;
out vec2 v_texcoord;

void main() {
    v_texcoord = a_position * 0.5 + 0.5;
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
    return out