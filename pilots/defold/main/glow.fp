#version 140
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform fs_uniforms {mediump vec4 tint;};
void main(){
 vec2 q=(var_texcoord0-.5)*2.0;
 float glow=exp(-4.8*dot(q,q))*(1.0-smoothstep(.70,1.0,length(q)));
 out_fragColor=vec4(tint.rgb*glow*tint.a,glow*tint.a);
}
