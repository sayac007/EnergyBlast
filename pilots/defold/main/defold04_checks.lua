-- Real Defold-runtime checks for duration input, expanded worlds and death effects.
local C=require 'main.combat'
local View=require 'main.view'
local M={}
function M.run(g)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function step(seconds)for i=1,math.floor(seconds/.025+.001)do g:update(.025)end end
 local function quiet()for _,t in ipairs(g.enemies)do t.timer=999;t.warning=0;t.patrol=nil end end
 local function load(i)g:load(i);quiet();View.follow(g,0,true)end
 local function press(p,id)local x,y=g.project(g,p,0);g.input({x=x,y=y,pressed=true,id=id});return{x=x,y=y,id=id}end
 local function release(a)a.pressed=nil;a.released=true;g.input(a)end
 local function aim(p)g.aim=C.norm({p[1]-g.p[1],p[2]-g.p[2]});g.cooldown=0;g:fire();step(1.7)end
 g.saved={earned={},clues={},weapon='pulse'};load(1)
 local a=press({-4,4});step(.25);release(a);check(g.shots_fired==0 and #g.path>0,'quick press moves')
 load(1);a=press(g.enemies[1].p);step(.1);release(a);check(g.shots_fired==0,'short enemy tap never fires')
 load(1);a=press({1,-6.525});step(.1);release(a);check(g.shots_fired==0,'short reflector tap never fires')
 load(1);a=press({-3,3});g.input({x=a.x+150,y=a.y-90});step(.1);release(a);check(g.shots_fired==0,'quick swipe cannot become a shot')
 load(1);a=press({-4,2});step(.325);check(g.aiming and #g.path==0,'stationary hold arms aiming on ordinary floor')
 check(g.shots_fired==0,'holding only aims');release(a);check(g.shots_fired==1,'long hold releases one shot')
 load(1);a=press({-4,2});step(.275);check(not g.aiming and g.pending_hold,'threshold is not early');step(.025);check(g.aiming,'aim starts at .30 seconds');release(a)
 load(1);a=press({-4,2});g:update(.35);check(g.aiming,'hold uses elapsed frame time even during slow rendering');g.cancel_controls()
 load(1);a=press({-4,2},1);g.input({x=a.x+120,y=a.y+100,released=true,id=2});check(g.touch.pointer~=nil and g.shots_fired==0,'foreign finger cannot end hold');g.cancel_controls();check(not g.aiming and not g.pending_hold,'cancel clears all held state')
 load(1);a=press({-4,2});step(.325);g.cancel_controls();release(a);check(g.shots_fired==0,'cancelled long hold never fires on resume')
 load(1);a=press({-4,2});step(.325);g.paused=true;g.touch:update(.1);g.paused=false;release(a);check(g.shots_fired==0,'pause cannot leak a pending shot')
 load(1);check(g.data.arena[3]==21 and g.data.arena[4]==15,'world is 2.25 times previous area')
 g.hp=99;g:navigate({-8.5,-4.5});step(4);check(C.dist(g.p,{-8.5,-4.5})<.7,'walk beyond old arena bounds')
 local previous={g.camera[1],g.camera[2]};View.follow(g,.5,false);check(C.dist(previous,g.camera)>.2,'camera follows position')
 for _,p in ipairs({{-8,3},{0,0},{8,-5}})do local x,y=g.project(g,p,0);local q=View.ground(g,x,y);check(C.dist(p,q)<.001,'camera projection/unprojection round trip')end
 a=press({7,-4});step(.325);local center={g.camera[1],g.camera[2]};g.p={-8,5};View.follow(g,.5,false);check(C.dist(center,g.camera)==0,'camera remains steady during aim');g.cancel_controls()
 load(1);g.aim=C.norm({8.5,-11.9});g:fire();step(2);check(g.enemies[1].hp==1,'expanded arena bank shot works')
 g:fire();step(2);check(g.solved and g:total()==100,'expanded first sector finishes with one-time reward')
 load(2);for _,t in ipairs(g.enemies)do g.p={t.p[1],t.p[2]+.65};aim(t.p);aim(t.p)end
 check(not g.solved,'second sector still requires exit');g.p={7.8,-5.25};g.clock=5;step(.025);check(g.solved,'expanded second core is reachable')
 load(3);g.p={-8.25,-3.75};aim(g.enemies[2].p);aim(g.enemies[2].p);aim({-1.5,-7.875});check(g.enemies[4].hp==0,'upper relay works at expanded coordinates')
 g.p={6,5.25};aim({11.4,3.75});check(g.enemies[5].hp==0 and not g:locked(g.enemies[1]),'right bank shot unlocks boss in expanded world')
 for i=1,3 do local t=g.enemies[i];g.p={t.p[1],t.p[2]+.65};for hit=1,3 do if t.hp>0 then aim(t.p)end end end
 g.p={7.8,-5.55};g.clock=5;step(.025);check(g.solved,'expanded dock can be completed with actual projectiles')
 load(1);local t=g.enemies[1];g:hit(t,1);check(not t.death_age,'ordinary hit is not destruction')
 g:hit(t,1);local explosions=0;for _,f in ipairs(g.fx)do if f.kind=='explosion'then explosions=explosions+1 end end
 check(explosions==1 and t.death_age==0,'final hit creates one explosion')
 check(g.pending_win and not g.dialog,'victory allows visible explosion before overlay')
 local f=g.fx[#g.fx];step(.2);check(f.age>=.19 and t.death_age>=.19,'animation advances even after final victory')
 local count=#g.fx;g:hit(t,1);check(#g.fx==count,'dead target cannot create duplicate explosions')
 step(1);check(#g.fx==0 and g.dialog=='win','effects expire and victory dialog follows')
 return n
end
return M
