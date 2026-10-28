#version 140
// Original soft stylized lighting; actual baked AO or painted albedo is sampled.
in highp vec4 var_position;
in mediump vec3 var_normal;
in mediump vec2 var_texcoord0;
in mediump vec4 var_light;
out vec4 out_fragColor;
uniform mediump sampler2D tex0;
uniform fs_uniforms { mediump vec4 tint; mediump vec4 surface; };
void main(){
 vec3 n=normalize(var_normal), l=normalize(var_light.xyz-var_position.xyz), v=normalize(-var_position.xyz);
 vec3 tex=texture(tex0,var_texcoord0).rgb;
 vec3 base=surface.x>.5?pow(tex,vec3(2.2))*tint.rgb:tint.rgb*mix(1.0,tex.r,.78);
 float diffuse=smoothstep(-.25,.95,dot(n,l));
 vec3 ambient=mix(vec3(.62,.69,.84),vec3(1.0,.97,.88),n.y*.5+.5);
 float spec=pow(max(0.0,dot(n,normalize(l+v))),28.0)*.10;
 float rim=pow(1.0-max(0.0,dot(n,v)),3.0)*.055;
 vec3 lit=base*ambient*(.57+.43*diffuse)+vec3(1.0,.88,.66)*spec+vec3(.24,.60,.66)*rim;
 lit=mix(lit,base*1.55,surface.y);
 out_fragColor=vec4(pow(max(lit,vec3(0.0)),vec3(1.0/2.2)),1.0);
}
