-- Shared camera mathematics for rendering, touch unprojection and world overlays.
local M={width=720,height=1280,bottom=250,top=1130,size=12.2}
function M.matrices(w,h,center)
 local pixel_height=h*(M.top-M.bottom)/M.height
 local aspect=w/pixel_height;local size=math.max(M.size,10/aspect)
 local x,z=center[1],center[2]
 local view=vmath.matrix4_look_at(vmath.vector3(x+18,24,z),vmath.vector3(x,0,z),vmath.vector3(0,1,0))
 local projection=vmath.matrix4_orthographic(-size*aspect/2,size*aspect/2,-size/2,size/2,.1,100)
 return view,projection,aspect,size
end
function M.project(g,p,height)
 local w,h=window.get_size();local v,projection=M.matrices(w,h,g.camera or{0,0})
 local q=projection*v*vmath.vector4(p[1],height or .75,p[2],1)
 return(q.x/q.w+1)*M.width/2,M.bottom+(q.y/q.w+1)*(M.top-M.bottom)/2
end
function M.ground(g,x,y)
 local w,h=window.get_size();local v,p=M.matrices(w,h,g.camera or{0,0});local inv=vmath.inv(p*v)
 local nx=x/M.width*2-1;local ny=(y-M.bottom)/(M.top-M.bottom)*2-1
 local near=inv*vmath.vector4(nx,ny,-1,1);local far=inv*vmath.vector4(nx,ny,1,1)
 local a=vmath.vector3(near.x/near.w,near.y/near.w,near.z/near.w);local d=vmath.vector3(far.x/far.w,far.y/far.w,far.z/far.w)-a
 local t=-a.y/d.y;local r=g.data.arena
 return{math.max(r[1]+.5,math.min(r[1]+r[3]-.5,a.x+d.x*t)),math.max(r[2]+.5,math.min(r[2]+r[4]-.5,a.z+d.z*t))}
end
function M.follow(g,dt,snap)
 local r=g.data.arena;local w,h=window.get_size();local _,_,aspect,size=M.matrices(w,h,{0,0});local cx,cz=r[1]+r[3]/2,r[2]+r[4]/2
 local ex=math.max(0,(r[3]-size/.8)/2+.3);local ez=math.max(0,(r[4]-size*aspect)/2+.3)
 local x=math.max(cx-ex,math.min(cx+ex,g.p[1]));local z=math.max(cz-ez,math.min(cz+ez,g.p[2]))
 if snap or not g.camera then g.camera={x,z};return end
 if g.pending_hold or g.aiming then return end
 local blend=1-math.exp(-7*dt);g.camera[1]=g.camera[1]+(x-g.camera[1])*blend;g.camera[2]=g.camera[2]+(z-g.camera[2])*blend
end
return M
