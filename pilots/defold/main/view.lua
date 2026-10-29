-- Shared camera mathematics for rendering, touch unprojection and world overlays.
local Layout=require 'main.layout'
local M={width=Layout.width,height=Layout.height,bottom=Layout.bottom,top=Layout.top,left=Layout.left,right=Layout.right,size=8.8,min_zoom=.75,max_zoom=1.75}
function M.zoom_factor(value)
 if type(value)~='number'or value~=value or value==math.huge or value==-math.huge then return 1 end
 local zoom=math.max(M.min_zoom,math.min(M.max_zoom,value))
 -- Repeated decimal button steps may land a few ULPs below a bound. Keep the
 -- public limits canonical before Zoom:set's no-change/save-write tolerance.
 if math.abs(zoom-M.min_zoom)<.000001 then return M.min_zoom end
 if math.abs(zoom-M.max_zoom)<.000001 then return M.max_zoom end
 return zoom
end
function M.matrices(w,h,center,zoom)
 local pixel_height=h*(M.top-M.bottom)/M.height
 local aspect=(w*(M.right-M.left)/M.width)/pixel_height;local size=math.max(M.size,10/aspect)/M.zoom_factor(zoom)
 local x,z=center[1],center[2]
 local view=vmath.matrix4_look_at(vmath.vector3(x,24,z+18),vmath.vector3(x,0,z),vmath.vector3(0,1,0))
 local projection=vmath.matrix4_orthographic(-size*aspect/2,size*aspect/2,-size/2,size/2,.1,100)
 return view,projection,aspect,size
end
function M.project(g,p,height)
 local w,h=window.get_size();local v,projection=M.matrices(w,h,g.camera or{0,0},g.zoom)
 local q=projection*v*vmath.vector4(p[1],height or .75,p[2],1)
 return M.left+(q.x/q.w+1)*(M.right-M.left)/2,M.bottom+(q.y/q.w+1)*(M.top-M.bottom)/2
end
function M.unproject(g,x,y)
 local w,h=window.get_size();local v,p=M.matrices(w,h,g.camera or{0,0},g.zoom);local inv=vmath.inv(p*v)
 local nx=(x-M.left)/(M.right-M.left)*2-1;local ny=(y-M.bottom)/(M.top-M.bottom)*2-1
 local near=inv*vmath.vector4(nx,ny,-1,1);local far=inv*vmath.vector4(nx,ny,1,1)
 local a=vmath.vector3(near.x/near.w,near.y/near.w,near.z/near.w);local d=vmath.vector3(far.x/far.w,far.y/far.w,far.z/far.w)-a
 local t=-a.y/d.y
 return{a.x+d.x*t,a.z+d.z*t}
end
function M.ground(g,x,y)
 local p=M.unproject(g,x,y);local r=g.data.arena
 return{math.max(r[1]+.5,math.min(r[1]+r[3]-.5,p[1])),math.max(r[2]+.5,math.min(r[2]+r[4]-.5,p[2]))}
end
local function power_scale(g)
 if not g.power_state then return nil end
 local state=g:power_state()
 if not state.enabled or state.count==0 then return nil end
 return math.max(1,math.min(1.75,state.visual_scale or 1))
end
function M.clamp_camera(g,center)
 local r=g.data.arena;local w,h=window.get_size();local _,_,aspect,size=M.matrices(w,h,{0,0},g.zoom);local cx,cz=r[1]+r[3]/2,r[2]+r[4]/2
 local ex=math.max(0,(r[3]-size*aspect)/2+.3);local ez=math.max(0,(r[4]-size/.8)/2+.3)
 local scale=power_scale(g)
 if scale then
  -- Allow the camera beyond arena edges so a grown head is never cropped by
  -- an old floor-only clamp, including at maximum user zoom.
  ex=ex+.725*scale;ez=ez+2.1*scale/.8
 end
 return{math.max(cx-ex,math.min(cx+ex,center[1])),math.max(cz-ez,math.min(cz+ez,center[2]))}
end
function M.follow(g,dt,snap)
 local scale=power_scale(g)
 -- The illustrated quad's centre, rather than its feet, follows the camera.
 local target=M.clamp_camera(g,scale and{g.p[1],g.p[2]-2.1*scale/1.6}or g.p)
 if snap or not g.camera then g.camera=target;g.zoom_focus=nil;return end
 if g.pending_hold or g.aiming or g.dragging or g.tactical_pause or g.zooming then return end
 if g.zoom_focus then
  local p=g.zoom_focus.player;local distance=(g.p[1]-p[1])^2+(g.p[2]-p[2])^2
  if distance<.08*.08 then return end
  g.zoom_focus=nil
 end
 local blend=1-math.exp(-7*dt);g.camera[1]=g.camera[1]+(target[1]-g.camera[1])*blend;g.camera[2]=g.camera[2]+(target[2]-g.camera[2])*blend
end
return M
