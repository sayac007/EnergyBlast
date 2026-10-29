-- Single solid-surface specification consumed by physics and the mesh generator.
local S={}
function S.for_mission(data,m)
 local a=data.arena
 local walls={{r={a[1],a[2],a[3],.3},type='border'},{r={a[1],a[2]+a[4]-.3,a[3],.3},type='border'},{r={a[1],a[2],.3,a[4]},type='border'},{r={a[1]+a[3]-.3,a[2],.3,a[4]},type='border'}}
 for _,r in ipairs(m.covers)do walls[#walls+1]={r=r,type='cover'}end
 for _,r in ipairs(m.reflectors)do walls[#walls+1]={r=r,type='reflector'}end
 local visual=data.visual_surfaces and data.visual_surfaces[m.id]
 for i,wall in ipairs(walls)do wall.height=visual and visual[i]and visual[i].height or data.visual_wall_height or 1.6 end
 return walls
end
return S
