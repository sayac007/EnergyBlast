#version 140
// Original illustrated animation on a camera-facing NATIVE world quad.
// Alpha cutout writes depth; no GUI actor/projectile can bypass a wall.
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform mediump sampler2D tex0;
uniform fs_uniforms { mediump vec4 tint; mediump vec4 frame; mediump vec4 edge; };
void main(){
 vec2 uv=vec2(var_texcoord0.x,1.0-var_texcoord0.y);
 if(tint.w<0.0)uv.x=1.0-uv.x;
 uv=vec2((uv.x+frame.x)/frame.z,(uv.y+frame.w-1.0-frame.y)/frame.w);
 vec4 color=texture(tex0,uv);
 vec2 dx=dFdx(uv)*edge.x,dy=dFdy(uv)*edge.x;
 float nearby=0.0;
 if(edge.x>0.0)nearby=max(max(texture(tex0,uv+dx).a,texture(tex0,uv-dx).a),max(texture(tex0,uv+dy).a,texture(tex0,uv-dy).a));
 if(color.a<.16){
  // A thin screen-space silhouette edge keeps ivory heroes readable on light floors.
  if(edge.x>.0 && nearby>.5){out_fragColor=vec4(.012,.024,.045,.88);return;}
  discard;
 }
 out_fragColor=vec4(color.rgb*tint.rgb*color.a,color.a);
}
