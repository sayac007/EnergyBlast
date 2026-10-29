-- Previous combat scenarios retained as native regression fixtures.
local Combat=require 'main.combat'
local M={}
function M.run(g)
 local n=0;local function check(v,m)n=n+1;assert(v,m)end;local function step(t)for i=1,math.floor(t/.025)do g:update(.025)end end
 g.paused=false;local x,y=g.project(g,{-4,2},0);g.input({x=x,y=y,pressed=true});g.input({x=x,y=y,released=true});check(#g.path>0,'tap-to-move');g:load(1);local sx,sy=g.project(g,{-3,2},0);local tx,ty=g.project(g,{1.392857,-4.35},0);g.input({x=sx,y=sy,pressed=true});g.input({x=tx,y=ty});step(.325);g.input({x=tx,y=ty,released=true});check(#g.bullets>0,'long-hold release fires');check(math.abs(g.aim[1]-.581238)<.01,'native gesture/world projection');g.held=true;g.aiming=true;g.cancel_controls();check(not g.held and not g.aiming,'cancel held combat input');g:load(1);check(#g.enemies==1 and g.enemies[1].hp==2,'live cannon');g.p={3,2};g.aim=Combat.norm({1.5,-2});g:fire();step(.4);check(g.enemies[1].hp==2,'shield blocks direct fire')
 g:load(1);g.p={4.5,3.2};step(1);check(g.enemies[1].warning>0,'windup');step(2);check(g.hp<3,'real enemy hit');local hp=g.hp;g:hit_player();check(g.hp==hp,'invulnerability')
 g:load(1);step(4);check(g.hp==3,'cover intercepts shells');check(g:total()==0,'no wait farming');g.aim=Combat.norm({8.5,-11.9});g:fire();step(1.8);check(g.enemies[1].hp==1,'bank shot');g:fire();step(1.8);check(g.solved,'enemy destroyed');check(g:total()==100 and g:credits()==2,'one-time combat reward');g:finish();check(g:total()==100,'no replay double award');g:load(2);check(#g.enemies==2,'second sector');g:navigate({5.2,-3.5});check(#g.path>0 and g.path[#g.path][2]>-1.1,'staging at closed gate')
 n=n+require('main.raid_checks').run(g)
 return n
end
return M
