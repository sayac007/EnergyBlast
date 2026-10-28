local Combat=require 'main.combat'
local Bonus=require 'main.bonus'
local Shots=require 'main.projectiles'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(i)local g=Combat.new(data);g:load(i);g.changed=function()end;return g end
 for i=1,#data.missions do
  local g=fresh(i);check(g.bonus.total==2 and #g.bonus.tasks==2,'two bonuses in mission '..i)
  for _,task in ipairs(g.bonus.tasks)do
   check(task.reward==(task.id=='prism'and 100 or 150),'displayed bonus reward matches earned key')
   for _,e in ipairs(task.targets)do
    check(e.optional and not g:blocked(e.p),'optional target on free floor')
    g:navigate(e.p);check(#g.path>0,'bonus reachable through actual movement graph')
   end
  end
 end
 local g=fresh(1);local task=g.bonus.tasks[1];local e=task.targets[1]
 g:hit(e,0);check(not task.done and e.hp==1 and g:total()==0,'direct shot cannot claim bank-shot bonus')
 -- Exercise the REAL swept reflection path against an arena wall.
 g.enemies={e};g.p={-9,e.p[2]};Shots.spawn(g,g.p,{-1,0},false)
 for i=1,80 do Shots.update(g,.02)end
 check(task.done and g:total()==100,'real reflected projectile awards optional crystal')
 check(not g.solved,'bonus alone cannot finish main mission')
 g:hit(e,1);check(g:total()==100,'no double bonus from dead target')
 g:load(1);check(g.bonus.completed==1 and g.bonus.tasks[1].targets[1].hp==0,'collected bonus persists on replay')
 local seq=fresh(1);local t=seq.bonus.tasks[2]
 seq:hit(t.targets[t.sequence[2]],0);check(t.progress==0 and not t.done,'wrong bonus order resets without awarding')
 for _,order in ipairs(t.sequence)do seq:hit(t.targets[order],0)end
 check(t.done and seq:total()==150,'correct remembered sequence awards150')
 check(seq.hp==3,'sequence mistakes cause no health penalty')
 local wait=fresh(2);local w=wait.bonus.tasks[2];local target=w.targets[1]
 Bonus.update(wait,2.99);wait:hit(target,0);check(not w.done,'red timing phase cannot be claimed')
 for i=1,20 do Bonus.update(wait,.45);wait:hit(target,0)end
 check(not w.done and wait:total()==0,'rapid repeated fire cannot brute-force patience bonus')
 Bonus.update(wait,3.01);wait:hit(target,0);check(w.done and wait:total()==150,'quiet wait followed by green shot awards150')
 local completed=fresh(2);for _,enemy in ipairs(completed.enemies)do if not enemy.optional then enemy.hp=0 end end
 completed.p={completed.m.goal[1],completed.m.goal[2]};completed.clock=5.5;completed:update(.01)
 check(completed.solved and completed.bonus.completed==0,'open bonus targets do not block mission completion')
 local total=completed:total();completed:finish();check(completed:total()==total,'finish remains one-time with bonuses')
 local forge=fresh(4);local crystal=forge.bonus.tasks[1].targets[1];forge.enemies={crystal}
 forge:trap(crystal.p,'magnet');forge:update(.05)
 check(#forge.traps==1 and not forge.bonus.tasks[1].done,'optional crystals cannot consume magnetic traps')
 local echo=fresh(5)
 for _,enemy in ipairs(echo.enemies)do if not enemy.optional and enemy.kind~='sequence'then enemy.hp=0 end end
 for _,order in ipairs(echo.m.sequence)do for _,enemy in ipairs(echo.enemies)do if enemy.kind=='sequence'and enemy.order==order then echo:hit(enemy,0);break end end end
 check(echo.solved and echo.bonus.completed==0,'required sequence finishes while optional timing and bank-shot targets remain')
 return n
end
return M
