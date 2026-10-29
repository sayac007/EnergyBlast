#version 140
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
void main(){
 vec2 q=(var_texcoord0-.5)*2.0;
 float a=exp(-3.8*dot(q,q))*.48*(1.0-smoothstep(.78,1.0,max(abs(q.x),abs(q.y))));
 out_fragColor=vec4(vec3(.018,.035,.050)*a,a);
}
