-- Native swept-projectile checks against every wall type and changing gates.
local C=require 'main.combat'
local P=require 'main.projectiles'
local M={}
function M.run(g)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function step(s)for i=1,math.floor(s/.025+.001)do g:update(.025)end end
 local function sandbox(walls,p)
  g.saved={earned={},clues={},weapon='pulse'};g:load(1)
  local m={};for k,v in pairs(g.m)do m[k]=v end;g.m=m;g.m.absorbers={}
  g.walls=walls or{};g.p=p or{-1.5,0};g.enemies={};g.aim={1,0}
 end
 local function enemy(p)
  return{p=p,hp=2,max_hp=2,timer=999,warning=0,direction={1,0},burst=1}
 end
 for _,kind in ipairs({'cover','border','gate','reflector'})do
  sandbox({{r={0,-3,.25,6},type=kind}});g.aim=C.norm({1,.3});g:fire();local b=g.bullets[1];step(.2)
  check(b.bounces==1 and b.direction[1]<0 and b.p[1]<0,kind..' reflects a moving shot')
  check(math.abs(b.direction[2]-.3/math.sqrt(1.09))<1e-7,kind..' preserves tangential speed/angle')
 end
 sandbox({{r={-3,0,6,.25},type='cover'}},{0,-1.5});g.aim=C.norm({.3,1});g:fire();local b=g.bullets[1];step(.2)
 check(b.bounces==1 and b.direction[2]<0 and b.direction[1]>0,'horizontal face reverses only its normal component')
 sandbox({{r={0,-3,.25,6},type='cover'}},{1.5,0});g.aim=C.norm({-1,.2});g:fire();b=g.bullets[1];step(.2)
 check(b.bounces==1 and b.direction[1]>0,'opposite face reflects too')
 sandbox({{r={0,0,1,1},type='cover'}},{-1,-1});g.aim=C.norm({1,1});g:fire();b=g.bullets[1];step(.15)
 check(b.bounces==1 and b.direction[1]<0 and b.direction[2]<0,'exact corner flips both components without a loop')
 check(math.abs(b.direction[1]^2+b.direction[2]^2-1)<1e-7,'corner does not create speed')
 sandbox({{r={0,-3,.1,6},type='cover'}},{-.31,0});g:fire();b=g.bullets[1]
 check(b.p[1]==-.31,'muzzle offset cannot skip a nearby thin wall');step(.05)
 check(b.bounces==1 and b.p[1]<0,'close shot bounces instead of tunnelling')
 sandbox({{r={0,-3,.25,6},type='cover'}});local t=enemy({1.5,0});g.enemies={t};g:fire();step(.2)
 check(t.hp==2,'wall collision occurs before an enemy behind it')
 sandbox({{r={0,-3,.25,6},type='cover'}},{-2,-1});t=enemy({-2,1});t.shield=true;g.enemies={t};g.aim=C.norm({4,2});g:fire();step(.4)
 check(t.hp==1,'ordinary cover bank shot can defeat a shield')
 local corridor={{r={0,-2,.25,4},type='cover'},{r={-3.25,-2,.25,4},type='border'}}
 sandbox(corridor);g:fire();b=g.bullets[1];step(.5)
 check(b.bounces==1 and #g.bullets==0,'normal reflection budget stops the projectile at the next wall')
 sandbox(corridor);g.saved.earned={['mission:reactor']=true,['skill:reactor']=true};g.saved.weapon='prism';g:fire();b=g.bullets[1];step(.5)
 check(b.bounces==2 and #g.bullets==0,'Prisma reflects twice then expires')
 sandbox(nil,{0,0});g:fire();b=g.bullets[1];step(3)
 check(#g.bullets==0 and b.remaining<.00011,'range prevents permanent free-flying projectiles')
 sandbox({{r={0,-3,.25,6},type='cover'}},{-2,0});t=enemy({-1,0});t.warning=.001;g.enemies={t};g:update(.025);b=g.bullets[1];step(.9)
 check(b.enemy and b.bounces==1 and g.damage==1,'actual enemy warning produces a reflected shot that can hit the player')
 sandbox();g.m.gate_rect={0,-3,.25,6};g.clock=4.8;g:fire();b=g.bullets[1];step(.05);g.clock=5.1;step(.1)
 check(b.bounces==0 and b.p[1]>.25,'gate that opens during flight is no ghost reflector')
 sandbox();g.m.gate_rect={0,-3,.25,6};g.clock=5.1;g:fire();b=g.bullets[1];step(.025);g.clock=0;step(.15)
 check(b.bounces==1 and b.p[1]<0,'gate that closes during flight reflects on arrival')
 sandbox(nil,{0,0});local far,near=enemy({1,0}),enemy({.75,0});g.enemies={far,near};g:fire();g:update(.05)
 check(near.hp==1 and far.hp==2,'nearest swept target wins regardless of enemy list order')
 sandbox({{r={0,0,1,1},type='cover'}},{-.01,-1});g.aim={0,1};g:fire();b=g.bullets[1];step(.2)
 check(b.bounces==0 and b.direction[2]==1,'parallel grazing shot is not caught by an infinite corner bounce')
 sandbox(nil,{0,0});g:fire();b=g.bullets[1];b.remaining=999;step(2.8)
 check(b.alpha<1 and b.alpha>0,'energy visibly fades before timeout');step(.3)
 check(#g.bullets==0 and b.age<=3.00001,'hard lifetime removes even a long-range player shot')
 sandbox(nil,{0,0});g.m.absorbers={{position={1,0},radius=.65}};g:fire();step(.1)
 check(#g.bullets==0 and g.fx[#g.fx].kind=='absorb','neutraliser consumes player shot')
 check(not g:blocked({1,0}),'neutraliser remains walkable')
 sandbox(nil,{2,0});g.m.absorbers={{position={0,0},radius=.65}};b=P.spawn(g,{-2,0},{1,0},true);step(1)
 check(#g.bullets==0 and g.damage==0 and b.bounces==0,'neutraliser consumes enemy shot before the player')
 sandbox(nil,{0,0});b=P.spawn(g,{-2,2},{1,0},true);b.remaining=999;step(6.1)
 check(#g.bullets==0 and b.age<=6.00001,'enemy shot has finite lifetime too')
 return n
end
return M
