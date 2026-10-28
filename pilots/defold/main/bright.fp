#version 140
// Original EnergyBlast lighting: lifted shadows, broad highlights and a soft rim.
in highp vec4 var_position;
in mediump vec3 var_normal;
in mediump vec2 var_texcoord0;
in mediump vec4 var_light;
out vec4 out_fragColor;
uniform mediump sampler2D tex0;
uniform fs_uniforms { mediump vec4 tint; };
void main() {
    vec3 n=normalize(var_normal);
    float diffuse=max(dot(n,normalize(var_light.xyz-var_position.xyz)),0.0);
    float light=diffuse>.60 ? 1.04 : (diffuse>.23 ? .88 : .67);
    float rim=pow(1.0-max(dot(n,normalize(-var_position.xyz)),0.0),3.0)*0.13;
    vec3 base=texture(tex0,var_texcoord0).rgb*tint.rgb;
    out_fragColor=vec4(base*light+vec3(0.15,0.65,0.7)*rim,1.0);
}
