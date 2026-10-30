-- Shared camera mathematics for rendering, touch unprojection and world overlays.
local Layout=require 'main.layout'
local M={width=Layout.width,height=Layout.height,bottom=Layout.bottom,top=Layout.top,left=Layout.left,right=Layout.right,size=8.8,min_zoom=.75,max_zoom=1.75}
local function campaign(g)return g and g.data and(g.data.campaign_enabled or g.data.campaign_v14)end
function M.arena(g)return g.arena or(g.m and g.m.arena)or g.data.arena end
function M.viewport(g,w,h)
 w=w or M.width;h=h or M.height
 local left,bottom,width,height=M.left,M.bottom,M.right-M.left,M.top-M.bottom
 if campaign(g)then
  local a=M.arena(g);local wanted=a[3]/(.8*a[4]);local pixelw,pixelh=w*width/M.width,h*height/M.height
  if pixelw/pixelh>wanted then local nextw=pixelh*wanted;left=left+(pixelw-nextw)/w*M.width/2;width=nextw/w*M.width
  else local nexth=pixelw/wanted;bottom=bottom+(pixelh-nexth)/h*M.height/2;height=nexth/h*M.height end
 end
 return{left=left,bottom=bottom,width=width,height=height,right=left+width,top=bottom+height,px=left*w/M.width,py=bottom*h/M.height,pw=width*w/M.width,ph=height*h/M.height}
end
function M.field(g,x,y)
 if not campaign(g)then return Layout.field(x,y)end
 local w,h=window.get_size();local r=M.viewport(g,w,h)
 return x>r.left and x<r.right and y>r.bottom and y<r.top
end
function M.minimum_zoom(g)
 if not campaign(g)then return M.min_zoom end
 local a=M.arena(g);local aspect=a[3]/(.8*a[4]);return math.max(M.size,10/aspect)/(.8*a[4])
end
function M.zoom_factor(value,g)
 if type(value)~='number'or value~=value or value==math.huge or value==-math.huge then return 1 end
 local minimum=M.minimum_zoom(g)
 local zoom=math.max(minimum,math.min(M.max_zoom,value))
 -- Repeated decimal button steps may land a few ULPs below a bound. Keep the
 -- public limits canonical before Zoom:set's no-change/save-write tolerance.
 if math.abs(zoom-minimum)<.000001 then return minimum end
 if math.abs(zoom-M.max_zoom)<.000001 then return M.max_zoom end
 return zoom
end
function M.matrices(w,h,center,zoom,arena)
 local pixel_height=h*(M.top-M.bottom)/M.height
 local aspect=(w*(M.right-M.left)/M.width)/pixel_height
 if arena then aspect=arena[3]/(.8*arena[4])end
 local context=arena and{arena=arena,data={campaign_enabled=true}}or nil
 local size=math.max(M.size,10/aspect)/M.zoom_factor(zoom,context)
 local x,z=center[1],center[2]
 local view=vmath.matrix4_look_at(vmath.vector3(x,24,z+18),vmath.vector3(x,0,z),vmath.vector3(0,1,0))
 local projection=vmath.matrix4_orthographic(-size*aspect/2,size*aspect/2,-size/2,size/2,.1,100)
 return view,projection,aspect,size
end
function M.project(g,p,height)
 local w,h=window.get_size();local v,projection=M.matrices(w,h,g.camera or{0,0},g.zoom,campaign(g)and M.arena(g)or nil)
 local q=projection*v*vmath.vector4(p[1],height or .75,p[2],1);local r=M.viewport(g,w,h)
 return r.left+(q.x/q.w+1)*r.width/2,r.bottom+(q.y/q.w+1)*r.height/2
end
function M.unproject(g,x,y)
 local w,h=window.get_size();local v,p=M.matrices(w,h,g.camera or{0,0},g.zoom,campaign(g)and M.arena(g)or nil);local inv=vmath.inv(p*v);local r=M.viewport(g,w,h)
 local nx=(x-r.left)/r.width*2-1;local ny=(y-r.bottom)/r.height*2-1
 local near=inv*vmath.vector4(nx,ny,-1,1);local far=inv*vmath.vector4(nx,ny,1,1)
 local a=vmath.vector3(near.x/near.w,near.y/near.w,near.z/near.w);local d=vmath.vector3(far.x/far.w,far.y/far.w,far.z/far.w)-a
 local t=-a.y/d.y
 return{a.x+d.x*t,a.z+d.z*t}
end
function M.ground(g,x,y)
 local p=M.unproject(g,x,y);local r=M.arena(g)
 return{math.max(r[1]+.5,math.min(r[1]+r[3]-.5,p[1])),math.max(r[2]+.5,math.min(r[2]+r[4]-.5,p[2]))}
end
local function power_scale(g)
 if not g.power_state then return nil end
 local state=g:power_state()
 if not state.enabled or state.count==0 then return nil end
 return math.max(1,math.min(1.75,state.visual_scale or 1))
end
function M.clamp_camera(g,center)
 local r=M.arena(g);local w,h=window.get_size();local _,_,aspect,size=M.matrices(w,h,{0,0},g.zoom,campaign(g)and r or nil);local cx,cz=r[1]+r[3]/2,r[2]+r[4]/2
 if campaign(g)then
  local ex=math.max(0,(r[3]-size*aspect)/2);local ez=math.max(0,(r[4]-size/.8)/2)
  return{math.max(cx-ex,math.min(cx+ex,center[1])),math.max(cz-ez,math.min(cz+ez,center[2]))}
 end
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
 if campaign(g)then
  local zoom=M.zoom_factor(g.zoom,g)
  if g.zoom~=zoom then g.zoom=zoom;if g.saved then g.saved.zoom=zoom end end
 end
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
