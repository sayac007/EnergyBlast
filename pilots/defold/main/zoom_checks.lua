-- Native camera math and real-controller coexistence; no hardware pinch claim.
local View=require 'main.view'
local Zoom=require 'main.zoom'
local Combat=require 'main.combat'
local Touch=require 'main.touch'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function near(a,b)return math.abs(a-b)<.0001 end
 local function fresh(saved)
  local g=Combat.new(data,saved);g:load(1);g.p={0,0};g.enemies={};g.walls={};g.bonus={tasks={},total=0,completed=0};g.camera={0,0};g.project=View.project
  local changes=0;g.changed=function()changes=changes+1 end
  g.touch=Touch.new(g,function(x,y)return View.ground(g,x,y)end);g.control_tick=function(dt)g.touch:update(dt)end
  local z=Zoom.new(g);g.zoom_control=z
  return g,z,function()return changes end
 end
 local function dispatch(g,z,packet)
  local consumed=z:input(packet)
  if not consumed then for _,a in ipairs(packet)do g.touch:input(a)end end
  return consumed
 end
 local function contact(id,x,y,kind)return{id=id,x=x,y=y,pressed=kind=='press',released=kind=='release'}end
 local g,z,changes=fresh()
 check(g.zoom==1,'old profiles keep exactly the previous default camera scale')
 for _,factor in ipairs({.75,1,1.75})do
  g.zoom=factor
  for _,p in ipairs({{-2,-2},{0,0},{2.5,2}})do
   local x,y=View.project(g,p,0);local q=View.ground(g,x,y)
   check(near(p[1],q[1])and near(p[2],q[2]),'actual projection and touch unprojection agree at '..factor)
  end
 end
 for _,window_size in ipairs({{1280,720},{1280,800},{1920,1080}})do
  local w,h=window_size[1],window_size[2]
  for _,factor in ipairs({.75,1,1.75})do
   local v,p,aspect,size=View.matrices(w,h,{1,-1},factor)
   check(near(size,math.max(8.8,10/aspect)/factor),'aspect-correct whole-scene zoom '..w..' '..factor)
   local q=p*v*vmath.vector4(2,0,-2,1);local inverse=vmath.inv(p*v)*q
   check(near(inverse.x/inverse.w,2)and near(inverse.z/inverse.w,-2),'native camera inverse remains valid '..w..' '..factor)
  end
 end
 g.zoom=1;g.camera={0,0};local x1=View.project(g,{1,0},0);local x0=View.project(g,{0,0},0)
 g.zoom=1.75;local x2=View.project(g,{1,0},0);local center=View.project(g,{0,0},0)
 check(near((x2-center)/(x1-x0),1.75),'actors and every world distance magnify together')
 check(View.zoom_factor(nil)==1 and View.zoom_factor('2')==1,'missing and nonnumeric preferences are safe')
 check(View.zoom_factor(0/0)==1 and View.zoom_factor(math.huge)==1,'NaN and infinite preferences never poison matrices')
 check(View.zoom_factor(-4)==.75 and View.zoom_factor(50)==1.75,'zoom range is bounded')
 check(View.zoom_factor(1.75-.00000001)==1.75 and View.zoom_factor(.75+.00000001)==.75,'floating-point steps normalize to exact public limits')
 g,z,changes=fresh();local total=g:total();check(z:step(1)and near(g.zoom,1.15),'plus button magnifies the complete scene')
 check(changes()==1 and near(g.saved.zoom,1.15),'one explicit zoom action persists exactly once')
 check(z:step(-1)and near(g.zoom,1),'minus button restores previous scale')
 check(g:total()==total,'inspection cannot award or spend stars')
 for i=1,20 do z:step(1)end
 check(g.zoom==1.75,'repeated plus cannot exceed the upper bound')
 local count=changes();check(not z:step(1)and changes()==count,'pressing beyond the limit does not rewrite saves')
 for i=1,20 do z:step(-1)end
 check(g.zoom==.75,'repeated minus cannot exceed the lower bound')
 local restored=Combat.new(data,g.saved);Zoom.new(restored)
 check(restored.zoom==.75,'chosen scale survives save reconstruction')
 g,z=fresh();local anchor=View.unproject(g,720,320);z:set(1.5,720,320);local after=View.unproject(g,720,320)
 check(near(anchor[1],after[1])and near(anchor[2],after[2]),'zoom preserves the floor under its focal point')
 local camera={g.camera[1],g.camera[2]};View.follow(g,.25,false)
 check(near(camera[1],g.camera[1])and near(camera[2],g.camera[2]),'inspection remains in view while the hero stands still')
 g.p[1]=g.p[1]+1;View.follow(g,.25,false)
 check(g.zoom_focus==nil,'moving the hero resumes ordinary following')
 local clamped=View.clamp_camera(g,{999,-999});local again=View.clamp_camera(g,clamped)
 check(near(clamped[1],again[1])and near(clamped[2],again[2])and clamped[1]<999 and clamped[2]>-999,'camera remains within zoom-aware arena limits')
 g,z,changes=fresh();g.path={{2,1}}
 check(dispatch(g,z,{contact(1,540,180,'press'),contact(2,780,180,'press')}),'two simultaneous floor contacts belong to zoom before normal input')
 check(g.zooming and g.touch.pointer==nil and not g.held and #g.path==0 and g.shots_fired==0,'pinch start stops movement and firing without emitting')
 check(z:blocks_mouse(),'native multitouch suppresses duplicate primary mouse callbacks')
 dispatch(g,z,{contact(1,480,180),contact(2,840,180)})
 check(near(g.zoom,1.5)and changes()==0,'pinch distance changes zoom without per-frame disk writes')
 for i=1,20 do g:update(.02)end
 check(g.shots_fired==0 and g.touch.pending_shot==nil,'holding a pinch never turns into auto fire')
 check(dispatch(g,z,{contact(2,840,180,'release')}),'lifting the first finger consumes its release')
 check(not g.zooming and changes()==1,'completed pinch persists exactly once')
 check(dispatch(g,z,{contact(1,500,180)}),'remaining finger movement stays quarantined')
 check(dispatch(g,z,{contact(1,500,180,'release')}),'remaining finger release stays quarantined')
 check(not z:blocks_mouse()and g.shots_fired==0 and #g.path==0,'all fingers up restores ordinary input without a stray action')
 check(not dispatch(g,z,{contact(3,800,180,'press')}),'next intentional single-finger gesture remains normal')
 g:update(.04);dispatch(g,z,{contact(3,800,180,'release')})
 check(#g.path>0 and g.shots_fired==0,'ordinary short tap moves after a pinch')
 g,z,changes=fresh();dispatch(g,z,{contact(1,800,180,'press')});g:update(.06)
 check(g.touch.pointer~=nil and g.pending_hold,'first floor finger retains the familiar short-tap grace period')
 dispatch(g,z,{contact(1,800,180),contact(2,540,180,'press')})
 check(g.touch.pointer==nil and not g.pending_hold and g.zooming,'adding second finger cancels the first aim intent')
 for i=1,20 do g:update(.02)end
 check(g.shots_fired==0,'cancelled pre-pinch aim cannot fire later')
 dispatch(g,z,{contact(1,800,180,'release'),contact(2,540,180,'release')})
 check(changes()==0,'a pinch that never changed scale causes no save write')
 g,z=fresh();check(not z:input({contact(1,72,340,'press'),contact(2,540,180,'press')}),'HUD and floor fingers cannot accidentally start zoom')
 check(not g.zooming and g.zoom==1,'HUD ownership preserves the current zoom')
 z:cancel();check(not z:blocks_mouse(),'explicit context cancellation clears tracked finger ownership')
 g,z,changes=fresh();dispatch(g,z,{contact(1,540,180,'press'),contact(2,780,180,'press')});dispatch(g,z,{contact(1,510,180),contact(2,810,180)})
 local scale=g.zoom;z:cancel();g.touch:cancel()
 check(not g.zooming and changes()==1 and g.zoom==scale,'menu/background cancellation ends zoom and persists its chosen scale')
 dispatch(g,z,{contact(1,510,180,'release')});dispatch(g,z,{contact(2,810,180,'release')})
 check(g.shots_fired==0 and #g.path==0,'post-cancel finger releases cannot revive a stale gesture')
 for _,state in ipairs({'paused','background','tactical_pause'})do
  g,z=fresh();g[state]=true
  check(not z:step(1)and g.zoom==1,'zoom buttons respect '..state)
  check(not z:input({contact(1,540,180,'press'),contact(2,780,180,'press')})and not g.zooming,'pinch respects '..state)
 end
 return n
end
return M
