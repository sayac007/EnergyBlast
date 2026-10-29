#version 140
// Original depth-tested character sheets, with a restrained animated energy rim.
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform mediump sampler2D tex0;
uniform fs_uniforms { mediump vec4 tint; mediump vec4 frame; mediump vec4 edge; mediump vec4 hero_fx; mediump vec4 atlas_texel; };
void main(){
 vec2 local_uv=vec2(var_texcoord0.x,1.0-var_texcoord0.y);
 if(tint.w<0.0)local_uv.x=1.0-local_uv.x;
 vec2 cell=vec2(frame.x,frame.w-1.0-frame.y),grid=vec2(frame.z,frame.w);
 vec2 uv=(local_uv+cell)/grid;
 vec2 texel=atlas_texel.xy;
 vec2 lo=cell/grid+texel*.5,hi=(cell+1.0)/grid-texel*.5;
 vec4 color=texture(tex0,clamp(uv,lo,hi));
 vec2 dx=dFdx(uv),dy=dFdy(uv);
 float nearby=0.0;
 if(edge.x>0.0)nearby=max(max(texture(tex0,clamp(uv+dx*edge.x,lo,hi)).a,texture(tex0,clamp(uv-dx*edge.x,lo,hi)).a),max(texture(tex0,clamp(uv+dy*edge.x,lo,hi)).a,texture(tex0,clamp(uv-dy*edge.x,lo,hi)).a));
 bool shimmer=hero_fx.w>.5;
 float t=hero_fx.x,kind=hero_fx.w;
 vec3 hue=kind>3.5?vec3(1.0,.73,.16):kind>2.5?vec3(.64,.45,1.0):kind>1.5?vec3(1.0,.54,.13):vec3(.16,.83,1.0);
 hue=mix(hue,vec3(.65,1.0,.92),.18+.16*sin(t*1.9+local_uv.y*5.0+kind));
 float pulse=.73+.27*sin(t*3.1+kind);
 if(color.a<.16){
  if(shimmer){
   float glow=max(max(texture(tex0,clamp(uv+dx*3.2,lo,hi)).a,texture(tex0,clamp(uv-dx*3.2,lo,hi)).a),max(texture(tex0,clamp(uv+dy*3.2,lo,hi)).a,texture(tex0,clamp(uv-dy*3.2,lo,hi)).a));
   if(glow>.4){float a=(nearby>.5?.72:.23)*pulse;out_fragColor=vec4(hue*a,a);return;}
  }
  if(edge.x>0.0&&nearby>.5){out_fragColor=vec4(.012,.024,.045,.88);return;}
  discard;
 }
 vec3 rgb=color.rgb*tint.rgb;
 if(shimmer){
  float low=min(min(texture(tex0,clamp(uv+dx*1.5,lo,hi)).a,texture(tex0,clamp(uv-dx*1.5,lo,hi)).a),min(texture(tex0,clamp(uv+dy*1.5,lo,hi)).a,texture(tex0,clamp(uv-dy*1.5,lo,hi)).a));
  float sweep=pow(max(0.0,.5+.5*sin(local_uv.y*8.0+local_uv.x*2.0-t*1.5)),18.0);
  rgb+=hue*((1.0-low)*.38*pulse+sweep*.09+hero_fx.z*.10);
 }
 out_fragColor=vec4(rgb*color.a,color.a);
}
