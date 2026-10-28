#version 140
// Original illustrated animation on a camera-facing NATIVE world quad.
// Alpha cutout writes depth; no GUI actor/projectile can bypass a wall.
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform mediump sampler2D tex0;
uniform fs_uniforms { mediump vec4 tint; mediump vec4 frame; };
void main(){
 vec2 uv=vec2(var_texcoord0.x,1.0-var_texcoord0.y);
 if(tint.w<0.0)uv.x=1.0-uv.x;
 uv=vec2((uv.x+frame.x)/frame.z,(uv.y+frame.w-1.0-frame.y)/frame.w);
 vec4 color=texture(tex0,uv);
 if(color.a<.16)discard;
 out_fragColor=vec4(color.rgb*tint.rgb*color.a,color.a);
}
