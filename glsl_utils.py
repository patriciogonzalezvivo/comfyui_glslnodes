import requests
import re
import numpy as np

GL_BACKENDS = {
    "Linux": "egl",
}

GL_PLATFORMS = {
    "Linux": "PLATFORM_LINUX",
    "Darwin": "PLATFORM_OSX",
    "Windows": "PLATFORM_WIN",
}

GLSL_VERSIONS = ["100", "120", "130", "140", "150", "330", "330 core", "400", "410", "420", "430", "440"]

GLSL_FRAGMENT_HEADER = """
#if __VERSION__ >= 130
out vec4 fragColor;
#define gl_FragColor fragColor
#define texture2D(TEX, UV) texture(TEX, UV)
#else
#extension GL_EXT_texture_array : enable
#endif
#ifdef GL_ES
precision mediump float;
#endif
#line 1
"""

DEFAULT_FRAGMENT_SHADER= """
// <NAME>_TYPE: have the uniform type
//uniform U_TEX0_TYPE u_tex0;
//uniform U_TEX0_TYPE u_val0;

uniform vec4    u_date;
uniform vec2    u_resolution;
uniform float   u_delta;
uniform float   u_time;
uniform float   u_fps;
uniform int     u_frame;

void main() {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 pixel = 1.0 / u_resolution;
    vec2 st = gl_FragCoord.xy * pixel;

    color.rgb = vec3(st, 0.5 + 0.5 * cos(u_time));

    // texture arrays have this <NAME>_TOTALFRAMES
    //#ifdef U_TEX0_TOTALFRAMES
    //color = texture(u_tex0, vec3(st, float(u_frame)));
    //#else
    //color = texture(u_tex0, st);
    //#endif

    gl_FragColor = color;
}
"""

GLSL_SHADERTOY_HEADER = """
out vec4 fragColor;

#ifdef U_TEX0_TYPE
uniform U_TEX0_TYPE u_tex0;
#define iChannel0 u_tex0
#endif

#ifdef U_TEX1_TYPE
uniform U_TEX1_TYPE u_tex1;
#define iChannel1 u_tex1
#endif

#ifdef U_TEX2_TYPE
uniform U_TEX2_TYPE u_tex1;
#define iChannel2 u_tex2
#endif

#ifdef U_TEX3_TYPE
uniform U_TEX3_TYPE u_tex1;
#define iChannel3 u_tex3
#endif

uniform vec4    u_date;
#define iDate   u_date

uniform vec2    u_resolution;
#define iResolution u_resolution

#define iMouse  vec2(0.0)

uniform float   u_time;
#define iTime   u_time

uniform float   u_delta;
#define iTimeDelta u_delta

uniform float   u_fps;

uniform int     u_frame;
#define iFrame  u_frame

void mainImage( out vec4 fragColor, in vec2 fragCoord );

void main() {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 st = gl_FragCoord.xy;
    mainImage(color, st);
    fragColor = color;
}
"""

DEFAULT_SHADERTOY_SHADER = """void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    // Time varying pixel color
    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));

    // Output to screen
    fragColor = vec4(col,1.0);
}
"""

def getIp():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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
                    "Origin": getIp() + ":8188",
                })
                if response.status_code == 200:
                    source += response.text + "\n"
                else:
                    print("Failed to fetch", url)

        else:
            source += line + "\n"

    return source





def getDefaultVertexShader(version):
    out = "#version " + version + "\n"
    if version == "100" or version == "120":
        out += """
#ifdef GL_ES
precision highp float;
#endif

attribute vec2 a_position;
varying vec2 v_texcoord;
"""
    else:
        out += """
in vec2 a_position;
out vec2 v_texcoord;
"""

    out += """
void main() {
    v_texcoord = a_position * 0.5 + 0.5;
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
    return out


def getFragmentShader(fragment_code, defines):
    out = "#version " + fragment_code["version"] + "\n" 

    # Stack defines
    for define in defines:
        out += f"#define {define[0]} {define[1]}\n"

    if fragment_code["specs"] == "shadertoy":
        print("Using Shadertoy Header")
        out += GLSL_SHADERTOY_HEADER
    else:
        out += GLSL_FRAGMENT_HEADER 

    out += "\n#line 1\n" 
    out += fragment_code["src"]
    return out


def getSizeFromCode(width:int, height:int, code: str, name:str):
    size_found = re.findall(r"uniform\\s*sampler2D\\s*"+name+"\\;\\s*\\/\\/*\\s(\\d+)x(\\d+)", code)
    if size_found:
        return (int(size_found[0]), int(size_found[1]))
    
    scale_found = re.findall(r"uniform\\s*sampler2D\\s*"+name+"\\;\\s*\\/\\/*\\s(\\d+)x(\\d+)", code)
    if scale_found:
        return ( int(width * scale_found[0]), int(height * scale_found[1]))
    
    return (width, height)


def hue_to_rgb(hue):
    """Convert hue to RGB."""
    if isinstance(hue, np.ndarray):
        rgb = np.zeros((hue.shape[0], hue.shape[1], 3))
        rgb[..., 0] = hue * 6.0
        rgb[..., 1] = hue * 6.0 + 4.0
        rgb[..., 2] = hue * 6.0 + 2.0
    else:
        rgb = np.zeros(3)
        rgb[0] = hue * 6.0
        rgb[1] = hue * 6.0 + 4.0
        rgb[2] = hue * 6.0 + 2.0

    rgb = np.abs(np.mod(rgb, 6.0) - 3.0) - 1.0
    rgb = np.clip(rgb, 0.0, 1.0)
    return rgb


def encode_polar(a: np.ndarray, rad):
    """Encode polar cordinates to Hue (angle) and Saturate (radius)."""
    rgb = hue_to_rgb(a)
    rgb = saturate(rgb, rad)
    return rgb


def saturate(rgb, sat):
    """Set saturate."""
    rgb[..., 0] = rgb[..., 0] * sat + (1.0-sat)
    rgb[..., 1] = rgb[..., 1] * sat + (1.0-sat)
    rgb[..., 2] = rgb[..., 2] * sat + (1.0-sat)
    return rgb


def process_flow(flow):
    """Process flow."""

    h, w, _ = flow.shape
    distances = np.sqrt(np.square(flow[..., 0]) + np.square(flow[..., 1]))

    max_distance = distances.max()
    dX = flow[..., 0] / float(max_distance)
    dY = flow[..., 1] / float(max_distance)
    rad = np.sqrt(np.square(dX) + np.square(dY))
    a = (np.arctan2(dY, dX) / np.pi + 1.0) * 0.5
    rgb = encode_polar(a, rad)

    return (rgb * 255).astype(np.uint8), max_distance


