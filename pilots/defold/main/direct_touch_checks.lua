-- The real controller, real navigation graph and real swept projectile module.
local Combat=require 'main.combat'
local Touch=require 'main.touch'
local Regions=require 'main.hit_regions'
local Projectiles=require 'main.projectiles'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh()
  local g=Combat.new(data);g:load(1);g.enemies={};g.walls={};g.bonus={tasks={},total=0,completed=0};g.invulnerable=999
  g.project=function(_,p,h)return 640+p[1]*40,360-p[2]*32+(h or 0)*24 end
  local c=Touch.new(g,function(x,y)return{(x-640)/40,(360-y)/32}end)
  g.touch=c;g.control_tick=function(dt)c:update(dt)end
  return g,c
 end
 local function enemy(g,p)
  local e={p=p or{3,0},hp=100,max_hp=100,timer=999,warning=0,direction={0,1},burst=1};g.enemies[#g.enemies+1]=e;return e
 end
 local function press(c,x,y,id)c:input({pressed=true,x=x,y=y,id=id or 1})end
 local function release(c,x,y,id)c:input({released=true,x=x,y=y,id=id or 1})end
 local g,c=fresh();press(c,600,180);g:update(.06);release(c,600,180)
 check(g.shots_fired==0 and #g.path>0,'short ground tap moves without firing')
 g,c=fresh();press(c,980,480);g:update(.139)
 check(g.shots_fired==0 and g.pending_hold,'ground tap grace period does not fire early')
 g:update(.001)
 check(g.shots_fired==1 and g.held and c.pointer~=nil,'holding emits before finger release at140ms')
 for i=1,30 do g:update(.02)end
 check(g.shots_fired>=2,'held ground contact repeats using actual weapon cooldown')
 local count=g.shots_fired;release(c,980,480)
 check(g.shots_fired==count and not g.held and not g.aiming,'release adds no final shot')
 for i=1,30 do g:update(.02)end
 check(g.shots_fired==count,'releasing actually stops repeated fire')
 g,c=fresh();local e=enemy(g);local r=Regions.bounds(g,e)
 press(c,r.x+r.w/2-2,r.y)
 check(g.shots_fired==1 and c.pointer.seconds==0,'padded enemy press fires immediately without elapsed time')
 local bullet=g.bullets[1];local dx,dy=e.p[1]-g.p[1],e.p[2]-g.p[2];local length=math.sqrt(dx*dx+dy*dy)
 check(math.abs(bullet.direction[1]-dx/length)<.00001 and math.abs(bullet.direction[2]-dy/length)<.00001,'actor tap aims at actual actor position, not floor behind it')
 release(c,r.x,r.y);check(g.shots_fired==1,'short enemy release does not duplicate first shot')
 press(c,r.x,r.y);release(c,r.x,r.y)
 check(g.shots_fired==1 and c.pending_shot~=nil,'quick second enemy press is buffered rather than silently lost')
 for i=1,18 do g:update(.02)end
 check(g.shots_fired==2 and c.pending_shot==nil,'queued press fires once when weapon is ready without release action')
 for i=1,15 do g:update(.02)end;check(g.shots_fired==2,'buffered tap cannot become automatic fire')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);g.cooldown=.2
 press(c,r.x,r.y);release(c,r.x,r.y);press(c,600,180);release(c,600,180)
 for i=1,15 do g:update(.02)end
 check(c.pending_shot==nil and g.shots_fired==0,'new movement cancels queued attack intent before it emits')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);g.cooldown=1
 press(c,r.x,r.y);release(c,r.x,r.y);for i=1,20 do g:update(.02)end
 check(c.pending_shot==nil and g.shots_fired==0,'queued attack expires rather than firing a long-delayed shot')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);g.cooldown=.2
 press(c,r.x,r.y);release(c,r.x,r.y);e.hp=0;g:update(.05)
 check(c.pending_shot==nil and g.shots_fired==0,'dead buffered target cancels the shot')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);g.cooldown=.2
 press(c,r.x,r.y);release(c,r.x,r.y);g.paused=true;c:update(.05)
 check(c.pending_shot==nil and g.shots_fired==0,'menu pause cancels a queued tap after its finger was released')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);press(c,r.x+r.w/2+4,r.y)
 check(g.shots_fired==0 and c.pointer.mode=='ground','outside tolerance remains ordinary ground')
 release(c,r.x+r.w/2+4,r.y)
 check(#g.path>0,'ordinary near-miss ground tap still moves')
 g,c=fresh();e=enemy(g);local second=enemy(g,{3.45,0});r=Regions.bounds(g,second)
 check(Regions.enemy(g,r.x,r.y)==second,'nearest overlapping target wins rather than array order')
 e.hp=0;second.hp=0
 check(Regions.enemy(g,r.x,r.y)==nil,'dead actors are never touch targets')
 g,c=fresh();e=enemy(g);e.optional=true;e.kind='bonus_prism';r=Regions.bounds(g,e)
 press(c,r.x,r.y);check(g.shots_fired==1,'optional bonus crystal accepts same immediate actor gesture')
 check(Regions.enemy(g,1208,340)==nil,'HUD coordinates cannot select a world target')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e)
 g.walls={{r={e.p[1]-2,e.p[2]-2,4,4},height=6,type='cover'}}
 check(not Regions.visible(g,e)and Regions.enemy(g,r.x,r.y)==nil,'fully camera-occluded actor cannot be selected through solid geometry')
 g,c=fresh();e=enemy(g);r=Regions.bounds(g,e);g.walls={{r={-1.8,2.1,.6,.6},height=1.2,type='cover'}}
 press(c,r.x,r.y)
 check(g.shots_fired==1,'visible enemy across cover still responds immediately')
 local reflected=false
 for i=1,40 do Projectiles.update(g,.02);for _,b in ipairs(g.bullets)do reflected=reflected or b.bounces>0 end end
 check(reflected and e.hp==100,'instant target assistance never lets real shots bypass the wall')
 g,c=fresh();local px,py=g.project(g,g.p,1.75);local start=g.p[1]
 press(c,px,py);g:update(.8)
 check(g.shots_fired==0 and g.dragging and #g.path==0,'stationary contact on own hero never fires')
 c:input({x=px+80,y=py,id=1});for i=1,25 do g:update(.02)end
 check(g.p[1]>start+.2 and g.shots_fired==0,'own-body drag actually moves via navigation without firing')
 release(c,px+80,py)
 check(not g.dragging and #g.path==0,'lifting dragged hero stops movement')
 g,c=fresh();px,py=g.project(g,g.p,1.75);local navigation=g.navigate;local calls=0
 g.navigate=function(self,p)calls=calls+1;return navigation(self,p)end
 press(c,px,py)
 for i=1,40 do c:input({x=px+30+i,y=py,id=1})end
 check(calls==1,'high-frequency drag events do not rebuild path for every motion event')
 g:update(.1);check(calls<=2,'drag replans at bounded interval')
 g,c=fresh();g.walls={{r={-5,3.5,1,3},height=1.2,type='cover'}};px,py=g.project(g,g.p,1.75)
 press(c,px,py);c:input({x=px+100,y=py,id=1})
 for i=1,50 do g:update(.02);check(not g:blocked(g.p),'drag movement respects actual solid collision')end
 release(c,px+100,py)
 g,c=fresh();px,py=g.project(g,g.p,1.75);e=enemy(g,{g.p[1]+.1,g.p[2]})
 press(c,px,py);check(g.dragging and g.shots_fired==0,'own centre wins ambiguous overlapping body contact')
 g,c=fresh();e=enemy(g,{g.p[1]+.4,g.p[2]});r=Regions.bounds(g,e)
 press(c,r.x,r.y);check(g.shots_fired==1 and not g.dragging,'enemy centre still fires in close combat instead of being stolen by own-body tolerance')
 g,c=fresh();press(c,980,480,1);press(c,600,180,2);release(c,600,180,2)
 check(c.pointer and c.pointer.id==1,'foreign finger cannot replace or release active contact')
 g:update(.15);check(g.shots_fired==1,'original finger continues held-fire gesture')
 release(c,980,480,1);check(not g.held and c.pointer==nil,'owner release cleans held state')
 for _,state in ipairs({'paused','background','over'})do
  g,c=fresh();press(c,980,480);g:update(.15);local before=g.shots_fired;g[state]=true;c:update(.02)
  check(not g.held and not g.aiming and c.pointer==nil,'cancellation clears firing on '..state)
  release(c,980,480);check(g.shots_fired==before,'inactive release cannot fire on '..state)
 end
 g,c=fresh();px,py=g.project(g,g.p,1.75);press(c,px,py);c:input({x=px+90,y=py,id=1});c:cancel()
 check(not g.dragging and #g.path==0,'menu/focus cancellation stops dragged movement')
 g,c=fresh();press(c,980,480);g:update(.15);c:input({x=500,y=520,id=1})
 check(g.target[1]<0 and g.target[2]<0,'held fire changes aim as finger moves')
 return n
end
return M
