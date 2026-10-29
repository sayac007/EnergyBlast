#version 140
in mediump vec2 var_texcoord0;
out vec4 out_fragColor;
uniform fs_uniforms { mediump vec4 tint; mediump vec4 frame; };
void main(){
 vec2 q=(var_texcoord0-.5)*2.0;float r=length(q);
 if(r>1.0)discard;
 float rim=exp(-100.0*pow(r-.89,2.0));
 float pulse=.80+.20*sin(frame.x*3.0+atan(q.y,q.x)*3.0);
 float scan=pow(.5+.5*sin(q.y*25.0-frame.x*2.0),12.0)*.035;
 float a=(rim*.9*pulse+.025+scan)*tint.a;
 out_fragColor=vec4(tint.rgb*a,a);
}
