-- Finger-sized hit regions around actual camera-facing actor drawings.
-- Selection never changes projectile collision or computes a shot preview.
local Layout=require 'main.layout'
local View=require 'main.view'
local H={}
local function rect(g,p,width,height,padding,min_width,min_height)
 local x,y=g.project(g,p,0)
 local edge=g.project(g,{p[1]+width/2,p[2]},0)
 local _,top=g.project(g,p,height/.6)
 local w=math.max(min_width or 0,math.abs(edge-x)*2)
 local h=math.max(min_height or 0,math.abs(top-y))
 return{x=x,y=y+h/2,w=w+padding*2,h=h+padding*2,foot_x=x,foot_y=y,visual_h=math.abs(top-y)}
end
local function inside(r,x,y)return math.abs(x-r.x)<=r.w/2 and math.abs(y-r.y)<=r.h/2 end
function H.own(g,x,y)
 if not g.project or not View.field(g,x,y)then return false end
 return inside(H.hero(g),x,y)
end
function H.hero(g)
 -- The touch silhouette grows with the drawing; the movement/shot collider
 -- remains unchanged so a powerful hero can still traverse every existing lane.
 local state=g.power_state and g:power_state()or nil
 local size=math.max(1,math.min(1.75,g.hero_visual_scale or(state and state.visual_scale)or 1))
 return rect(g,g.p,1.45*size,2.1*size,8,48,72)
end
function H.dimensions(e)
 if e.optional then return .7,1.19 end
 if e.kind=='mini_drone'then return 1.15,1.25 end
 if e.kind=='splitter'then return 1.7,1.75 end
 if e.kind=='crawler'then return 1.65,1.25 end
 if e.kind=='wisp'then return 1.2,1.7 end
 if e.kind=='relay'or e.kind=='sequence'then return 1,1.7 end
 if e.boss then return 3.72,3.6 end
 return 2.25,2.15
end
function H.bounds(g,e,padding)
 local w,h=H.dimensions(e);return rect(g,e.p,w,h,padding or 18,48,64)
end
function H.visible(g,e)
 -- Orthographic camera points from (0,24,18). Test silhouette points toward
 -- the camera, not line of fire: peeking actors remain selectable over cover.
 local width,height=H.dimensions(e)
 local walls=g:active()
 for _,fraction in ipairs({.22,.55,.88})do
  local z=e.p[2]-.8*height*fraction;local y=.6*height*fraction
  for _,side in ipairs({-.25,0,.25})do
   local x=e.p[1]+width*side;local hidden=false
   for _,wall in ipairs(walls)do
    local r=wall.r
    if x>=r[1]and x<=r[1]+r[3]and r[2]+r[4]>=z then
     local entry=math.max(z,r[2]);local h=wall.height or g.data.visual_wall_height or 1.6
     if y+(entry-z)*(24/18)<h then hidden=true;break end
    end
   end
   if not hidden then return true end
  end
 end
 return false
end
function H.enemy(g,x,y)
 if not g.project or not View.field(g,x,y)then return nil end
 local selected,score=nil,math.huge
 for _,e in ipairs(g.enemies)do if e.hp>0 then
  local r=H.bounds(g,e)
  if inside(r,x,y)and H.visible(g,e)then
   local value=((x-r.x)/(r.w/2))^2+((y-r.y)/(r.h/2))^2
   if value<score then selected,score=e,value end
  end
 end end
 return selected
end
return H
