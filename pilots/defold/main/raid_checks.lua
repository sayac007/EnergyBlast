-- Native-runtime regression for the shortlist iteration. No mocked renderer/engine.
local C=require 'main.combat'
local M={}
function M.run(g)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function step(t)for i=1,math.floor(t/.025)do g:update(.025)end end
 local function quiet()for _,t in ipairs(g.enemies)do t.timer=999;t.warning=0;t.patrol=nil end end
 local function aim(p)g.aim=C.norm({p[1]-g.p[1],p[2]-g.p[2]});g.cooldown=0;g:fire();step(1.5)end
 g.saved={earned={},clues={},weapon='pulse'};g:load(1)
 local x,y=g.project(g,{-4,2},0);g.input({x=x,y=y,pressed=true,id=1});g.input({x=x+160,y=y+40,id=2});g.input({x=x+160,y=y+40,released=true,id=2});check(#g.bullets==0 and not g.aiming,'second finger cannot fire the first finger gesture')
 g.input({x=x,y=y,released=true,id=1});check(#g.path>0,'owning finger still moves')
 g:load(1);local ex,ey=g.project(g,g.enemies[1].p,.8);g.input({x=ex,y=ey,pressed=true});g.input({x=ex,y=ey,released=true});check(#g.bullets==0 and #g.path>0,'short cannon tap is movement under the new duration rule')
 g:load(1);local cx,cy=g.project(g,{0,1},0);g.input({x=cx,y=cy,pressed=true});g.input({x=cx,y=cy,released=true});check(#g.bullets==0,'cover tap never interpreted as a shot')
 g:load(3);check(#g.enemies==5 and g.enemies[4].kind=='relay','three cannons and two relays')
 check(g:locked(g.enemies[1]),'boss protected by active relays')
 g:hit(g.enemies[1],1);check(g.enemies[1].hp==3,'bank shot cannot bypass relay protection')
 g:hit(g.enemies[4],0);check(g.enemies[4].hp==1,'relay resists direct shots')
 local p=g.enemies[2].p[1];g.enemies[2].timer=99;step(.4);check(g.enemies[2].p[1]>p+.2,'patrol actually moves')
 g.enemies[2].warning=.5;local stop=g.enemies[2].p[1];step(.2);check(g.enemies[2].p[1]==stop,'patrol stops to telegraph its locked shot')
 g:load(3);quiet();g.enemies[3].warning=.01;g.enemies[3].direction={1,0};step(.025);check(#g.bullets==3,'burst cannon produces three moving projectiles')
 g:load(3);quiet();g.p={-5.5,-2.5};g.hp=2;step(.025);check(g.hp==3 and g.heal_used,'health cell restores one missing hit')
 g.hp=2;step(.025);check(g.hp==2,'cell cannot be farmed')
 g:load(3);quiet();g.p={-5.5,-2.5};aim(g.enemies[2].p);aim(g.enemies[2].p);check(g.enemies[2].hp==0,'clear the mobile escort before the bank route');aim({-1,-5.25});check(g.enemies[4].hp==0,'actual reflected projectile destroys upper relay')
 g.p={4,3.5};aim({7.6,2.5});check(g.enemies[5].hp==0 and not g:locked(g.enemies[1]),'second bank shot disables boss protection')
 for i=1,3 do local t=g.enemies[i];g.p={t.p[1],t.p[2]+.65};for hit=1,3 do if t.hp>0 then aim(t.p)end end end
 check(not g.solved,'all enemies destroyed still requires the core')
 g.p={5.2,-3.7};g.clock=0;step(.025);check(not g.solved,'cannot exit while gate closed')
 g.clock=5;step(.025);check(g.solved and g:total()==200,'relay and cannon encounter can actually be completed')
 g:finish();check(g:total()==200,'dock victory never pays twice')
 g:load(3);quiet();g.p={-2.8,-2.3};step(.025);check(g.saved.earned['secret:dock']and g:total()==275,'hidden dock equipment and stars')
 g:dash();check(g.dash_cooldown<2.3,'earned capacitor improves dash recharge')
 g:load(3);quiet();g.hp=99;g:navigate({4,3.5});step(5);check(C.dist(g.p,{4,3.5})<.7,'far flank reachable without wall crossing')
 g:load(3);quiet();g.hp=99;g:navigate({-5.5,-2.5});step(3);check(C.dist(g.p,{-5.5,-2.5})<.7,'upper bank position and cell reachable')
 g.saved.clues={'dock:1'};check(g:level()==1 and g:credits()==1,'new clue preserved with existing credit system')
 return n
end
return M
