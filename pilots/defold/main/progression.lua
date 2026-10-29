-- Lifetime score never falls. Purchases spend a separate, derived star balance.
local P={}
local function catalogue(g,id)
 for _,item in ipairs(g.data.shop_catalog or{})do if item.id==id then return item end end
end
function P.bind(g)
 function g:wallet()
  local n=self:total()
  for _,price in pairs(self.saved.spent or{})do if type(price)=='number'and price>=0 then n=n-price end end
  return math.max(0,n)
 end
 function g:owns(id)
  if not self.data.shop_enabled then
   for _,u in ipairs(self.data.unlocks)do if u.id==id then return self:total()>=u.stars end end
   return false
  end
  return(self.saved.purchases or{})[id]==true
 end
 function g:max_health()
  if not self.data.recovery then return 3+(self:owns('armor')and 1 or 0)end
  local bonus=0
  for _,item in ipairs(self.data.shop_catalog)do
   if item.category=='armor'and self:owns(item.id)then bonus=math.max(bonus,item.health_bonus or 0)end
  end
  return self.data.player.hit_points+bonus
 end
 function g:weapon_stats()
  local base={id='pulse',damage=1,cooldown=self.data.combat.fire_cooldown,bounces=1}
  if self.data.shop_catalog then
   local item=catalogue(self,self.saved.weapon)
   if item and item.category=='weapon'and self:owns(item.id)then
    return{id=item.id,damage=item.damage or 1,cooldown=item.cooldown or base.cooldown,bounces=item.bounces or 1}
   end
  elseif self:owns('prism')and self.saved.weapon=='prism'then base.id='prism';base.bounces=2 end
  return base
 end
 function g:shop_item(id)
  local original=catalogue(self,id);if not original then return nil end
  local item={};for k,v in pairs(original)do item[k]=v end
  item.owned=not item.repeatable and self:owns(id)or false
  item.locked=item.requires~=nil and not self:owns(item.requires)
  item.equipped=item.category=='weapon'and self.saved.weapon==id and item.owned
  item.missing=math.max(0,item.price-self:wallet())
  item.available=not item.locked and item.missing==0 and not item.owned
  if item.id=='health'then item.available=item.available and self.hp~=nil and self.hp>0 and self.hp<self.max_hp end
  if item.category=='weapon'and item.owned then item.available=not item.equipped end
  return item
 end
 function g:shop_items(category)
  local rows={}
  for _,item in ipairs(self.data.shop_catalog or{})do
   if not category or item.category==category then rows[#rows+1]=self:shop_item(item.id)end
  end
  return rows
 end
 function g:can_buy(id)
  local item=self:shop_item(id)
  if not item then return false,'UNBEKANNT'end
  if item.owned then
   if item.category=='weapon'and not item.equipped then return true,'AUSRUESTEN'end
   return false,item.equipped and'AUSGERUESTET'or'GEKAUFT'
  end
  if item.locked then return false,'VORHERIGE STUFE ZUERST'end
  if item.id=='health'and(not self.hp or self.hp<=0 or self.over and not self.solved)then return false,'NEUER ANLAUF'end
  if item.id=='health'and self.hp>=self.max_hp then return false,'GESUNDHEIT VOLL'end
  if item.missing>0 then return false,'NOCH '..item.missing..' STERNE'end
  return true,'KAUFEN'
 end
 function g:buy(id)
  if self.data.shop_catalog then
   local item=self:shop_item(id);local allowed,reason=self:can_buy(id)
   if not allowed then self.shop_status=reason;return false end
   if item.owned and item.category=='weapon'then
    self.saved.weapon=id;self.shop_status='AUSGERUESTET';self.changed();return true
   end
   self.saved.purchases=self.saved.purchases or{};self.saved.spent=self.saved.spent or{}
   if item.repeatable then
    -- Each refill has a unique ledger entry; it never grants permanent ownership.
    local count=math.max(0,math.floor(tonumber(self.saved.health_purchases)or 0))+1
    while self.saved.spent['health:'..count]~=nil do count=count+1 end
    self.saved.health_purchases=count;self.saved.spent['health:'..count]=item.price
    self.hp=self.max_hp;self.regen_charge=0;self.regenerating=false
    self.shop_status='GESUNDHEIT VOLL'
   else
    self.saved.purchases[id]=true;self.saved.spent[id]=item.price
    if item.category=='weapon'then self.saved.weapon=id end
    if item.category=='armor'and self.hp then
     local old=self.max_hp;self.max_hp=self:max_health();self.hp=math.min(self.max_hp,self.hp+self.max_hp-old)
    end
    self.shop_status='AUSGERUESTET'
   end
   self.changed();return true
  end
  -- Unchanged historical shop behavior for frozen regression fixtures.
  for _,u in ipairs(self.data.unlocks)do if u.id==id then
   if self:owns(id)then if id=='prism'then self.saved.weapon=self.saved.weapon=='prism'and'pulse'or'prism';self.changed()end;return false end
   local cost=u.price or u.stars
   if self:wallet()<cost then self.shop_status='Noch '..(cost-self:wallet())..' Sterne';return false end
   self.saved.purchases=self.saved.purchases or{};self.saved.spent=self.saved.spent or{};self.saved.purchases[id]=true;self.saved.spent[id]=cost
   if id=='prism'then self.saved.weapon='prism'end
   if id=='armor'and self.hp then self.max_hp=self.max_hp+1;self.hp=math.min(self.max_hp,self.hp+1)end
   self.shop_status='AUSGERUESTET';self.changed();return true
  end end
  return false
 end
 function g:set_character(id)
  for _,c in ipairs(self.data.characters or{})do if c.id==id then self.saved.character=id;self.changed();return true end end;return false
 end
 function g:character()
  local id=self.saved.character or'hero'
  for _,c in ipairs(self.data.characters or{})do if c.id==id then return c end end
  return{id='hero',name='NOVA',shot='energy'}
 end
 -- Preserve all pre-shop automatic gear, then mark the migration exactly once.
 if g.data.shop_enabled and(type(g.saved.schema)~='number'or g.saved.schema<2)then
  g.saved.purchases=g.saved.purchases or{};g.saved.spent={}
  for _,u in ipairs(g.data.unlocks)do if g:total()>=u.stars then g.saved.purchases[u.id]=true end end
  g.saved.schema=2
 end
 if g.data.shop_catalog then g.saved.schema=3 end
end
return P
