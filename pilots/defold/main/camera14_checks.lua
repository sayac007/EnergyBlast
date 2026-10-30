-- Actual native matrices, viewport and controller bounds for all campaign fields.
-- A whole-map view uses neutral letterboxing; it never exposes an outer world.
local View=require 'main.view'
local Zoom=require 'main.zoom'
local Layout=require 'main.layout'
local M={}
function M.run(data)
 if not(data.campaign_enabled or data.campaign_v14)then return 0 end
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function near(a,b)return math.abs(a-b)<.0001 end
 local original_size=window.get_size
 for _,resolution in ipairs({{1280,720},{1280,800},{1920,1080}})do
  local w,h=resolution[1],resolution[2];window.get_size=function()return w,h end
  for index,mission in ipairs(data.missions)do
   local r=mission.arena or data.arena
   local g={data=data,m=mission,arena=r,p={mission.spawn[1],mission.spawn[2]},saved={},path={},changed=function()end}
   g.power_state=function()return{enabled=true,count=16,visual_scale=1.25}end
   local minimum=View.minimum_zoom(g);local viewport=View.viewport(g,w,h)
   check(near(viewport.pw/viewport.ph,r[3]/(.8*r[4])),'real viewport matches individual map aspect '..index)
   check(viewport.left>=Layout.left-.0001 and viewport.right<=Layout.right+.0001 and viewport.bottom>=Layout.bottom-.0001 and viewport.top<=Layout.top+.0001,'map viewport stays away from HUD '..index)
   check(minimum>0 and minimum<=1 and near(View.zoom_factor(-999,g),minimum),'zoom stops exactly at full-map boundary '..index)
   local cx,cz=r[1]+r[3]/2,r[2]+r[4]/2
   for _,zoom in ipairs({minimum,1,1.75})do
    g.zoom=zoom;g.camera=View.clamp_camera(g,{999,-999})
    local view,projection,aspect,size=View.matrices(w,h,g.camera,zoom,r)
    check(size/.8<=r[4]+.0001 and size*aspect<=r[3]+.0001,'no zoomed-out frustum larger than field '..index)
    -- Camera clamping must hold for the real ground plane at every screen corner,
    -- including a fully upgraded hero: old power cannot expand the camera bounds.
    for _,point in ipairs({{viewport.left,viewport.bottom},{viewport.right,viewport.bottom},{viewport.left,viewport.top},{viewport.right,viewport.top}})do
     local ground=View.unproject(g,point[1],point[2])
     check(ground[1]>=r[1]-.0001 and ground[1]<=r[1]+r[3]+.0001 and ground[2]>=r[2]-.0001 and ground[2]<=r[2]+r[4]+.0001,'every visible floor corner belongs to map '..index)
    end
    for _,p in ipairs({{cx,cz},{cx-r[3]*.2,cz+r[4]*.15},{cx+r[3]*.2,cz-r[4]*.15}})do
     local x,y=View.project(g,p,0);local q=View.unproject(g,x,y)
     check(near(p[1],q[1])and near(p[2],q[2]),'render and touch use the same map viewport '..index)
    end
    if near(zoom,minimum)then
     check(near(g.camera[1],cx)and near(g.camera[2],cz),'full-map inspection centres whole field '..index)
     for _,p in ipairs({{r[1],r[2]},{r[1]+r[3],r[2]+r[4]}})do
      local x,y=View.project(g,p,0)
      check(x>=viewport.left-.001 and x<=viewport.right+.001 and y>=viewport.bottom-.001 and y<=viewport.top+.001,'both full-map diagonal corners are visible '..index)
     end
    end
   end
   check(View.field(g,(viewport.left+viewport.right)/2,(viewport.bottom+viewport.top)/2),'real centre accepts touch '..index)
   if viewport.left>Layout.left+.5 then check(not View.field(g,(Layout.left+viewport.left)/2,360),'neutral side band cannot move or launch a drone '..index)
   elseif viewport.bottom>Layout.bottom+.5 then check(not View.field(g,640,(Layout.bottom+viewport.bottom)/2),'neutral lower band cannot move or launch a drone '..index)end
   g.zoom=1;g.camera={cx,cz};g.saved.zoom=1;local control=Zoom.new(g)
   for _=1,20 do control:step(-1)end
   check(near(g.zoom,minimum)and near(g.saved.zoom,minimum),'actual minus controller persists complete-map scale '..index)
   local changes=0;g.changed=function()changes=changes+1 end
   check(not control:step(-1)and changes==0,'zoom beyond arena edge neither moves nor rewrites saves '..index)
  end
 end
 window.get_size=original_size
 check(View.zoom_factor(-999)==.75 and View.zoom_factor(999)==1.75,'historical camera defaults remain unchanged')
 return n
end
return M
