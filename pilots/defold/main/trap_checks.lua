-- Real combat/controller regression: explicit field placement, never a fire gesture.
local C=require 'main.combat'
local P=require 'main.projectiles'
local O=require 'main.objectives'
local View=require 'main.view'
local M={}
function M.run(g)
 local n=0;local spoken={};local prior_say=g.say
 g.say=function(id)spoken[#spoken+1]=id end
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh()
  g.saved={earned={},clues={},weapon='pulse',schema=2,purchases={},spent={}};g:load(4)
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil end
  View.follow(g,0,true);spoken={}
 end
 local function step(seconds)for i=1,math.floor(seconds/.025+.001)do g:update(.025)end end
 local function point(p)local x,y=g.project(g,p,0);return{x=x,y=y}end
 fresh();local c=g.trap_control
 check(c~=nil and #O.catalogue==3,'three explicit trap choices share their real gameplay specs')
 local p=point({-5.8,4.8});p.id=1;p.pressed=true;g.input(p);g:update(.325)
 check(g.aiming,'normal long hold still arms aim before catalogue opens')
 check(c:open()and g.trap_ui.mode=='catalogue'and g.tactical_pause,'field catalogue opens tactical pause')
 check(not g.aiming and not g.pending_hold and not g.held and not g.touch.pointer,'catalogue clears all pending shooting gestures')
 check(spoken[#spoken]=='defold_trap_open','catalogue has matching spoken instruction')
 local clock=g.clock;local enemy={g.enemies[1].p[1],g.enemies[1].p[2]}
 local bullet=P.spawn(g,{-6,4},{1,0},true);local age=bullet.age;g:update(1)
 check(g.clock==clock and C.dist(enemy,g.enemies[1].p)==0 and bullet.age==age,'catalogue freezes enemies and live projectiles, not just labels')
 g.cooldown=0;g:fire();check(g.shots_fired==0,'fire cannot leak through a tactical pause')
 check(not c:select('bad')and g.trap_ui.mode=='catalogue','unknown trap cannot select or consume anything')
 check(c:select('frost')and g.trap_ui.mode=='place'and g.trap_ui.selected=='frost','catalogue selection changes real trap type')
 check(spoken[#spoken]=='defold_trap_frost','placement instruction names the selected device and next floor tap')
 check(not c:place({7,4})and #g.traps==0 and g.trap_ui.reason=='ZU WEIT WEG','range rejects teleport placement')
 check(not c:place({-2,0})and #g.traps==0 and g.trap_ui.reason=='HIER IST EINE WAND','solid wall rejects placement')
 g.p={-4,0};check(not c:place({-.5,0})and #g.traps==0 and g.trap_ui.reason=='WAND DAZWISCHEN','nearby floor behind a wall cannot be used')
 g.p={-7,4.8};local floor=point({-5.5,4.8})
 g.input({x=floor.x,y=floor.y,pressed=true,id=1})
 g.input({x=floor.x,y=floor.y,released=true,id=2})
 check(#g.traps==0 and c.pointer~=nil,'foreign finger cannot confirm another fingers placement')
 g.input({x=floor.x,y=floor.y,released=true,id=1})
 check(#g.traps==1 and C.dist(g.traps[1].p,{-5.5,4.8})<.001 and g.traps[1].type=='frost','press and release place selected device at touched floor')
 check(not g.trap_ui and not g.tactical_pause and g.shots_fired==0 and #g.path==0,'placement resumes without shot or accidental walking')
 check(g.trap_cooldown==7 and spoken[#spoken]=='defold_trap_place','frost consumes its real cooldown and acknowledges placement')
 check(not c:open()and not g.trap_ui,'recharging traps cannot be reopened for free devices')
 fresh();c=g.trap_control;c:open();c:select('pulse');c:cancel(true)
 check(not g.trap_ui and not g.tactical_pause and #g.traps==0 and g.shots_fired==0,'cancel leaves no trap and no pending fire')
 p=point({-5,4});g.input({x=p.x,y=p.y,released=true,id=1});check(g.shots_fired==0 and #g.path==0,'late release after cancellation cannot fire or move')
 c:open();local camera={g.camera[1],g.camera[2]};g.p={8,-4};View.follow(g,1,false)
 check(C.dist(camera,g.camera)==0,'placement camera cannot drift under a finger')
 g:load(1);check(not g.trap_ui and not g.tactical_pause and not c:open(),'sector change closes catalogue and combat sectors cannot open it')
 fresh();g.paused=true;check(not c:open(),'paused menu cannot open trap mode');g.paused=false;g.background=true;check(not c:open(),'background app cannot open trap mode');g.background=false;g.over=true;check(not c:open(),'finished round cannot open trap mode')
 fresh();g.p={3,-4};g:trap(nil,'frost');local e=g.enemies[1];e.p={3,-4};g:update(.025)
 check(e.trapped>8.9 and #g.traps==0 and e.hp==3,'ice really holds nine seconds without dealing damage')
 local frozen_clock=e.timer;step(.5);check(e.timer==frozen_clock,'held guardian cannot charge or shoot')
 fresh();g.p={3,-4};g:trap(nil,'pulse');e=g.enemies[1];e.p={3,-4};g:update(.025)
 check(e.hp==1 and e.trapped>4.9 and #g.traps==0 and not g.solved,'pulse removes two shielded guardian energy and gives time for the voice cue and a shot')
 check(g:total()==0 and spoken[#spoken]=='defold_trap_trigger','trap activation alone awards no stars and speaks the firing opportunity')
 fresh();g.p={3,-4};e=g.enemies[1];e.p={3,-4};e.trapped=8;g:trap(nil,'magnet');g:update(.025)
 check(e.trapped>7.9,'a later shorter trap cannot shorten an already longer shield opening')
 fresh();g.p={-7,4.8};for i=1,3 do g.trap_cooldown=0;g:trap({-7+i*.3,4.8},'magnet')end
 check(#g.traps==2,'at most two planted devices exist')
 step(12.3);check(#g.traps==0,'all unused trap types expire from the world')
 fresh();local target=point({-5.5,4.8});g.input({x=target.x,y=target.y,pressed=true,id=1});step(.325);g.input({x=target.x,y=target.y,released=true,id=1})
 check(g.shots_fired==1 and not g.trap_ui,'ordinary hold release still fires exactly one shot')
 g.say=prior_say
 return n
end
return M
