#version 140
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform fs_uniforms { mediump vec4 frame; };
void main(){
 vec2 q=abs(var_texcoord0-.5)*2.0;
 vec2 d=max(vec2(0.0),q-frame.xy);
 float a=exp(-16.0*dot(d,d))*frame.z*(1.0-smoothstep(.88,1.0,max(q.x,q.y)));
 out_fragColor=vec4(vec3(.012,.019,.042)*a,a);
}
